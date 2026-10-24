# 怎么用这套规范

## 场景 1：写新页面

1. 读 `DESIGN.md` 的 `colors` / `typography` / `spacing`
2. **只用里面定义的值**，不凭空造颜色和字号
3. 写完跑 `python check_tokens.py` 确认没有引入不达标组合

## 场景 2：接入现有项目

### lain42.top（静态站）

现有 `assets/studio.css` 里的变量名是 `--fg` / `--bg` / `--brand`，
本仓库导出的是 `--color-ink` / `--color-canvas` / `--color-brand`。

两种接法：

**A. 改 DESIGN.md 的令牌名对齐现有 CSS**（推荐，改动小）
把 `ink` → `fg`、`canvas` → `bg` 等重命名，导出的 CSS 就能直接替换。

**B. 改现有 CSS 用新名**（改动大，但命名更清晰）
需要全站替换，风险高。

### lyco-sub / rembg-ui（有构建链）

直接用导出：

```bash
npx -p "@google/design.md" designmd export DESIGN.md --format css-tailwind > theme.css
```

## 场景 3：给 AI 代理下指令

把 `DESIGN.md` 放进项目根目录，agent 会自动读到。指令模板：

> 按 DESIGN.md 实现这个页面。只用其中定义的令牌，
> 不新增颜色。写完用 `designmd lint` 检查。

## 场景 4：防止设计回归

改动前后各存一份，用 diff 对比：

```bash
npx -p "@google/design.md" designmd diff DESIGN.md DESIGN-new.md
```

输出里的 `regression: true` 表示引入了倒退（比如删了令牌、对比度变差）。

---

## 踩过的坑

### Windows 下 `design.md` 命令无输出

`npx @google/design.md lint` 在 PowerShell 里会和 Markdown 文件关联冲突。
用点号无关的别名：

```bash
npx --yes -p "@google/design.md" designmd lint DESIGN.md
```

### YAML 注释会打断简单正则

写解析脚本时，别用 `^colors:\n((?:[ \t]+.*\n)+)` 这种正则 ——
遇到 `# 底色层` 注释行就断了。用逐行状态机。

### 令牌定义了却不用会被警告

`orphaned-tokens` 规则要求每个令牌至少被一个 component 引用。
这是好事：防止设计系统里堆积没人用的死令牌。

但如果某个令牌确实只在特定场景用（比如 `ink-mute` 只用于图注），
就要补一个 component 把它引用起来，否则 lint 会一直警告。
