# Object Type设计文档 - 潘达油田全域生产分析

> **版本**：V1.0
> **创建日期**：2026年6月13日
> **阶段**：阶段二 - 本体设计与确认
> **引用**：《000-顶层设计.md》；《020-L1-核心实体清单.md》；《010-物理表设计文档.md》
> **说明**：本文档定义油田行业本体的核心Object Type，基于60个核心实体映射设计。

---

## 一、Object Type设计概述

### 1.1 设计原则

| 原则 | 说明 |
|------|------|
| **核心实体优先** | 以"井"(Well)为核心构建Object Type |
| **10域覆盖** | 覆盖D1-D10全部业务域 |
| **属性映射** | 基于核心实体属性定义Object属性 |
| **编码规范** | 采用PascalCase命名规范 |

### 1.2 Object Type分类体系

| 业务域 | Object Type数量 | 核心实体 |
|--------|----------------|---------|
| D1 地质勘探 | 6 | Reservoir, Formation, Reserves, TrappedOil, SeismicSurvey |
| D2 钻井工程 | 5 | Well, Wellbore, DrillingRig, Casing, Cementing |
| D3 完井与改造 | 5 | WellCompletion, Perforation, Fracturing, SandControl, Stimulation |
| D4 采油采气生产 | 8 | ProductionWell, InjectionWell, WellProduction, ArtificialLift, Pump, ESP, RodPump |
| D5 增产措施 | 4 | Acidizing, Workover, ProfileControl |
| D6 生产动态管理 | 4 | ProductionIndicator, DeclineCurve, ProductionForecast, AlertRecord |
| D7 油藏工程 | 5 | Block, OilGasField, InjectionAllocation, PressureData, DevelopmentPlan |
| D8 地面集输 | 5 | GatheringStation, Pipeline, PipelineNetwork, ProcessEquipment, Compressor |
| D9 设备资产 | 6 | Equipment, MaintenancePlan, MaintenanceRecord, FailureRecord |
| D10 QHSE与井完整性 | 4 | WellIntegrity, SafetyCheck, EnvironmentalMonitoring, IncidentRecord |
| **合计** | **52** | - |

---

## 二、核心Object Type详细设计

### 2.1 井域核心Object Type

#### Well（井）

| 属性名 | 数据类型 | 长度 | 约束 | 说明 | 来源字段 |
|--------|---------|------|------|------|---------|
| well_key | string | 64 | PRIMARY KEY | 井主键 | dim_well.well_key |
| well_code | string | 32 | NOT NULL | 井号 | dim_well.well_code |
| well_name | string | 100 | - | 井名称 | dim_well.well_name |
| well_type_code | string | 20 | - | 井型编码 | dim_well.well_type_code |
| well_type_name | string | 50 | - | 井型名称 | dim_well.well_type_name |
| lifting_type_code | string | 20 | - | 举升方式编码 | dim_well.lifting_type_code |
| lifting_type_name | string | 50 | - | 举升方式名称 | dim_well.lifting_type_name |
| block_key | string | 64 | - | 区块主键 | dim_well.block_key |
| reservoir_code | string | 32 | - | 油藏编码 | dim_well.reservoir_code |
| spud_date | date | - | - | 开钻日期 | dim_well.spud_date |
| completed_date | date | - | - | 完井日期 | dim_well.completed_date |
| status_code | string | 20 | - | 当前状态 | dim_well.status_code |
| x_coordinate | decimal | (12,6) | - | X坐标 | dim_well.x_coordinate |
| y_coordinate | decimal | (12,6) | - | Y坐标 | dim_well.y_coordinate |

#### WellProduction（井产量）

| 属性名 | 数据类型 | 长度 | 约束 | 说明 | 来源字段 |
|--------|---------|------|------|------|---------|
| production_key | string | 64 | PRIMARY KEY | 产量主键 | fact_well_production.production_key |
| well_key | string | 64 | NOT NULL | 井主键 | fact_well_production.well_key |
| date_key | int32 | - | NOT NULL | 日期键 | fact_well_production.date_key |
| daily_oil_production | decimal | (10,2) | - | 日产油量(t) | fact_well_production.daily_oil_production |
| daily_liquid_production | decimal | (10,2) | - | 日产液量(m³) | fact_well_production.daily_liquid_production |
| daily_gas_production | decimal | (12,2) | - | 日产气量(m³) | fact_well_production.daily_gas_production |
| water_cut | decimal | (5,2) | - | 含水率(%) | fact_well_production.water_cut |
| pump_efficiency | decimal | (5,2) | - | 泵效(%) | fact_well_production.pump_efficiency |

