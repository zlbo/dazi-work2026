# Action Type设计文档 - 潘达油田全域生产分析

> **版本**：V1.0
> **创建日期**：2026年6月13日
> **阶段**：阶段二 - 本体设计与确认
> **引用**：《000-顶层设计.md》；《070-L5-流程动作清单.md》；《030-ObjectType设计文档.md》
> **说明**：本文档定义油田行业本体的核心Action Type，基于21条流程动作映射设计。

---

## 一、Action Type设计概述

### 1.1 设计原则

| 原则 | 说明 |
|------|------|
| **流程映射** | 基于L5流程动作清单映射Action Type |
| **业务场景驱动** | 覆盖生产/措施/设备/安全/开发5类场景 |
| **参数完整性** | 定义输入输出参数 |
| **命名规范** | 采用PascalCase命名规范 |

### 1.2 Action Type分类体系

| 业务场景 | Action Type数量 | 说明 |
|---------|----------------|------|
| 生产管理 | 6 | 调整举升、变更状态、计划措施等 |
| 措施作业 | 5 | 压裂、酸化、修井等 |
| 设备管理 | 4 | 维护安排、故障记录、设备监控等 |
| 安全环保 | 3 | 安全检查、环保监测、事故处理等 |
| 开发规划 | 3 | 开发方案、注水分配、产量预测等 |
| **合计** | **21** | - |

---

## 二、核心Action Type详细设计

### 2.1 生产管理类Action Type

#### AdjustLifting（调整举升）

| 属性 | 内容 |
|------|------|
| **display_name** | 调整举升 |
| **description** | 调整油井举升参数 |
| **category** | 生产管理 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| well_code | string | 32 | NOT NULL | 井号 |
| lifting_type_code | string | 20 | - | 举升方式编码 |
| stroke_length | decimal | (5,2) | - | 冲程长度(m) |
| stroke_frequency | decimal | (5,2) | - | 冲次(次/min) |
| pump_depth | decimal | (6,2) | - | 泵挂深度(m) |
| adjustment_reason | string | 200 | - | 调整原因 |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| adjustment_time | datetime | - | 调整时间 |

---

#### ChangeStatus（变更状态）

| 属性 | 内容 |
|------|------|
| **display_name** | 变更状态 |
| **description** | 变更井的生产状态 |
| **category** | 生产管理 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| well_code | string | 32 | NOT NULL | 井号 |
| new_status_code | string | 20 | NOT NULL | 新状态编码 |
| status_reason | string | 200 | - | 状态变更原因 |
| operator_id | string | 32 | - | 操作人ID |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| status_change_time | datetime | - | 状态变更时间 |

---

#### PlanStimulation（计划措施）

| 属性 | 内容 |
|------|------|
| **display_name** | 计划措施 |
| **description** | 制定增产措施计划 |
| **category** | 生产管理 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| well_code | string | 32 | NOT NULL | 井号 |
| stimulation_type_code | string | 20 | NOT NULL | 措施类型编码 |
| plan_date | date | - | NOT NULL | 计划日期 |
| budget_amount | decimal | (12,2) | - | 预算金额 |
| expected_oil_increase | decimal | (10,2) | - | 预期增油量(t) |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| plan_id | string | 64 | 计划编号 |

---

#### RecordProduction（记录产量）

| 属性 | 内容 |
|------|------|
| **display_name** | 记录产量 |
| **description** | 记录井的日产量数据 |
| **category** | 生产管理 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| well_code | string | 32 | NOT NULL | 井号 |
| production_date | date | - | NOT NULL | 生产日期 |
| daily_oil_production | decimal | (10,2) | - | 日产油量(t) |
| daily_liquid_production | decimal | (10,2) | - | 日产液量(m³) |
| daily_gas_production | decimal | (12,2) | - | 日产气量(m³) |
| water_cut | decimal | (5,2) | - | 含水率(%) |
| recorder_id | string | 32 | - | 记录人ID |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| production_id | string | 64 | 产量记录ID |

---

#### RecordInjection（记录注入）

