# ui-spec · lain42 设计规范与组件库

**可被脚本强制执行**的 UI 规范 + 48 个开箱即用组件。
不是一堆说明文档，而是能被 linter 检查、被 CI 拦截、被真实浏览器验证的
单一事实来源。

```
DESIGN.md          ← 唯一事实来源（54 色 / 7 字号 / 48 组件）
src/               ← 组件源文件（改这里）
dist/tokens.css    ← 由 DESIGN.md 生成，不要手改
dist/ui.css        ← 由 src/ 合并生成，不要手改
index.html         ← 组件总览，浏览器直接打开
build.py           ← src/ -> dist/ui.css
contrast.py        ← WCAG 对比度计算
check_tokens.py    ← 独立核对（不依赖 node）
verify_pixels.py   ← 真实渲染像素验证（抓 CSS 变量失效这类 bug）
```

## 组件一览

**无框架、无构建链**，纯 CSS + 4KB 原生 JS。适合手写 HTML 的静态站
（如 lain42.top），也适合任何有构建链的项目。

| 类别 | 组件 |
|---|---|
| 按钮 | `.btn` 6 变体 · 3 尺寸 · 图标 · 加载态 · 禁用态 · `.btn-group` |
| 表单 | `.input` `.textarea` `.select` `.input-group` `.check` `.switch` `.slider` 校验态/禁用态 |
| 容器 | `.card` 4 变体 · `.panel` · `.list` |
| 标记 | `.badge` 6 变体 · `.dot` · `.kbd` · `.avatar` · `.chip` |
| 反馈 | `.alert` 4 变体 · `.progress` · `.spinner` · `.skeleton` · `.empty` · `.toast` |
| 覆盖层 | `.dialog` · `.drawer` · `.menu` · `.tooltip` · `.popover` |
| 导航 | `.tabs` · `.breadcrumb` · `.pagination` · `.sidebar` · `.topbar` · `.shell` |
| 数据 | `.table` · `.desc` · `.stat` · `.timeline` |
| 折叠 | `.accordion` · `.collapsible` · `.toggle` · `.toggle-group` · `.separator` · `.ratio` · `.scroll-area` |
| 命令面板 | `.command`（输入过滤 + 上下键 + 回车） |

`src/ui.js` 只做 CSS 做不到的部分：标签页键盘导航、`<dialog>` 开关、
下拉菜单、Toast、命令面板过滤、主题切换。没有 JS 时页面仍可用。

```html
<link rel="stylesheet" href="dist/tokens.css">
<link rel="stylesheet" href="dist/ui.css">
<script src="src/ui.js" defer></script>

<button class="btn btn--brand">开始</button>
<span class="badge badge--success">已完成</span>
```

## 三道验证闸门

| 闸门 | 抓什么 | 命令 |
|---|---|---|
| `designmd lint` | 对比度、孤立令牌、结构 | `npx -p "@google/design.md" designmd lint DESIGN.md` |
| `check_tokens.py` | 同上，但不依赖 node | `python check_tokens.py` |
| `verify_pixels.py` | **真实渲染**的对比度 | `python verify_pixels.py light\|dark` |

第三道是关键。前两道都基于令牌值推算，抓不到「暗色主题变量没生效」
这类问题——实测踩过：`getComputedStyle` 在动态改 `data-theme` 后返回
缓存值，会同时骗过验证脚本和开发者。只有截图取真实像素才靠得住。

## 为什么用 DESIGN.md 格式

调研结论（2026-10）：[google-labs-code/design.md](https://github.com/google-labs-code/design.md)
（28.5k★）已是事实标准，配套 `@google/design.md` 提供 lint / diff / export。
自研格式等于重造标准，还会失去与 [W3C DTCG](https://github.com/design-tokens/community-group)
生态的互操作性。

**决定：采用，不自研。**

## 常用命令

```bash
# 校验（CI 里跑这个）
npx -p "@google/design.md" designmd lint DESIGN.md

# 导出 CSS 变量
npx -p "@google/design.md" designmd export DESIGN.md --format css-vars > dist/tokens.css

# 导出 Tailwind v4
npx -p "@google/design.md" designmd export DESIGN.md --format css-tailwind

# 导出 W3C DTCG 标准格式
npx -p "@google/design.md" designmd export DESIGN.md --format dtcg

# 对比两个版本，检测设计回归
npx -p "@google/design.md" designmd diff DESIGN.md DESIGN-old.md

# 核对对比度（不依赖 node）
python contrast.py
```

⚠️ Windows PowerShell 下要用 `designmd` 而不是 `design.md` ——
后者会和 Markdown 文件关联冲突，导致命令无输出。

## 强制执行的规则

| 规则 | 检查方式 | 失败后果 |
|---|---|---|
| 文字对比度 ≥ 4.5:1 | `lint` 的 `contrast-ratio` | CI 失败 |
| 必须有 `primary` 色 | `lint` 的 `missing-primary` | CI 失败 |
| 令牌不能定义后不用 | `lint` 的 `orphaned-tokens` | 警告 |
| 章节顺序固定 | `lint` 结构检查 | 错误 |

## 已修正的真实缺陷

规范建立过程中发现并修复：

| 问题 | 原值 | 实测对比度 | 修正后 |
|---|---|---|---|
| `--fg-mute` 白底 | `#8b8c87` | **3.39:1 ❌** | `#6b6c68` → 5.29:1 ✅ |
| `--fg-mute` 灰底 | `#8b8c87` | **3.16:1 ❌** | `#6b6c68` → 4.93:1 ✅ |
| 暗色 `mute` | `#8f908c` | **4.47:1 ❌** | `#9a9b97` → 5.13:1 ✅ |

**注意**：站点 `AGENTS.md` 里写「`--fg-mute` 4.78:1 刚好过线」是**错的**。
实测 3.39:1，明确不达标。以本仓库的实测值为准。

## 给 AI 代理用

这个文件本身就是给 agent 读的。agent 读 `DESIGN.md` 后应当：

1. 只用 `colors` 里定义的令牌，不凭空造颜色；
2. 文字/背景组合先查对比度；
3. 组件样式引用 `components` 里的定义，不自由发挥。

## 许可证

MIT
