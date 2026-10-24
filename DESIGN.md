---
version: alpha
name: lain42
description: >
  编辑风格的浅色界面，暖中性底 + 单一绿色品牌色。整体克制、留白大、
  边框细，靠字号与间距建立层级而不是靠阴影和色彩。品牌绿 #167153 用于
  可交互元素与强调标签，正文用近黑 #202123 保证长时间阅读不刺眼。
  暗色主题不是简单反色，而是保持同一套语义令牌、换一组值。

colors:
  # 底色层
  canvas: "#ffffff"
  canvas-soft: "#f7f7f5"
  surface: "#ffffff"
  surface-hover: "#f0f0ed"

  # 文字
  ink: "#202123"
  ink-soft: "#62635f"
  # 原值 #8b8c87 在白底只有 3.39:1、灰底 3.16:1，不达 WCAG AA。
  # 加深到 #6b6c68：白底 5.31:1、灰底 4.96:1，两个底都过线。
  ink-mute: "#6b6c68"
  ink-inverse: "#ffffff"

  # 线条
  line: "#e6e6e2"
  line-strong: "#d4d4cf"

  # 品牌与语义
  primary: "#167153"
  brand: "#167153"
  brand-soft: "#e8f3ee"
  on-brand: "#ffffff"
  success: "#167153"
  warning: "#9a6700"
  danger: "#c43b32"

  # 按钮
  button: "#202123"
  on-button: "#ffffff"

  # 暗色主题
  dark-canvas: "#202123"
  dark-canvas-soft: "#171717"
  dark-surface: "#292a2d"
  dark-surface-hover: "#343539"
  dark-ink: "#f4f4f2"
  dark-ink-soft: "#b8b9b5"
  # 原值 #8f908c 在 dark-surface(#292a2d) 上 4.47:1，差 0.03 不达标。
  # 提亮到 #9a9b97：dark-surface 上 5.06:1，dark-canvas 上 5.67:1。
  dark-ink-mute: "#9a9b97"
  dark-line: "#3b3c3f"
  dark-line-strong: "#515256"
  dark-brand: "#67c79e"
  dark-brand-soft: "#173d31"
  dark-on-brand: "#202123"

typography:
  body:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif'
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif'
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif'
    fontSize: 12px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0.12em
  title-sm:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif'
    fontSize: 14px
    fontWeight: 650
    lineHeight: 1.3
  title-md:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif'
    fontSize: 20px
    fontWeight: 650
    lineHeight: 1.3
    letterSpacing: -0.01em
  title-lg:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif'
    fontSize: 26px
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: -0.02em
  display:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif'
    fontSize: 36px
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: -0.02em

rounded:
  sm: 10px
  md: 12px
  lg: 20px
  pill: 999px

spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  xxl: 32px
  section: 58px

components:
  button-primary:
    backgroundColor: "{colors.button}"
    textColor: "{colors.on-button}"
    rounded: "{rounded.md}"
    padding: 10px 16px
    height: 44px
  button-brand:
    backgroundColor: "{colors.brand}"
    textColor: "{colors.on-brand}"
    rounded: "{rounded.md}"
    padding: 10px 16px
    height: 44px
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: 10px 16px
    height: 44px
  button-quiet:
    backgroundColor: "{colors.canvas-soft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: 10px 16px
    height: 44px
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: 24px
  card-muted:
    backgroundColor: "{colors.canvas-soft}"
    textColor: "{colors.ink-soft}"
    rounded: "{rounded.lg}"
    padding: 16px
  card-hover:
    backgroundColor: "{colors.surface-hover}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: 24px
  divider:
    backgroundColor: "{colors.line}"
    textColor: "{colors.ink-soft}"
    height: 1px
  divider-strong:
    backgroundColor: "{colors.line-strong}"
    textColor: "{colors.ink}"
    height: 1px
  brand-chip:
    backgroundColor: "{colors.brand-soft}"
    textColor: "{colors.brand}"
    rounded: "{rounded.pill}"
    padding: 5px 10px
  alert-success:
    backgroundColor: "{colors.brand-soft}"
    textColor: "{colors.success}"
    rounded: "{rounded.md}"
    padding: 12px
  alert-warning:
    backgroundColor: "{colors.canvas-soft}"
    textColor: "{colors.warning}"
    rounded: "{rounded.md}"
    padding: 12px
  alert-danger:
    backgroundColor: "{colors.canvas-soft}"
    textColor: "{colors.danger}"
    rounded: "{rounded.md}"
    padding: 12px
  button-on-dark:
    backgroundColor: "{colors.dark-brand}"
    textColor: "{colors.dark-on-brand}"
    rounded: "{rounded.md}"
    padding: 10px 16px
    height: 44px
  button-on-dark-quiet:
    backgroundColor: "{colors.dark-brand-soft}"
    textColor: "{colors.dark-brand}"
    rounded: "{rounded.md}"
    padding: 10px 16px
    height: 44px
  page:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
  caption:
    backgroundColor: "{colors.canvas-soft}"
    textColor: "{colors.ink-mute}"
    rounded: "{rounded.sm}"
    padding: 4px
  caption-dark:
    backgroundColor: "{colors.dark-canvas-soft}"
    textColor: "{colors.dark-ink-mute}"
    rounded: "{rounded.sm}"
    padding: 4px
  page-inverse:
    backgroundColor: "{colors.button}"
    textColor: "{colors.ink-inverse}"
    rounded: "{rounded.md}"
    padding: 12px
  surface-dark:
    backgroundColor: "{colors.dark-canvas}"
    textColor: "{colors.dark-ink}"
    rounded: "{rounded.lg}"
    padding: 24px
  surface-dark-soft:
    backgroundColor: "{colors.dark-canvas-soft}"
    textColor: "{colors.dark-ink-soft}"
    rounded: "{rounded.lg}"
    padding: 24px
  surface-dark-card:
    backgroundColor: "{colors.dark-surface}"
    textColor: "{colors.dark-ink}"
    rounded: "{rounded.lg}"
    padding: 24px
  surface-dark-hover:
    backgroundColor: "{colors.dark-surface-hover}"
    textColor: "{colors.dark-ink}"
    rounded: "{rounded.lg}"
    padding: 24px
  divider-dark:
    backgroundColor: "{colors.dark-line}"
    textColor: "{colors.dark-ink-soft}"
    height: 1px
  divider-dark-strong:
    backgroundColor: "{colors.dark-line-strong}"
    textColor: "{colors.dark-ink}"
    height: 1px
  text-muted-dark:
    backgroundColor: "{colors.dark-surface}"
    textColor: "{colors.dark-ink-soft}"
    rounded: "{rounded.md}"
    padding: 8px
  nav-item:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink-soft}"
    rounded: "{rounded.sm}"
    padding: 9px 11px
    height: 42px
  nav-item-active:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: 9px 11px
    height: 42px
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: 10px 12px
    height: 44px
  status-pill:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink-soft}"
    rounded: "{rounded.pill}"
    padding: 5px 10px
