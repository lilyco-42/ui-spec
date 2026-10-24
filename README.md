# ui-spec · lain42 设计规范

**可被脚本强制执行**的 UI 规范。不是一堆说明文档，而是能被 linter 检查、
能被 CI 拦截、能导出成 CSS 变量的单一事实来源。

```
DESIGN.md          ← 唯一事实来源（YAML 令牌 + 设计理由）
dist/tokens.css    ← 由 DESIGN.md 生成，不要手改
contrast.py        ← WCAG 对比度计算（核实 lint 结论）
```

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
