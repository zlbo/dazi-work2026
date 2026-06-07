# 本体分类规划与 SDK 扩展方案

**文档 ID**：`onto/category-taxonomy-sdk`

> **类型**：规范 + 实施方案（对齐 `ads_categories` 平台分类）  
> **同步路径**：`dazi docs sync` → `资源/docs/onto/本体分类规划与SDK扩展方案.md`  
> **前置依据**：[本体命名规范](./本体命名规范_物理表Cube与对象.md)、[本体规划指南](./本体规划指南.md)

---

## 1. 目标

将 **规划语义分类**（规划表「类别/分类」列）与 **`ads_categories` 平台分类**（侧栏分组、桥表挂载）打通，支持 init 脚本幂等注册。

> **术语**：下文 **平台标准分类** = 侧栏 `ads_categories` 使用的标准中文名（如「维度表」「总览分析」）。SDK 中的 `category_347`、`ensure_347` 为历史参数/方法名，**含义即平台标准分类**，与文档编号无关。

**约束**：本体规划阶段分类 **全部平级**（挂空间默认根下，不建多层树）。

---

## 2. 两类分类，一套语言

| 维度 | 规划语义分类 | ads_categories 平台分类 |
|------|-------------|------------------------|
| 作用 | 规划自检、命名约束 | 侧栏展示、资源分组 |
| 对齐 | 平台 `category_name` **=** 平台标准分类中文名 | 禁止自定义别名 |

---

## 3. 平台标准分类字典（6 类资源）

### 3.1 物理表（`category_kind=dataspace_table`）

| 平台分类类别 | 前缀 | 平台分类名 |
|----------|------|------------|
| 时间维 | `dim_date` | 时间维 |
| 维度表 | `dim_` | 维度表 |
| 事实表 | `fact_` | 事实表 |
| 桥表 | `bridge_` | 桥表 |
| 映射表 | `map_` | 映射表 |
| 配置表 | `cfg_` | 配置表 |
| 汇总表 | `agg_` | 汇总表 |
| 临时表 | `tmp_` | 临时表 |

### 3.2 Cube（`category_kind=cube`）

| 平台分类类别 | 平台分类名 |
|----------|------------|
| Process | 流程型 |
| Subject | 主体型 |
| Comparison | 对比型 |
| Snapshot | 快照型 |

> 时间增强不单独建 Cube（命名规范 §4.2），不设平台分类。

### 3.3 本体对象（`category_kind=ontology_object_type`）

| 平台分类 | 平台分类名 |
|----------|------------|
| Master | 主数据 |
| Transaction | 事务 |
| Analytical | 分析 |
| Reference | 参考 |
| Configuration | 配置 |

### 3.4 表间关系（`category_kind=relation`，平台扩展）

| 关系类别 | 平台分类名 |
|----------|------------|
| 时间关联 | 时间关联 |
| 主数据关联 | 主数据关联 |
| 层级自关联 | 层级自关联 |
| 预实关联 | 预实关联 |
| 桥接关联 | 桥接关联 |

### 3.5 本体链接（`category_kind=ontology_link_type`，平台扩展）

| 链接类别 | 平台分类名 |
|----------|------------|
| 归属/包含 | 归属关系 |
| 分析归因 | 分析归因 |
| 层级/结构 | 层级关系 |
| 对比/映射 | 对比关系 |

### 3.6 本体函数（`category_kind=ontology_function`，平台扩展）

| 函数类别 | 平台分类名 |
|----------|------------|
| 总览 | 总览分析 |
| 趋势 | 趋势分析 |
| 结构 | 结构分析 |
| 预实 | 预实分析 |
| 组织 | 组织分析 |

---

## 4. SDK 设计

### 4.1 模块

```python
s.categories                    # CategoryManager
s.categories.apply_registry(CATEGORY_REGISTRY)
s.categories.ensure_347(kind="table", category="维度表")
s.categories.assign_table("维度表", "dim_account")
s.categories.auto_assign_tables(["dim_account", "fact_gl_journal_entry"])
```

### 4.2 分类挂载脚本 `*_category_mount.py`

**方式 A — 批量**（推荐，类灌数）：独立 `setup/*_category_mount.py` 顶部 `CATEGORY_REGISTRY` 与规划 **附录 B** 对齐；在 **init + seed + 全部函数 publish 之后** 执行：

```python
cat_counts = s.categories.apply_registry(CATEGORY_REGISTRY, skip_missing=True)
```

**方式 B — 内联**（P2）：各注册 API 支持 `category_347=`，注册后即时挂载（与方式 A 幂等可并存）：

```python
s.tables.register_with_meta("dim_product", ..., category_347="维度表")
s.register_cube("SalesCube", ..., category_347="流程型")
s.onto.define_object_type("Product", "产品", category_347="主数据")
s.tables.add_relationship(..., category_347="时间关联")
s.onto.define_link_type(..., category_347="归属关系")
s.onto.register_function("sales.fn.get_summary", adapter, category_347="总览分析")
```

函数类资源若 init 未 `register_function`，批量方式须 `skip_missing=True`。

---

## 5. 规划与 init 约定

| 产出 | 位置 | 说明 |
| ---- | ---- | ---- |
| 规划附录 B | `plans/<主题>.md` | 6 类资源分类对照表 |
| `CATEGORY_REGISTRY` | `setup/*_category_mount.py` 顶部 | 与附录 B 逐行一致 |
| 分类步骤 | 流程最后 | publish + run `*_category_mount.py` |

参考：`资源/examples/onto/销售示例/plans/`、`利润示例/plans/`、`设备运营/plans/` 各附录 B 与 `setup/*_category_mount.py`。

---

## 6. 验收标准

1. 平台侧栏分类名与平台标准分类表一致
2. `dim_*` / `fact_*` 自动归入维度表/事实表
3. init 重跑幂等，桥表不重复
4. `CATEGORY_REGISTRY` 与规划附录 B 逐行一致

---

## 7. 相关文档

| 文档 | 路径（`dazi docs sync` 后） |
| ---- | --------------------------- |
| 本体命名规范 | `资源/docs/onto/本体命名规范_物理表Cube与对象.md` |
| 本体规划指南 | `资源/docs/onto/本体规划指南.md` |
| SDK 参考 §5.6 | `资源/docs/onto/dazi_script_sdk_reference.md` |
| 脚本编写指南 | `资源/docs/onto/本体脚本编写指南.md` |

---

**变更记录**

| 日期 | 说明 |
| ---- | ---- |
| 2026-06-06 | 首版：对齐 平台分类方案 + SDK 设计 |
| 2026-06-06 | 改为 `dazi-vscode` 完整可同步正文（客户环境不依赖 `dazi/docs/`） |