| 属性 | 内容 |
|------|------|
| **display_name** | 记录注入 |
| **description** | 记录注水井的注入数据 |
| **category** | 生产管理 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| well_code | string | 32 | NOT NULL | 井号 |
| injection_date | date | - | NOT NULL | 注入日期 |
| daily_water_injection | decimal | (10,2) | - | 日注水量(m³) |
| injection_pressure | decimal | (5,2) | - | 注入压力(MPa) |
| recorder_id | string | 32 | - | 记录人ID |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| injection_id | string | 64 | 注入记录ID |

---

#### MonitorProduction（监控生产）

| 属性 | 内容 |
|------|------|
| **display_name** | 监控生产 |
| **description** | 监控井的生产状态，触发预警 |
| **category** | 生产管理 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| well_code | string | 32 | NOT NULL | 井号 |
| monitoring_duration | int | - | - | 监控时长(分钟) |
| threshold_config | json | - | - | 阈值配置(JSON) |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| alert_count | int | - | 预警数量 |
| alert_details | json | - | 预警详情(JSON) |

---

### 2.2 措施作业类Action Type

#### ExecuteFracturing（执行压裂）

| 属性 | 内容 |
|------|------|
| **display_name** | 执行压裂 |
| **description** | 执行压裂增产作业 |
| **category** | 措施作业 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| well_code | string | 32 | NOT NULL | 井号 |
| construction_date | date | - | NOT NULL | 施工日期 |
| fracturing_fluid_type | string | 50 | - | 压裂液类型 |
| proppant_amount | decimal | (10,2) | - | 支撑剂用量(t) |
| max_pressure | decimal | (5,2) | - | 施工压力(MPa) |
| target_zone | string | 100 | - | 目的层位 |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| construction_id | string | 64 | 施工记录ID |

---

#### ExecuteAcidizing（执行酸化）

| 属性 | 内容 |
|------|------|
| **display_name** | 执行酸化 |
| **description** | 执行酸化增产作业 |
| **category** | 措施作业 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| well_code | string | 32 | NOT NULL | 井号 |
| construction_date | date | - | NOT NULL | 施工日期 |
| acid_type | string | 50 | - | 酸液类型 |
| acid_volume | decimal | (10,2) | - | 酸液用量(m³) |
| injection_rate | decimal | (6,2) | - | 注入速度(m³/h) |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| construction_id | string | 64 | 施工记录ID |

---

#### ExecuteWorkover（执行修井）

| 属性 | 内容 |
|------|------|
| **display_name** | 执行修井 |
| **description** | 执行修井作业 |
| **category** | 措施作业 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| well_code | string | 32 | NOT NULL | 井号 |
| workover_date | date | - | NOT NULL | 修井日期 |
| workover_reason | string | 200 | - | 修井原因 |
| workover_type | string | 50 | - | 修井类型 |
| estimated_duration | int | - | 预计时长(小时) |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| workover_id | string | 64 | 修井记录ID |

---

#### ExecutePerforation（执行射孔）

| 属性 | 内容 |
|------|------|
| **display_name** | 执行射孔 |
| **description** | 执行射孔完井作业 |
| **category** | 措施作业 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| well_code | string | 32 | NOT NULL | 井号 |
| perforation_date | date | - | NOT NULL | 射孔日期 |
| perforation_type | string | 50 | - | 射孔类型 |
| hole_density | int | - | 孔密(孔/m) |
| perforation_zones | json | - | 射孔层段(JSON) |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| perforation_id | string | 64 | 射孔记录ID |

---

#### ExecuteProfileControl（执行调剖）

| 属性 | 内容 |
|------|------|
| **display_name** | 执行调剖 |
| **description** | 执行调剖措施 |
| **category** | 措施作业 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| well_code | string | 32 | NOT NULL | 井号 |
| profile_control_date | date | - | NOT NULL | 调剖日期 |
| agent_type | string | 50 | - | 调剖剂类型 |
| agent_amount | decimal | (10,2) | - | 调剖剂用量(t) |
| injection_zones | json | - | 注入层段(JSON) |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| profile_control_id | string | 64 | 调剖记录ID |

---

### 2.3 设备管理类Action Type

#### ScheduleMaintenance（安排维护）

