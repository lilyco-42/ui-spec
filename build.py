# -*- coding: utf-8 -*-
"""把 src/ 下的 CSS 合成一个文件，输出到 dist/ui.css。

为什么不用 PostCSS / Sass：
- 本项目没有构建链依赖，加一个 Node 工具链反而增加维护成本；
- 只需要"按固定顺序拼接 + 去掉重复注释"，20 行 Python 就够；
- 拼接顺序显式写在下面，比 glob 排序更可控。

用法：python build.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "dist"

# 顺序即层叠顺序，不要随意调整：
# base 先给重置，components 依赖它，utilities 最后才能覆盖。
ORDER = [
    "base.css",
    "components/button.css",
    "components/form.css",
    "components/card.css",
    "components/badge.css",
    "components/feedback.css",
    "components/overlay.css",
    "components/navigation.css",
    "components/data.css",
    "components/disclosure.css",
    "components/command.css",
    "utilities.css",
]

HEADER = """/*!
 * lain42 UI — 由 src/ 自动生成，不要直接改这个文件
 * 源文件见 src/ ，改完跑 python build.py
 */

"""


def build() -> int:
    DIST.mkdir(exist_ok=True)
    parts: list[str] = [HEADER]
    total = 0

    for rel in ORDER:
        path = SRC / rel
        if not path.exists():
            print(f"[error] 缺少源文件: {rel}", file=sys.stderr)
            return 1
        text = path.read_text(encoding="utf-8").rstrip()
        parts.append(f"\n/* ===== {rel} ===== */\n")
        parts.append(text)
        parts.append("\n")
        total += 1

    out = DIST / "ui.css"
    css = "".join(parts)
    out.write_text(css, encoding="utf-8")

    kb = len(css.encode("utf-8")) / 1024
    print(f"合并 {total} 个文件 -> {out.relative_to(ROOT)}  ({kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(build())