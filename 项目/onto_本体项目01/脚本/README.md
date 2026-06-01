# 脚本

产品销售本体与员工培训本体 Python 脚本（空间：`space__0519`）。

## 目录结构

```text
脚本/
├── main.py
├── setup/
│   ├── sales_ontology_init.py   # 产品销售建表、Cube、本体
│   ├── sales_seed_data.py       # 产品销售演示数据
│   ├── training_ontology_init.py # 员工培训建表、Cube、本体
│   └── training_seed_data.py     # 员工培训演示数据
└── functions/
    ├── sales_fn_get_summary.py
    ├── sales_fn_top_products.py
    ├── sales_fn_yoy_analysis.py
    ├── sales_fn_mom_analysis.py
    ├── sales_fn_region_breakdown.py
    ├── sales_fn_channel_mix.py
    ├── sales_fn_customer_segmentation.py
    ├── training_fn_get_summary.py
    ├── training_fn_employee_training.py
    ├── training_fn_course_effectiveness.py
    ├── training_fn_department_training.py
    ├── training_fn_trainer_performance.py
    ├── training_fn_training_trend.py
    └── training_fn_need_training.py
```

## 执行顺序

### 产品销售本体

1. 发布并运行初始化（普通 data_script，不注册函数）：

```bash
dazi-onto script publish 项目/onto_本体项目01/脚本/setup/sales_ontology_init.py --space space__0519
```

2. 灌入演示数据：

```bash
dazi-onto script publish 项目/onto_本体项目01/脚本/setup/sales_seed_data.py --space space__0519
```

3. 发布本体函数（示例）：

```bash
dazi-onto script publish 项目/onto_本体项目01/脚本/functions/sales_fn_get_summary.py \
  --space space__0519 --register-function-id sales.fn.get_summary

dazi-onto function run sales.fn.get_summary --space space__0519 \
  --params '{"start_date":"2025-01-01","end_date":"2026-06-30"}'
```

### 员工培训本体

1. 发布并运行初始化（普通 data_script，不注册函数）：

```bash
dazi-onto script publish 项目/onto_本体项目01/脚本/setup/training_ontology_init.py --space space__0519
```

2. 灌入演示数据：

```bash
dazi-onto script publish 项目/onto_本体项目01/脚本/setup/training_seed_data.py --space space__0519
```

3. 发布本体函数（示例）：

```bash
dazi-onto script publish 项目/onto_本体项目01/脚本/functions/training_fn_get_summary.py \
  --space space__0519 --register-function-id training.fn.get_summary

dazi-onto function run training.fn.get_summary --space space__0519 \
  --params '{"start_date":"2025-01-01","end_date":"2026-06-30"}'
```

## 函数 ID 对照

### 产品销售本体

| 文件 | function_id |
|------|-------------|
| sales_fn_get_summary.py | sales.fn.get_summary |
| sales_fn_top_products.py | sales.fn.top_products |
| sales_fn_yoy_analysis.py | sales.fn.yoy_analysis |
| sales_fn_mom_analysis.py | sales.fn.mom_analysis |
| sales_fn_region_breakdown.py | sales.fn.region_breakdown |
| sales_fn_channel_mix.py | sales.fn.channel_mix |
| sales_fn_customer_segmentation.py | sales.fn.customer_segmentation |

### 员工培训本体

| 文件 | function_id |
|------|-------------|
| training_fn_get_summary.py | training.fn.get_summary |
| training_fn_employee_training.py | training.fn.employee_training |
| training_fn_course_effectiveness.py | training.fn.course_effectiveness |
| training_fn_department_training.py | training.fn.department_training |
| training_fn_trainer_performance.py | training.fn.trainer_performance |
| training_fn_training_trend.py | training.fn.training_trend |
| training_fn_need_training.py | training.fn.need_training |

## 规划文档

- 产品销售本体：`规划/产品销售本体规划方案.md`
- 员工培训本体：`规划/员工培训本体规划方案.md`