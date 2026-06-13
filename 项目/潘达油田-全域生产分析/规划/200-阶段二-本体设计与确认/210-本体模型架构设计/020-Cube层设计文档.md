# Cube层设计文档 - 潘达油田全域生产分析

> **版本**：V1.0
> **创建日期**：2026年6月13日
> **阶段**：阶段二 - 本体设计与确认
> **引用**：《000-顶层设计.md》；《010-物理表设计文档.md》；《050-指标计算规则.md》
> **说明**：本文档定义油田行业本体数据架构的Cube层设计，包括分析维度、度量和派生度量定义。

---

## 一、Cube设计概述

### 1.1 设计原则

| 原则 | 说明 |
|------|------|
| **平台分类适配** | 根据平台要求定义主体型/流程型/快照型 |
| **维度关联** | 基于事实表与维度表的外键关系 |
| **度量聚合** | 定义SUM/AVG/COUNT等聚合方式 |
| **派生度量** | 基于基础度量计算派生指标 |

### 1.2 Cube分类体系

| Cube名称 | 平台分类 | 事实来源 | 业务定位 |
|----------|---------|---------|---------|
| WellProductionCube | 流程型 | fact_well_production | 井产量分析 |
| BlockProductionCube | 主体型 | fact_well_production | 区块产量分析 |
| WellInjectionCube | 流程型 | fact_well_injection | 井注入分析 |
| EquipmentOperationCube | 快照型 | fact_equipment_operation | 设备运行分析 |
| StimulationEffectCube | 流程型 | fact_stimulation | 措施效果分析 |

---

## 二、核心Cube设计

### 2.1 WellProductionCube（井产量分析Cube）

**平台分类**：流程型  
**事实来源**：fact_well_production  
**业务定位**：单井日产量分析、趋势跟踪、效率评估

#### 维度定义

| 维度名称 | 数据类型 | 来源表 | 说明 |
|---------|---------|-------|------|
| date_key | int32 | dim_date | 日期维度 |
| well_key | string | dim_well | 井维度 |
| well_type_code | string | dim_well | 井型维度 |
| block_key | string | dim_block | 区块维度 |
| reservoir_code | string | dim_reservoir | 油藏维度 |
| lifting_type_code | string | dim_well | 举升方式维度 |

#### 度量定义

| 度量名称 | 数据类型 | 聚合方式 | 来源字段 | 说明 |
|---------|---------|---------|---------|------|
| daily_oil_production | decimal(10,2) | SUM | daily_oil_production | 日产油量(t) |
| daily_liquid_production | decimal(10,2) | SUM | daily_liquid_production | 日产液量(m³) |
| daily_gas_production | decimal(12,2) | SUM | daily_gas_production | 日产气量(m³) |
| avg_water_cut | decimal(5,2) | AVG | water_cut | 平均含水率(%) |
| avg_pump_efficiency | decimal(5,2) | AVG | pump_efficiency | 平均泵效(%) |
| total_working_hours | decimal(8,2) | SUM | working_hours | 总工作小时(h) |
| production_days | int | COUNT | production_key | 生产天数(天) |

#### 派生度量定义

| 派生度量名称 | 计算表达式 | 说明 |
|-------------|-----------|------|
| monthly_oil_production | daily_oil_production SUM over month | 月度产油量 |
| monthly_water_production | daily_liquid_production * avg_water_cut / 100 | 月度产水量 |
| oil_ratio | daily_oil_production / daily_liquid_production * 100 | 产油率(%) |
| daily_gor | daily_gas_production / NULLIF(daily_oil_production, 0) | 日气油比 |

---

### 2.2 BlockProductionCube（区块产量分析Cube）

**平台分类**：主体型  
**事实来源**：fact_well_production  
**业务定位**：区块级产量汇总、对比分析、完成率评估

#### 维度定义

| 维度名称 | 数据类型 | 来源表 | 说明 |
|---------|---------|-------|------|
| date_key | int32 | dim_date | 日期维度 |
| block_key | string | dim_block | 区块维度 |
| block_level | int | dim_block | 区块层级 |
| oil_gas_field_code | string | dim_oil_gas_field | 油气田维度 |
| reservoir_code | string | dim_reservoir | 油藏维度 |

#### 度量定义

| 度量名称 | 数据类型 | 聚合方式 | 来源字段 | 说明 |
|---------|---------|---------|---------|------|
| total_oil_production | decimal(12,2) | SUM | daily_oil_production | 区块总产油量(t) |
| total_liquid_production | decimal(12,2) | SUM | daily_liquid_production | 区块总产液量(m³) |
| total_gas_production | decimal(14,2) | SUM | daily_gas_production | 区块总产气量(m³) |
| avg_water_cut | decimal(5,2) | AVG | water_cut | 区块平均含水率(%) |
| well_count | int | COUNT(DISTINCT well_key) | well_key | 开井数(口) |

#### 派生度量定义

| 派生度量名称 | 计算表达式 | 说明 |
|--------------|-----------|------|
| daily_per_well_oil | total_oil_production / well_count | 单井日产油(t/口) |
| block_oil_ratio | total_oil_production / total_liquid_production * 100 | 区块产油率(%) |

---

### 2.3 WellInjectionCube（井注入分析Cube）

**平台分类**：流程型  
**事实来源**：fact_well_injection  
**业务定位**：注水井注入量监控、压力分析、配注完成率

#### 维度定义

