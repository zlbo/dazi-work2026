# 数据绑定

## 默认（P1 演示）

三个 key 均使用 **`static`**，不依赖空间内本体注册，任意 `space_id` 均可展示：

| key         | kind     | 说明                          |
|-------------|----------|-------------------------------|
| `kpi`       | `static` | 单行 KPI：revenue / profit / profit_rate |
| `trend`     | `static` | 月度趋势 rows                 |
| `yoy_table` | `static` | 同环比表                      |

## 接真实本体（FC02 等已种子空间）

将 `manifest.json` 中 `kpi` / `trend` 改为：

| key   | kind                | 说明 |
|-------|---------------------|------|
| `kpi` | `ontology_semantic` | `object_type_code`: **`FinPLMonthFact`**（非 monthly_pl） |
| `trend` | `ontology_function` | `function_id`: **`fc02.fn.month_pl_budget_kpi`**，object_type: `FinPLMonthFact` |

需在本空间执行 FC02 本体种子（见 `docs/daziscript/fin_cockpit02_space_init.py`）。

## 读取

```tsx
import { useDataset } from "@dazi/app-sdk-data";

const kpi = useDataset("kpi");
const row = kpi.data?.data?.[0] ?? {};
```

## 刷新

- 自动：`manifest.refresh.on_mount=true`
- 主动：`kpi.refetch()` / `trend.refetch()`
