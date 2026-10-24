# -*- coding: utf-8 -*-
"""独立核对关键令牌的对比度 —— 不依赖 node / linter。

为什么要有这个：linter 版本升级可能改规则，也可能某天不可用。
这里用 WCAG 2.1 公式自己算，作为第二道闸门。

退出码：0 全部达标 / 1 有令牌不达标
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from contrast import ratio

REQUIRED = [
    ("ink on canvas", "ink", "canvas", 4.5),
    ("ink-soft on canvas", "ink-soft", "canvas", 4.5),
    ("ink-mute on canvas", "ink-mute", "canvas", 4.5),
    ("ink-mute on canvas-soft", "ink-mute", "canvas-soft", 4.5),
    ("brand on canvas", "brand", "canvas", 4.5),
    ("on-brand on brand", "on-brand", "brand", 4.5),
    ("on-button on button", "on-button", "button", 4.5),
    ("dark-ink on dark-canvas", "dark-ink", "dark-canvas", 4.5),
    ("dark-ink-soft on dark-surface", "dark-ink-soft", "dark-surface", 4.5),
    ("dark-ink-mute on dark-surface", "dark-ink-mute", "dark-surface", 4.5),
    ("dark-brand on dark-canvas", "dark-brand", "dark-canvas", 4.5),
]


def parse_colors(md_path: Path) -> dict[str, str]:
    """从 DESIGN.md 的 YAML front matter 里抠出颜色令牌。

    不装 pyyaml 也能跑 —— 只匹配 name: "#rrggbb" 这种简单行。
    """
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        raise SystemExit("找不到 YAML front matter")
    body = m.group(1)

    # 逐行状态机：进入 colors: 段就收集，遇到顶格非空行就退出。
    # 比正则稳 —— 注释行、空行、缩进差异都不会打断解析。
    colors: dict[str, str] = {}
    in_colors = False
    for line in body.splitlines():
        if re.match(r"^colors:\s*$", line):
            in_colors = True
            continue
        if in_colors:
            if line and not line[0].isspace():
                break  # 出了 colors 段
            mm = re.match(r'\s+([a-z0-9-]+):\s*"(#[0-9a-fA-F]{6})"', line)
            if mm:
                colors[mm.group(1)] = mm.group(2)
    return colors


def main() -> int:
    colors = parse_colors(Path("DESIGN.md"))
    print(f"解析到 {len(colors)} 个颜色令牌")
    print()

    failed: list[str] = []
    print(f"{'组合':<38} {'比值':>8}  判定")
    print("-" * 60)
    for label, fg_key, bg_key, minimum in REQUIRED:
        fg, bg = colors.get(fg_key), colors.get(bg_key)
        if not fg or not bg:
            print(f"{label:<38} {'缺失令牌':>8}  SKIP")
            continue
        r = ratio(fg, bg)
        ok = r >= minimum
        print(f"{label:<38} {r:>7.2f}:1  {'PASS' if ok else 'FAIL'}")
        if not ok:
            failed.append(f"{label} = {r:.2f}:1 (需要 >= {minimum})")

    print()
    if failed:
        print("以下令牌不达 WCAG AA：")
        for f in failed:
            print("  -", f)
        return 1
    print("全部达标")
    return 0


if __name__ == "__main__":
    sys.exit(main())