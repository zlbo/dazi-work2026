# 财务报表01（`alarm-center0531`）· 应用 AI 上下文

> 由 `dazi-app init` / `context refresh` / `doctor` 维护。  
> **模板 `.ai/page-intent` 等仅为初始示例**；开发规则以 [`.ai/overview.md`](./.ai/overview.md) 与 manifest 为准。

## 应用元信息

| 项 | 值 |
|----|-----|
| app_id | `alarm-center0531` |
| 空间 | `space__0519` |
| 模板 | `alarm-center` |
| 目录 | `D:/src2025/ads2025/dazi-work/项目/app_财务报表01/apps/alarm-center0531` |

## 数据源（manifest）

| key | kind | 引用 | 备注 |
|-----|------|------|------|
| alarms | static | inline static | |

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
- ID: `space__0519`

## 应用
- app_id: `alarm-center0531`
- 名称: 财务报表01
- 模板: `alarm-center`

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
pnpm run dev
pnpm -C ..\.. run dazi-app -- manifest validate --scan-src
pnpm -C ..\.. run dazi-app -- doctor
pnpm -C ..\.. run dazi-app -- upload --cwd . --space space__0519 --activate
```

## 铁律

- 禁止裸 fetch；只用 @dazi/app-sdk-data
- 改 manifest 后必须 upload --activate
- 视觉见 `runtime-apps/docs/ui-style-guide.md`
- 详见 `runtime-apps/AGENTS.md`