| 维度名称 | 数据类型 | 来源表 | 说明 |
|---------|---------|-------|------|
| date_key | int32 | dim_date | 日期维度 |
| well_key | string | dim_well | 注水井维度 |
| block_key | string | dim_block | 区块维度 |
| allocation_key | string | dim_allocation | 分配方案维度 |

#### 度量定义

| 度量名称 | 数据类型 | 聚合方式 | 来源字段 | 说明 |
|---------|---------|---------|---------|------|
| daily_water_injection | decimal(10,2) | SUM | daily_water_injection | 日注水量(m³) |
| avg_injection_pressure | decimal(5,2) | AVG | injection_pressure | 平均注入压力(MPa) |
| avg_injection_temperature | decimal(5,1) | AVG | injection_temperature | 平均注入温度(℃) |

#### 派生度量定义

| 派生度量名称 | 计算表达式 | 说明 |
|--------------|-----------|------|
| monthly_water_injection | daily_water_injection SUM over month | 月度注水量 |
| injection_rate | daily_water_injection / 24 | 注入速率(m³/h) |

---

### 2.4 EquipmentOperationCube（设备运行分析Cube）

**平台分类**：快照型  
**事实来源**：fact_equipment_operation  
**业务定位**：设备运行状态监控、故障率分析、能耗统计

#### 维度定义

| 维度名称 | 数据类型 | 来源表 | 说明 |
|---------|---------|-------|------|
| date_key | int32 | dim_date | 日期维度 |
| equipment_key | string | dim_equipment | 设备维度 |
| equipment_type_code | string | dim_equipment_type | 设备类型维度 |
| well_key | string | dim_well | 所属井维度 |

#### 度量定义

| 度量名称 | 数据类型 | 聚合方式 | 来源字段 | 说明 |
|---------|---------|---------|---------|------|
| running_hours | decimal(8,2) | SUM | running_hours | 运行小时(h) |
| failure_count | int | SUM | failure_count | 故障次数 |
| maintenance_count | int | SUM | maintenance_flag | 维护次数 |
| total_power_consumption | decimal(12,2) | SUM | power_consumption | 总耗电量(kWh) |

#### 派生度量定义

| 派生度量名称 | 计算表达式 | 说明 |
|--------------|-----------|------|
| availability_rate | running_hours / (24 * days) * 100 | 设备可用率(%) |
| failure_rate | failure_count / (running_hours / 1000) | 故障率(次/千小时) |
| power_per_hour | total_power_consumption / NULLIF(running_hours, 0) | 单位小时能耗(kWh/h) |

---

### 2.5 StimulationEffectCube（措施效果分析Cube）

**平台分类**：流程型  
**事实来源**：fact_stimulation  
**业务定位**：措施效果评估、成本效益分析、有效期跟踪

#### 维度定义

| 维度名称 | 数据类型 | 来源表 | 说明 |
|---------|---------|-------|------|
| date_key | int32 | dim_date | 措施日期维度 |
| well_key | string | dim_well | 井维度 |
| block_key | string | dim_block | 区块维度 |
| stimulation_type_code | string | dim_stimulation_type | 措施类型维度 |

#### 度量定义

| 度量名称 | 数据类型 | 聚合方式 | 来源字段 | 说明 |
|---------|---------|---------|---------|------|
| total_oil_increase | decimal(12,2) | SUM | result_oil_increase | 累计增油量(t) |
| avg_valid_days | decimal(6,1) | AVG | valid_days | 平均有效期(天) |
| total_cost | decimal(14,2) | SUM | cost_amount | 措施总成本(元) |
| stimulation_count | int | COUNT | stimulation_key | 措施次数 |

#### 派生度量定义

| 派生度量名称 | 计算表达式 | 说明 |
|--------------|-----------|------|
| avg_oil_increase_per_well | total_oil_increase / stimulation_count | 单井平均增油量(t) |
| cost_per_ton | total_cost / NULLIF(total_oil_increase, 0) | 吨油成本(元/t) |
| roi | (total_oil_increase * oil_price - total_cost) / total_cost * 100 | 投资回报率(%) |

---

## 三、Cube关联关系

```
                    ┌─────────────────────────────┐
                    │         dim_date            │
                    └──────────────┬──────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│WellProductionCube│    │WellInjectionCube │    │StimulationEffect │
└────────┬─────────┘    └────────┬─────────┘    │      Cube        │
         │                       │               └────────┬─────────┘
         │                       │                        │
         ▼                       ▼                        │
┌──────────────────┐    ┌──────────────────┐              │
│BlockProductionCbe│    │EquipmentOperCube │◄─────────────┘
└──────────────────┘    └──────────────────┘
```

---

## 四、Cube设计质量检查

| 检查项 | 方法论要求 | 实际完成 | 结果 |
|--------|----------|---------|------|
| Cube数量 | ≥3个 | 5个 | ✅ |
| 平台分类覆盖 | 主体型/流程型/快照型 | 全部覆盖 | ✅ |
| 维度定义完整性 | 每个Cube含时间/业务维度 | 完整 | ✅ |
| 度量定义 | 包含基础度量和派生度量 | 已定义 | ✅ |
| 聚合方式 | SUM/AVG/COUNT等 | 规范 | ✅ |
| 业务覆盖 | 产量/注入/设备/措施 | 全部覆盖 | ✅ |

---

## 五、文件说明

**文件编号**：020  
**文件名称**：Cube层设计文档.md  
**版本**：V1.0  
**创建日期**：2026年6月13日  
**适用范围**：潘达油田全域生产分析项目阶段二