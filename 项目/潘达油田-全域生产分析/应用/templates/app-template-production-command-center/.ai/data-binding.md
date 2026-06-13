# 数据绑定（模板示例）

## 默认（static 演示）

| key | kind | 说明 |
|-----|------|------|
| `kpi` | `static` | KPI 行：`label` / `value` / `unit`（行数任意） |

## 接真实数据

按场景选用（可混用，见 `docs/data-source-cookbook.md`、`docs/inline-data-source.md`）：

| kind | 说明 |
|------|------|
| `sql_template` / `script_entry` | 空间内已保存查询 / 已发布脚本 |
| `sql_asset` / `script_asset` | `drap-assets/` 内文件（推荐） |
| `cube_query` / `ontology_*` | 语义层与本体 |

init 可选档：`--profile sql-asset` / `script-asset` / `sql-script` 等。

## 读取

```tsx
import { useDataset } from "@dazi/app-sdk-data";

const kpi = useDataset("kpi");
const rows = kpi.data?.data ?? [];
```

新增数据集：在 manifest 增加 `key`，组件中 `useDataset("新key")`。