---

## Overview

**编辑式的克制**。界面像一份排版良好的长文：大留白、细边框、字号层级清晰，
不用渐变、不用大圆角卡片堆叠、不用装饰性阴影。

品牌电压来自**单一的绿色**（`#167153`）—— 它只出现在可交互元素和强调标签上，
面积很小但位置关键。其余全部是中性色，让内容本身成为视觉主角。

暗色主题不是简单反色：底从 `#ffffff` 变到 `#202123`，但品牌绿要提亮到 `#67c79e`
—— 深底上 `#167153` 的对比度不够，直接反色会失效。

## Colors

- **Ink (`#202123`)**：正文与标题。近黑而非纯黑，长时间阅读不刺眼。
- **Ink-soft (`#62635f`)**：次级说明文字，对比度 5.3–6.05:1。
- **Ink-mute (`#8b8c87`)**：标签、图注，对比度 4.78–5.45:1。**这是底线，不许再调浅。**
- **Brand (`#167153`)**：唯一的强调色，只用于交互与状态。
- **Canvas-soft (`#f7f7f5`)**：侧栏与页面分区底色，比纯白柔和。

**硬约束**：任何文字/背景组合对比度必须 ≥ 4.5:1。历史上本站曾有 23% 文本不达标，
现在是 0 处，不要退化。

## Typography

系统字体栈优先（`-apple-system` / `Segoe UI` / `PingFang SC`），
不加载网络字体 —— 中文网络字体动辄几 MB，首屏代价太高。

字号只用这套刻度：`12 14 16 20 26 36`，容忍 `11 11.5 13` 用于微型标签。
**不要用 em/%/rem 混算**，会产生 `13.33px` 这种非整数。

## Layout

内容区宽度 `min(100% - 48px, 1120px)` 居中。侧栏固定 `228px`，
在 `860px` 以下折叠为抽屉。

间距刻度：`4 8 12 16 24 32`，区块间用 `58px`。

## Elevation & Depth

**极少用阴影**。层级靠边框和底色区分，不靠投影。
只有两类场景用阴影：浮层（侧栏抽屉、弹窗）和悬浮卡片。

- `--shadow`: `0 1px 2px rgba(20,20,18,.05)` —— 卡片贴地感
- `--shadow-float`: `0 16px 50px rgba(20,20,18,.12)` —— 真正浮起来的东西

## Shapes

- `10px`：小元素（导航项、图标按钮）
- `12px`：按钮、输入框
- `20px`：卡片、面板
- `999px`：胶囊标签

## Components

按钮最小高度 **44px** —— 这是触摸目标下限，不是审美选择。
所有交互元素都要有 `:focus-visible` 轮廓（`3px` 品牌色 55% 透明）。

## Do's and Don'ts

**Do**
- 用语义令牌（`var(--fg-soft)`），不写死颜色
- 用 `clamp()` 做响应式，但两端落在字号刻度上
- 给所有交互元素 44px 最小触摸区

**Don't**
- 不要引入 Tailwind / Bootstrap / React 重构现有静态站
- 不要嵌套 `<a>`（非法 HTML，浏览器会拆开）
- 不要用有 fallback 的 `var(--undefined, #666)` —— fallback 会掩盖变量缺失
