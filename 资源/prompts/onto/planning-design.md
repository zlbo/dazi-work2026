# 本体规划设计（TRAE / 智能体）



**文档 ID**: `onto/planning-design`  

**场景**: 新建本体实现、撰写 `plans/` 规划、能力评估（**默认任务模式**）  

**前置**: 已打开本体实现单元；`README.md` / `快速启动_*.md` 中有 `space_id`



---



## 0. 任务边界（强制）



本提示词用于 **规划阶段**，产出仅为 **`plans/<主题>.md`**（及自检附录）。



| 允许 | 禁止（未获用户明确要求「快速 demo」前） |

| ---- | ---------------------------------------- |

| 阅读 `资源/examples/onto/<示例>/plans/*.md` **学结构** | 复制 `资源/examples/onto/**/setup/*.py` 到本项目 |

| 阅读 `本体规划指南.md`、`本体命名规范_*.md` | 复制 `项目/*/本体/ontos/*` 整目录到其他实现 |

| 在 `plans/` **独立撰写**业务方案 | 把示例 `plans/*.md` **全文**另存为 `plans/` |

| 对照侧栏 **数据资源** 了解现网表/Cube | `dazi onto script publish` / 写 `setup/`、`functions/` |



**用户说「创建/设计本体方案」** → 先规划，**不是**先复制 init。



---



## 1. 开始前读取



1. `项目/<业务>/本体/ontos/<实现名>/README.md` — **space_id**

2. `快速启动_<实现名>.md` — §0 任务模式、§2 示例参照表

3. `dazi docs sync` 后：`资源/docs/onto/本体规划指南.md`

4. **`dazi examples sync` 后**：`资源/examples/onto/index.json` + **至少一个**示例的 `README.md` + `plans/*.md`



```powershell

dazi doctor

dazi auth whoami

dazi examples sync

dazi examples onto list

dazi examples onto suggest 利润 GL

dazi examples onto show profit --plan   # 可选：输出规划全文

dazi onto space get <space-id>   # 可选：现网资产

```



---



## 2. 业务域路由（只读参照）



完整索引：`资源/examples/onto/index.json`（`dazi examples onto list`）。下表为常用路由（规划正文均在各示例 **`plans/`** 下）：



| 用户意图关键词 | 对照示例目录 | 规划正文（plans/） |

| -------------- | ------------ | ------------------ |

| 销售、订单、产品、渠道、SKU | `销售示例/` | `规划示例_产品销售本体规划方案.md` |

| 利润、科目、预算、GL、成本中心、预实 | `利润示例/` | `规划示例_利润分析本体方案.md` |

| 设备、OEE、停机、维保、能耗、工厂 | `设备运营/` | `化工设备运营分析本体方案.md` |



示例是 **参照答案**，须结合本实现 **重写**，并写 **「与参照示例的差异说明」** 章节。



---



## 3. 规划方法（业务世界 → 三层）



**顺序**：对象类型 + 链接（业务语言）→ 反推物理表 + 表间关系 → Cube 读模型 → 函数清单。



每层须 **独立成章**（见规划指南标准结构）：



| 章节 | 必填要点 |

| ---- | -------- |

| 业务场景 | 域边界、分析问题、空间约束 |

| 物理层 | `dim_date` + `fact_*` 含 `date_key`；表/列 **显示名+说明** |

| 表间关系 | 从事实到维表；`join_keys`；与本体链接对照 |

| **Cube 层** | 每 Cube：类别、事实源、维度、度量、派生度量、支撑对象 |

| 本体层 | 对象 `code`、分类、bind_source、属性、链接 |

| 函数 | function_id、参数、返回值、test_arguments |

| 差异说明 | 与所选示例的业务/表/Cube/对象差异 |

| 附录 B | CATEGORY_REGISTRY 对照（平台分类） |



---



## 4. 产出路径



```

项目/<业务>/本体/ontos/<实现名>/plans/<主题>.md

```



定稿前勾选 [规划完整性自检清单](资源/docs/onto/本体规划指南.md)（含 Cube 层、6a–6e 平台分类、**6f 本体域成员**）。



规划阶段 **不** 创建或发布 `setup/`、`functions/` 脚本。



---



## 5. 反模式（视为不合格）



- `plans/` 为空即开始写 init

- 表名/Cube/对象与示例 **逐字相同** 且无差异说明

- 利润域任务却使用销售域 `fact_sales_order_line` 等且无业务论证

- 复制潘达石化或其他 `项目/` 下历史实现充数

- 规划缺 **Cube 独立章节**（仅表+对象+函数）

- 只读 `docs/onto/` 旧路径而不打开 `examples/onto/*/plans/` 正文



---



## 6. 进入实施



规划定稿且用户确认后，切换提示词 **`onto/script-publish-run`**，按 `plans/` 实现 `setup/`、`functions/`。



实施顺序：**init → seed → 发布全部函数 → `*_category_mount.py`**（平台分类，附录 B）→ **同脚本末尾 `s.domain.apply_registry`**（本体域成员；域 code = 快速启动 §1）。可选：各 publish 带 `--register-platform-category` 与 category_mount 幂等并存。



---



## 7. 相关文档



- `onto/本体规划指南.md`

- `资源/examples/onto/README.md`（完整示例总览）

- `资源/examples/onto/index.json`（示例索引 · `dazi examples onto suggest`）

- `onto/本体命名规范_物理表Cube与对象.md`

- `onto/本体分类规划与SDK扩展方案.md`