| 属性 | 内容 |
|------|------|
| **display_name** | 安排维护 |
| **description** | 安排设备维护计划 |
| **category** | 设备管理 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| equipment_code | string | 32 | NOT NULL | 设备编号 |
| maintenance_date | date | - | NOT NULL | 维护日期 |
| maintenance_type | string | 50 | - | 维护类型 |
| estimated_cost | decimal | (12,2) | - | 预计费用(元) |
| maintenance_content | string | 500 | - | 维护内容 |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| maintenance_plan_id | string | 64 | 维护计划ID |

---

#### RecordMaintenance（记录维护）

| 属性 | 内容 |
|------|------|
| **display_name** | 记录维护 |
| **description** | 记录设备维护执行情况 |
| **category** | 设备管理 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| equipment_code | string | 32 | NOT NULL | 设备编号 |
| maintenance_date | date | - | NOT NULL | 维护日期 |
| maintenance_type | string | 50 | - | 维护类型 |
| actual_cost | decimal | (12,2) | - | 实际费用(元) |
| maintenance_result | string | 200 | - | 维护结果 |
| operator_id | string | 32 | - | 操作人ID |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| maintenance_record_id | string | 64 | 维护记录ID |

---

#### RecordFailure（记录故障）

| 属性 | 内容 |
|------|------|
| **display_name** | 记录故障 |
| **description** | 记录设备故障 |
| **category** | 设备管理 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| equipment_code | string | 32 | NOT NULL | 设备编号 |
| failure_time | datetime | - | NOT NULL | 故障时间 |
| failure_type | string | 50 | - | 故障类型 |
| failure_description | string | 500 | - | 故障描述 |
| impact_scope | string | 200 | - | 影响范围 |
| reporter_id | string | 32 | - | 报告人ID |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| failure_record_id | string | 64 | 故障记录ID |

---

#### MonitorEquipment（监控设备）

| 属性 | 内容 |
|------|------|
| **display_name** | 监控设备 |
| **description** | 监控设备运行状态 |
| **category** | 设备管理 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| equipment_code | string | 32 | NOT NULL | 设备编号 |
| monitoring_duration | int | - | 监控时长(分钟) |
| parameter_thresholds | json | - | 参数阈值(JSON) |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| equipment_status | string | 20 | 设备状态 |
| abnormal_parameters | json | - | 异常参数(JSON) |

---

### 2.4 安全环保类Action Type

#### ExecuteSafetyCheck（执行安全检查）

| 属性 | 内容 |
|------|------|
| **display_name** | 执行安全检查 |
| **description** | 执行安全检查 |
| **category** | 安全环保 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| well_code | string | 32 | - | 井号（可选） |
| check_date | date | - | NOT NULL | 检查日期 |
| check_type | string | 50 | - | 检查类型 |
| check_items | json | - | 检查项目(JSON) |
| inspector_id | string | 32 | - | 检查人ID |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| safety_check_id | string | 64 | 安全检查ID |
| hazard_count | int | - | 隐患数量 |

---

#### ExecuteEnvMonitoring（执行环保监测）

| 属性 | 内容 |
|------|------|
| **display_name** | 执行环保监测 |
| **description** | 执行环保监测 |
| **category** | 安全环保 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| monitoring_point | string | 100 | NOT NULL | 监测点 |
| monitoring_date | date | - | NOT NULL | 监测日期 |
| monitoring_items | json | - | 监测项目(JSON) |
| monitor_id | string | 32 | - | 监测人ID |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| env_monitoring_id | string | 64 | 环保监测ID |
| exceeded_count | int | - | 超标数量 |

---

#### RecordIncident（记录事故）

| 属性 | 内容 |
|------|------|
| **display_name** | 记录事故 |
| **description** | 记录安全环保事故 |
| **category** | 安全环保 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| incident_time | datetime | - | NOT NULL | 事故时间 |
| incident_type | string | 50 | - | 事故类型 |
| incident_location | string | 200 | - | 事故地点 |
| incident_description | string | 500 | - | 事故描述 |
| casualty_count | int | - | 伤亡人数 |
| economic_loss | decimal | (14,2) | - | 经济损失(元) |
| reporter_id | string | 32 | - | 报告人ID |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| incident_record_id | string | 64 | 事故记录ID |

