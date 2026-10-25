# -*- coding: utf-8 -*-
"""用真实渲染像素核对对比度 —— 不依赖 getComputedStyle。

为什么必须这样：
1. AGENTS.md 明确禁止凭 CSS 值推算对比度；
2. 实测无头 Chrome 在动态改 data-theme 后，getComputedStyle 返回缓存值
   （变量已是 #202123，bodyBg 仍报白色），会误报大量假失败；
3. color-mix()、半透明、backdrop-filter 都让推算偏离真实像素。

做法：渲染 -> 截图 -> 对每个文字元素取其包围盒内出现最多的颜色作为背景，
      文字颜色用 getComputedStyle（这个是准的），再用 WCAG 公式算比值。

用法：python verify_pixels.py light|dark [--width N]
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

from contrast import ratio

ROOT = Path(__file__).parent


def find_chrome() -> str:
    """找 Chrome/Chromium。CI 用 setup-chrome 装到 PATH，本地是固定路径。"""
    import os
    import shutil

    env = os.environ.get("CHROME_BIN") or os.environ.get("CHROME_PATH")
    if env and Path(env).exists():
        return env
    for name in ("chrome", "google-chrome", "chromium", "chromium-browser", "chrome.exe"):
        found = shutil.which(name)
        if found:
            return found
    for p in (
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ):
        if Path(p).exists():
            return p
    raise SystemExit("找不到 Chrome，请设置 CHROME_BIN 环境变量")


CHROME = find_chrome()

COLLECT_JS = r"""
(() => {
  const out = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    const text = node.textContent.trim();
    if (!text) continue;
    const el = node.parentElement;
    if (!el || el.closest("[hidden]")) continue;
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden" || cs.opacity === "0") continue;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    // 跳过完全不可见的元素（skip-link 平时在 top:-60px）
    if (r.bottom < 0) continue;
    // 跳过透明/近乎透明的文字
    const fgAlpha = cs.color.startsWith("rgba") ? parseFloat(cs.color.split(",")[3]) : 1;
    if (fgAlpha < 0.9) continue;
    out.push({
      text: text.slice(0, 20),
      cls: (typeof el.className === "string" ? el.className : "").slice(0, 44),
      color: cs.color,
      size: parseFloat(cs.fontSize),
      weight: parseInt(cs.fontWeight) || 400,
      x: Math.round(r.left), y: Math.round(r.top),
      w: Math.round(r.width), h: Math.round(r.height)
    });
  }
  return JSON.stringify({ items: out, pageHeight: Math.ceil(document.body.scrollHeight) });
})()
"""


def parse_rgb(s: str) -> tuple[int, int, int]:
    inner = s[s.index("(") + 1 : s.index(")")]
    parts = [p.strip() for p in inner.split(",")]
    return int(float(parts[0])), int(float(parts[1])), int(float(parts[2]))


def dominant_color(im: Image.Image, x: int, y: int, w: int, h: int) -> tuple[int, int, int]:
    """取包围盒内出现最多的颜色 —— 那就是背景（文字像素占比小）。"""
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(im.width, x + w), min(im.height, y + h)
    if x1 <= x0 or y1 <= y0:
        return (255, 255, 255)
    # 采样控制成本：步长自适应
    step = max(1, min(w, h) // 24)
    counter: Counter[tuple[int, int, int]] = Counter()
    for py in range(y0, y1, step):
        for px in range(x0, x1, step):
            counter[im.getpixel((px, py))] += 1
    return counter.most_common(1)[0][0] if counter else (255, 255, 255)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    theme = args[0] if args else "light"
    width = 1280
    for a in sys.argv[1:]:
        if a.startswith("--width"):
            width = int(a.split("=")[1]) if "=" in a else 1280

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    # 关键：主题必须写成静态属性，不能在 load 之后用 JS 设置。
    # 否则截图已经按浅色画完了，会误报大量假失败（实测 21 处）。
    if theme == "dark":
        html = html.replace("<html lang=", '<html data-theme="dark" lang=', 1)
    injected = html.replace(
        "</body>",
        f'<script>window.__COLLECT__ = {COLLECT_JS};'
        f'window.addEventListener("load",function(){{'
        f'document.title="R:"+btoa(unescape(encodeURIComponent(window.__COLLECT__)));'
        f'}});</script></body>',
    )
    tmp_html = ROOT / f"_pix_{theme}.html"
    tmp_html.write_text(injected, encoding="utf-8")
    url = f"file:///{tmp_html.as_posix()}"

    # 1) 先量页面高度（截太高会浪费，截太短会错位）
    res = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", f"--window-size={width},900",
         "--virtual-time-budget=4000", "--dump-dom", url],
        capture_output=True, encoding="utf-8", timeout=120,
    )
    import base64, re
    m = re.search(r"<title>R:([A-Za-z0-9+/=]+)</title>", res.stdout)
    if not m:
        print("提取元素信息失败", file=sys.stderr)
        return 1
    payload = json.loads(base64.b64decode(m.group(1)).decode("utf-8"))
    items = payload["items"]
    page_h = payload["pageHeight"]

    # 2) 按真实高度截图，保证坐标一一对应
    shot = ROOT / f"_pix_{theme}.png"
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         f"--window-size={width},{page_h}", f"--screenshot={shot}",
         "--virtual-time-budget=4000", url],
        capture_output=True, timeout=120,
    )

    im = Image.open(shot).convert("RGB")
    print(f"主题={theme}  视口宽={width}  截图={im.width}x{im.height}  文字元素={len(items)}")

    results = []
    seen = set()
    for it in items:
        fg = parse_rgb(it["color"])
        bg = dominant_color(im, it["x"], it["y"], it["w"], it["h"])
        r = ratio("#%02x%02x%02x" % fg, "#%02x%02x%02x" % bg)
        key = (fg, bg)
        if key in seen:
            continue
        seen.add(key)
        results.append((r, it, fg, bg))

    results.sort(key=lambda t: t[0])
    print()
    print("最差的 10 组：")
    print("  比值    字号  前景 -> 背景                    元素")
    print("  " + "-" * 74)
    for r, it, fg, bg in results[:10]:
        print(f"  {r:5.2f}:1 {it['size']:>4.0f}px  "
              f"#{fg[0]:02x}{fg[1]:02x}{fg[2]:02x} -> #{bg[0]:02x}{bg[1]:02x}{bg[2]:02x}  "
              f"{(it['cls'] or it['text'])[:34]}")

    fails = []
    for r, it, fg, bg in results:
        large = it["size"] >= 24 or (it["size"] >= 18.66 and it["weight"] >= 700)
        if r < (3.0 if large else 4.5):
            fails.append((r, it, fg, bg))

    print()
    if fails:
        print(f"❌ {len(fails)} 组不达标")
        for r, it, fg, bg in fails:
            print(f"   {r:.2f}:1 {it['size']:.0f}px [{it['cls']}] {it['text']}")
        return 1
    print("✅ 全部达标")
    return 0


if __name__ == "__main__":
    sys.exit(main())