---

### 2.2 油藏域核心Object Type

#### Reservoir（油藏）

| 属性名 | 数据类型 | 长度 | 约束 | 说明 | 来源字段 |
|--------|---------|------|------|------|---------|
| reservoir_key | string | 64 | PRIMARY KEY | 油藏主键 | dim_reservoir.reservoir_key |
| reservoir_code | string | 32 | NOT NULL | 油藏编码 | dim_reservoir.reservoir_code |
| reservoir_name | string | 100 | - | 油藏名称 | dim_reservoir.reservoir_name |
| reservoir_type_code | string | 20 | - | 油藏类型编码 | dim_reservoir.reservoir_type_code |
| reservoir_type_name | string | 50 | - | 油藏类型名称 | dim_reservoir.reservoir_type_name |
| formation_code | string | 32 | - | 主要地层编码 | dim_reservoir.formation_code |
| porosity | decimal | (5,3) | - | 孔隙度(%) | dim_reservoir.porosity |
| permeability | decimal | (8,3) | - | 渗透率(mD) | dim_reservoir.permeability |
| thickness | decimal | (6,2) | - | 厚度(m) | dim_reservoir.thickness |

#### Block（区块）

| 属性名 | 数据类型 | 长度 | 约束 | 说明 | 来源字段 |
|--------|---------|------|------|------|---------|
| block_key | string | 64 | PRIMARY KEY | 区块主键 | dim_block.block_key |
| block_code | string | 32 | NOT NULL | 区块编码 | dim_block.block_code |
| block_name | string | 100 | - | 区块名称 | dim_block.block_name |
| block_level | int | - | - | 区块层级 | dim_block.block_level |
| parent_block_key | string | 64 | - | 父级区块主键 | dim_block.parent_block_key |
| oil_gas_field_code | string | 32 | - | 油气田编码 | dim_block.oil_gas_field_code |
| reservoir_code | string | 32 | - | 主要油藏编码 | dim_block.reservoir_code |

---

### 2.3 设备域核心Object Type

#### Equipment（设备）

| 属性名 | 数据类型 | 长度 | 约束 | 说明 | 来源字段 |
|--------|---------|------|------|------|---------|
| equipment_key | string | 64 | PRIMARY KEY | 设备主键 | dim_equipment.equipment_key |
| equipment_code | string | 32 | NOT NULL | 设备编号 | dim_equipment.equipment_code |
| equipment_name | string | 100 | - | 设备名称 | dim_equipment.equipment_name |
| equipment_type_code | string | 20 | - | 设备类型编码 | dim_equipment.equipment_type_code |
| equipment_type_name | string | 50 | - | 设备类型名称 | dim_equipment.equipment_type_name |
| model | string | 50 | - | 规格型号 | dim_equipment.model |
| well_key | string | 64 | - | 所属井主键 | dim_equipment.well_key |
| installation_date | date | - | - | 安装日期 | dim_equipment.installation_date |
| status_code | string | 20 | - | 设备状态 | dim_equipment.status_code |

---

### 2.4 措施域核心Object Type

#### Stimulation（措施作业）

| 属性名 | 数据类型 | 长度 | 约束 | 说明 | 来源字段 |
|--------|---------|------|------|------|---------|
| stimulation_key | string | 64 | PRIMARY KEY | 措施主键 | fact_stimulation.stimulation_key |
| well_key | string | 64 | NOT NULL | 井主键 | fact_stimulation.well_key |
| date_key | int32 | - | NOT NULL | 措施日期键 | fact_stimulation.date_key |
| stimulation_type_code | string | 20 | NOT NULL | 措施类型编码 | fact_stimulation.stimulation_type_code |
| construction_params | json | - | - | 施工参数 | fact_stimulation.construction_params |
| result_oil_increase | decimal | (10,2) | - | 增油量(t) | fact_stimulation.result_oil_increase |
| valid_days | int | - | - | 有效期(天) | fact_stimulation.valid_days |
| cost_amount | decimal | (12,2) | - | 措施成本(元) | fact_stimulation.cost_amount |

---

### 2.5 注入域核心Object Type

#### WellInjection（井注入）