---

### 2.5 开发规划类Action Type

#### CreateDevelopmentPlan（创建开发方案）

| 属性 | 内容 |
|------|------|
| **display_name** | 创建开发方案 |
| **description** | 创建油藏开发方案 |
| **category** | 开发规划 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| plan_name | string | 100 | NOT NULL | 方案名称 |
| reservoir_code | string | 32 | NOT NULL | 油藏编码 |
| plan_date | date | - | NOT NULL | 编制日期 |
| development_method | string | 50 | - | 开发方式 |
| recovery_rate_target | decimal | (5,2) | - | 采收率目标(%) |
| plan_content | text | - | - | 方案内容 |
| creator_id | string | 32 | - | 创建人ID |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| plan_id | string | 64 | 方案编号 |

---

#### CreateInjectionAllocation（创建注水分配）

| 属性 | 内容 |
|------|------|
| **display_name** | 创建注水分配 |
| **description** | 创建注水井组水量分配方案 |
| **category** | 开发规划 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| allocation_name | string | 100 | NOT NULL | 分配方案名称 |
| block_code | string | 32 | NOT NULL | 区块编码 |
| effective_date | date | - | NOT NULL | 生效日期 |
| total_allocation | decimal | (10,2) | - | 总配水量(m³/d) |
| well_allocations | json | - | 单井配水(JSON) |
| creator_id | string | 32 | - | 创建人ID |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| allocation_id | string | 64 | 分配方案ID |

---

#### CalculateProductionForecast（计算产量预测）

| 属性 | 内容 |
|------|------|
| **display_name** | 计算产量预测 |
| **description** | 基于历史数据计算产量预测 |
| **category** | 开发规划 |

**输入参数**：

| 参数名 | 数据类型 | 长度 | 约束 | 说明 |
|--------|---------|------|------|------|
| well_code | string | 32 | NOT NULL | 井号 |
| forecast_period | int | - | NOT NULL | 预测周期(月) |
| decline_type | string | 20 | - | 递减类型 |
| historical_data_start | date | - | 历史数据开始日期 |
| calculation_method | string | 50 | - | 计算方法 |

**输出参数**：

| 参数名 | 数据类型 | 长度 | 说明 |
|--------|---------|------|------|
| result_code | string | 20 | 执行结果编码 |
| result_message | string | 200 | 执行结果说明 |
| forecast_id | string | 64 | 预测ID |
| forecast_data | json | - | 预测数据(JSON) |

---

## 三、Action Type分类汇总

### 3.1 分类统计

| 业务场景 | Action Type名称 |
|---------|----------------|
| **生产管理** | AdjustLifting, ChangeStatus, PlanStimulation, RecordProduction, RecordInjection, MonitorProduction |
| **措施作业** | ExecuteFracturing, ExecuteAcidizing, ExecuteWorkover, ExecutePerforation, ExecuteProfileControl |
| **设备管理** | ScheduleMaintenance, RecordMaintenance, RecordFailure, MonitorEquipment |
| **安全环保** | ExecuteSafetyCheck, ExecuteEnvMonitoring, RecordIncident |
| **开发规划** | CreateDevelopmentPlan, CreateInjectionAllocation, CalculateProductionForecast |
| **合计** | **21个** |

---

## 四、Action Type设计质量检查

| 检查项 | 方法论要求 | 实际完成 | 结果 |
|--------|----------|---------|------|
| Action Type数量 | ≥20个 | 21个 | ✅ |
| 业务场景覆盖 | 生产/措施/设备/安全/开发 | 全部覆盖 | ✅ |
| 参数定义完整性 | 输入输出参数完整 | 完整 | ✅ |
| 数据类型规范 | 合理选择数据类型 | 规范 | ✅ |
| 与Object Type关联 | 可关联到核心Object Type | 已关联 | ✅ |

---

## 五、文件说明

**文件编号**：050  
**文件名称**：Action Type设计文档.md  
**版本**：V1.0  
**创建日期**：2026年6月13日  
**适用范围**：潘达油田全域生产分析项目阶段二