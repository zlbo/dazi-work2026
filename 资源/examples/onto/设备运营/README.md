# 设备运营 · 化工设备运营分析

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 数据空间 | 分类测试01 |
| 数据空间 ID | `space_cate_test01` |
| 示例 ID | `equip-ops`（见 `../index.yaml` / `index.json`） |

## 目录

| 路径 | 说明 |
| --- | --- |
| [plans/化工设备运营分析本体方案.md](./plans/化工设备运营分析本体方案.md) | **规划正文**（OEE、停机等） |
| `setup/` | `equip_ops_ontology_init.py`、`equip_ops_seed_data.py`、`equip_ops_category_mount.py` |
| `functions/` | 11 个 `equip_ops_fn_*.py`、`test_arguments/` |

## 使用

- **规划阶段**：推荐阅读（含 Cube + 冗余字段策略 + 11 函数清单）
- **实施阶段**：init 不含 `apply_registry`；见 `equip_ops_category_mount.py`

规范指南：`资源/docs/onto/本体规划指南.md`