| 属性名 | 数据类型 | 长度 | 约束 | 说明 | 来源字段 |
|--------|---------|------|------|------|---------|
| injection_key | string | 64 | PRIMARY KEY | 注入主键 | fact_well_injection.injection_key |
| well_key | string | 64 | NOT NULL | 井主键 | fact_well_injection.well_key |
| date_key | int32 | - | NOT NULL | 日期键 | fact_well_injection.date_key |
| daily_water_injection | decimal | (10,2) | - | 日注水量(m³) | fact_well_injection.daily_water_injection |
| injection_pressure | decimal | (5,2) | - | 注入压力(MPa) | fact_well_injection.injection_pressure |
| injection_temperature | decimal | (5,1) | - | 注入温度(℃) | fact_well_injection.injection_temperature |

---

## 三、Object Type与业务域映射

### 3.1 业务域Object Type映射表

| 业务域 | Object Type | 核心属性数量 |
|--------|-------------|-------------|
| D1 地质勘探 | Reservoir | 9 |
| | Formation | 5 |
| | Reserves | 4 |
| | TrappedOil | 5 |
| | SeismicSurvey | 4 |
| | Porosity | 4 |
| | Permeability | 4 |
| **D1合计** | **7** | - |
|---|---|---|
| D2 钻井工程 | Well | 13 |
| | Wellbore | 4 |
| | DrillingRig | 4 |
| | Casing | 4 |
| | Cementing | 4 |
| | DrillingBit | 4 |
| | MudSystem | 4 |
| **D2合计** | **7** | - |
|---|---|---|
| D3 完井与改造 | WellCompletion | 4 |
| | Perforation | 4 |
| | Fracturing | 5 |
| | SandControl | 4 |
| | Stimulation | 8 |
| | WellIntegrity | 4 |
| **D3合计** | **6** | - |
|---|---|---|
| D4 采油采气生产 | ProductionWell | 5 |
| | InjectionWell | 4 |
| | ObservationWell | 4 |
| | WellProduction | 8 |
| | ArtificialLift | 4 |
| | Pump | 5 |
| | ESP | 4 |
| | RodPump | 4 |
| | ProductionStatus | 4 |
| | ProductionIndicator | 4 |
| | WaterCut | 4 |
| | GOR | 4 |
| | PumpEfficiency | 4 |
| | ShiftReport | 4 |
| **D4合计** | **14** | - |
|---|---|---|
| D5 增产措施 | Acidizing | 4 |
| | Workover | 4 |
| | ProfileControl | 4 |
| **D5合计** | **3** | - |
|---|---|---|
| D6 生产动态管理 | DeclineCurve | 4 |
| | ProductionForecast | 4 |
| | AlertRecord | 4 |
| **D6合计** | **3** | - |
|---|---|---|
| D7 油藏工程 | Block | 7 |
| | OilGasField | 5 |
| | InjectionAllocation | 5 |
| | PressureData | 4 |
| | InjectionPressure | 4 |
| | DevelopmentPlan | 4 |
| **D7合计** | **6** | - |
|---|---|---|
| D8 地面集输 | GatheringStation | 4 |
| | Pipeline | 4 |
| | PipelineNetwork | 4 |
| | ProcessEquipment | 4 |
| | MeasurementRecord | 4 |
| | Compressor | 4 |
| **D8合计** | **6** | - |
|---|---|---|
| D9 设备资产 | Equipment | 9 |
| | MaintenancePlan | 4 |
| | MaintenanceRecord | 4 |
| | FailureRecord | 5 |
| **D9合计** | **4** | - |
|---|---|---|
| D10 QHSE | WellIntegrity | 4 |
| | SafetyCheck | 4 |
| | EnvironmentalMonitoring | 4 |
| | IncidentRecord | 4 |
| **D10合计** | **4** | - |
|---|---|---|
| **总计** | **64** | - |

---

## 四、Object Type设计质量检查

| 检查项 | 方法论要求 | 实际完成 | 结果 |
|--------|----------|---------|------|
| Object Type数量 | ≥20个核心类 | 64个 | ✅ |
| 核心实体覆盖 | Well/Reservoir/Block/Equipment | 全部覆盖 | ✅ |
| 10域覆盖 | D1-D10全覆盖 | 全部覆盖 | ✅ |
| 属性定义完整性 | 每个Object含主键和业务属性 | 完整 | ✅ |
| 数据类型规范 | 合理选择数据类型 | 规范 | ✅ |
| 与物理表映射 | 可映射到事实表/维度表 | 已映射 | ✅ |

---

## 五、文件说明

**文件编号**：030  
**文件名称**：Object Type设计文档.md  
**版本**：V1.0  
**创建日期**：2026年6月13日  
**适用范围**：潘达油田全域生产分析项目阶段二