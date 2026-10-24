# -*- coding: utf-8 -*-
"""WCAG 对比度计算 —— 用来核实 design.md lint 的结论。

公式来自 WCAG 2.1：
  L = 0.2126*R + 0.7152*G + 0.0722*B   （R/G/B 是线性化后的相对亮度）
  ratio = (L1 + 0.05) / (L2 + 0.05)
"""

def _srgb_to_lin(c: float) -> float:
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def rel_lum(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _srgb_to_lin(r) + 0.7152 * _srgb_to_lin(g) + 0.0722 * _srgb_to_lin(b)


def ratio(fg: str, bg: str) -> float:
    l1, l2 = rel_lum(fg), rel_lum(bg)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


if __name__ == "__main__":
    pairs = [
        ("ink-mute #8b8c87 on white", "#8b8c87", "#ffffff"),
        ("ink-mute #8b8c87 on canvas-soft", "#8b8c87", "#f7f7f5"),
        ("ink-soft #62635f on white", "#62635f", "#ffffff"),
        ("ink-soft #62635f on canvas-soft", "#62635f", "#f7f7f5"),
        ("brand #167153 on white", "#167153", "#ffffff"),
        ("ink #202123 on white", "#202123", "#ffffff"),
        ("on-button #ffffff on button #202123", "#ffffff", "#202123"),
        ("dark-ink-mute #8f908c on dark-canvas #202123", "#8f908c", "#202123"),
        ("dark-ink-mute #8f908c on dark-surface #292a2d", "#8f908c", "#292a2d"),
        ("dark-ink-soft #b8b9b5 on dark-surface #292a2d", "#b8b9b5", "#292a2d"),
        ("dark-brand #67c79e on dark-canvas #202123", "#67c79e", "#202123"),
    ]
    print(f"{'组合':<48} {'比值':>7}  判定")
    print("-" * 70)
    for label, fg, bg in pairs:
        r = ratio(fg, bg)
        verdict = "PASS" if r >= 4.5 else "FAIL"
        print(f"{label:<48} {r:>6.2f}:1  {verdict}")
