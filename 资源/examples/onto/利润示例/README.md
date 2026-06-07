# 利润示例 · GL / 利润分析

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 数据空间 | 以示例脚本内 `space_id` 为准（复制后改 README） |
| 示例 ID | `profit`（见 `../index.yaml` / `index.json`） |

## 目录

| 路径 | 说明 |
| --- | --- |
| [plans/规划示例_利润分析本体方案.md](./plans/规划示例_利润分析本体方案.md) | **规划正文** |
| `setup/` | `profit_ontology_init.py`、`profit_seed_data.py`、`profit_category_mount.py` |
| `functions/` | 7 个 `profit_fn_*.py`、`test_arguments/` |

## 使用

- **规划阶段**：通读 `plans/*.md`；与 [销售示例](../销售示例/) 对照时写清差异说明
- **实施阶段**：init **不含** `apply_registry`；分类在 `profit_category_mount.py`（最后执行）

规范指南：`资源/docs/onto/本体规划指南.md`
