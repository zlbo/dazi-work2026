# 成本报表测试01（`financial-cost-report-08`）· 应用 AI 上下文

> 由 `dazi-app init` / `context refresh` / `doctor` 维护。  
> **模板 `.ai/page-intent` 等仅为初始示例**；开发规则以 [`.ai/overview.md`](./.ai/overview.md) 与 manifest 为准。

## 应用元信息

| 项 | 值 |
|----|-----|
| app_id | `financial-cost-report-08` |
| 空间 | `space__misc_01` |
| 模板 | `financial-indicators-report-02-template` |
| 目录 | `D:/src2025/ads2025/dazi-work/项目/app_财务报表01/apps/financial-cost-report-08` |

## 数据源（manifest）

| key | kind | 引用 | 备注 |
|-----|------|------|------|
| report_data | static | inline static | |

## 场景意图（摘录 · 模板示例）

```markdown
> ⚠️ 本文件由模板 `financial-indicators-report-01-template` 提供**初始示例**，仅作参考。
> - 通用规范：[`.ai/overview.md`](./overview.md)
> - 数据源：`docs/data-source-cookbook.md` · 内联：`docs/inline-data-source.md`
> - 视觉：`docs/ui-style-guide.md`
> - 可按业务自由扩展：增减 KPI、改用 Grid/表单、新增 manifest key 等

# 页面意图（动态模板）

- 来源应用：`financial-indicators-report-01`
- 由 release 转换，UI 与数据绑定以源码为准。
- data_sources 绑定保留原空间配置，跨空间 init 后须手改 manifest。

---

## 本应用业务目标（请填写）

- 服务对象：
- 关键决策 / 动作：
- 必看指标 / 字段：
- 与模板示例的差异：

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
- ID: `space__misc_01`

## 应用
- app_id: `financial-cost-report-08`
- 名称: 成本报表测试01
- 模板: `financial-indicators-report-02-template`

## 开发提示
- 通用指引见 `.ai/overview.md`
- 数据绑定见 `.ai/data-binding.md`
- 禁止裸 fetch，统一使用 @dazi/app-sdk-data
…
```

## 自检待办（doctor）

- [ ] 缺少 overview.md（通用）
- [ ] 缺少 data-binding.md
- [x] 已有 page-intent.md
- [x] 已有 CONTEXT.md（context refresh）

## 常用命令

```powershell
pnpm run dev   # 在应用组件目录
# 在 dazi-work 根执行（推荐，自动 bundled CLI）
dazi app manifest validate --cwd 项目/app_财务报表01/apps/financial-cost-report-08 --scan-src
dazi app doctor --cwd 项目/app_财务报表01/apps/financial-cost-report-08
dazi app upload --cwd 项目/app_财务报表01/apps/financial-cost-report-08 --space space__misc_01 --activate
```

## 铁律

- 禁止裸 fetch；只用 @dazi/app-sdk-data
- 改 manifest 后必须 upload --activate
- 视觉见 `runtime-apps/docs/ui-style-guide.md`
- 详见 `runtime-apps/AGENTS.md`
