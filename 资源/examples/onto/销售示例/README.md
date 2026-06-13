# 销售示例 · 产品销售分析

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 数据空间 | 以示例脚本内 `space_id` 为准（复制后改 README） |
| 示例 ID | `sales`（见 `../index.yaml` / `index.json`） |

## 目录

| 路径 | 说明 |
| --- | --- |
| [plans/规划示例_产品销售本体规划方案.md](./plans/规划示例_产品销售本体规划方案.md) | **规划正文**（表/Cube/对象/函数/附录 B） |
| `setup/` | `sales_ontology_init.py`、`sales_seed_data.py`、`sales_category_mount.py` |
| `functions/` | 7 个 `sales_fn_*.py`、`test_arguments/`、`save_test_arguments.ps1` |

## 使用

- **规划阶段**：通读 `plans/*.md` 学结构；在本项目 `plans/` **独立撰写** + 差异说明
- **实施阶段**：`plans/` 定稿后对照 `setup/`、`functions/`；最后 run `sales_category_mount.py`（**平台分类** + **`s.domain` 域成员**；域 code = `sales`）

规范指南：`资源/docs/onto/本体规划指南.md`
