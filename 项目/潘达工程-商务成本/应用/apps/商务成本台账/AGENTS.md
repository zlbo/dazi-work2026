# 商务成本台账（`chinese-complex-report-20260614005541`）· 应用 AI 上下文

> 由 `dazi-app init` / `context refresh` / `doctor` 维护。  
> **模板 `.ai/page-intent` 等仅为初始示例**；开发规则以 [`.ai/overview.md`](./.ai/overview.md) 与 manifest 为准。

## 应用元信息

| 项 | 值 |
|----|-----|
| app_id | `chinese-complex-report-20260614005541` |
| 空间 | `space__panda_construction` |
| 模板 | `chinese-complex-report` |
| 目录 | `D:/GitHub/dazi-work/项目/潘达工程-商务成本/应用/apps/商务成本台账` |

## 数据源（manifest）

| key | kind | 引用 | 备注 |
|-----|------|------|------|
| report_data | static | inline static | |

## 场景意图（摘录 · 模板示例）

```markdown
（未找到）
```

## 数据绑定（摘录）

```markdown
（未找到）
```

## 空间上下文

完整列表见 [`.ai/CONTEXT.md`](./.ai/CONTEXT.md)（执行 `dazi-app context refresh` 更新）。

```markdown
# 当前空间上下文（DRAP）

> 由 `dazi-app init` 生成。完整上下文请执行 `dazi-app context refresh`（P3）。

## 数据空间
- ID: `space__panda_construction`

## 应用
- app_id: `chinese-complex-report-20260614005541`
- 名称: 商务成本台账
- 模板: `chinese-complex-report`

## 开发提示
- 通用指引见 `.ai/overview.md`
- 数据绑定见 `.ai/data-binding.md`
- 禁止裸 fetch，统一使用 @dazi/app-sdk-data
…
```

## 自检待办（doctor）

- [ ] 缺少 overview.md（通用）
- [ ] 缺少 data-binding.md
- [ ] 缺少 page-intent.md
- [x] 已有 CONTEXT.md（context refresh）

## 常用命令

```powershell
pnpm run dev   # 在应用组件目录
# 在 dazi-work 根执行（推荐，自动 bundled CLI）
dazi app manifest validate --cwd 项目/潘达工程-商务成本/应用/apps/商务成本台账 --scan-src
dazi app doctor --cwd 项目/潘达工程-商务成本/应用/apps/商务成本台账
dazi app upload --cwd 项目/潘达工程-商务成本/应用/apps/商务成本台账 --space space__panda_construction --activate
```

## 铁律

- 禁止裸 fetch；只用 @dazi/app-sdk-data
- 改 manifest 后必须 upload --activate
- 视觉见 `runtime-apps/docs/ui-style-guide.md`
- 详见 `runtime-apps/AGENTS.md`
