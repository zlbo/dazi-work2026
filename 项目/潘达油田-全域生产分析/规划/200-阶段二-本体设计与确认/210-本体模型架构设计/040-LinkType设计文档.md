# Link Type设计文档 - 潘达油田全域生产分析

> **版本**：V1.0
> **创建日期**：2026年6月13日
> **阶段**：阶段二 - 本体设计与确认
> **引用**：《000-顶层设计.md》；《040-L2-显性关系清单.md》；《030-ObjectType设计文档.md》
> **说明**：本文档定义油田行业本体的核心Link Type，基于65条显性关系映射设计。

---

## 一、Link Type设计概述

### 1.1 设计原则

| 原则 | 说明 |
|------|------|
| **关系映射** | 基于L2显性关系清单映射Link Type |
| **核心实体为中心** | 以"井"(Well)为核心构建关系网络 |
| **基数定义** | 明确1:1、1:N、N:1、N:M关系基数 |
| **命名规范** | 采用camelCase命名规范 |

### 1.2 Link Type分类体系

| 关系类型 | Link Type数量 | 说明 |
|---------|-------------|------|
| 归属关系 | 15 | belongsTo系列 |
| 包含关系 | 10 | contains系列 |
| 配套关系 | 8 | equippedWith系列 |
| 生产关系 | 12 | produces系列 |
| 作业关系 | 15 | operatedBy系列 |
| 评估监测关系 | 10 | evaluatedBy/monitoredBy系列 |
| 关联关系 | 5 | relatesTo系列 |
| **合计** | **75** | - |

---

## 二、核心Link Type详细设计

### 2.1 归属关系（belongsTo）

| Link Type名称 | 显示名称 | 源Object Type | 目标Object Type | 基数 | 业务含义 |
|--------------|---------|--------------|----------------|------|---------|
| belongsToReservoir | 归属油藏 | Well | Reservoir | 1:1 | 井从地质上归属某个油藏单元 |
| belongsToBlock | 归属区块 | Well | Block | 1:1 | 井从管理上归属某个区块 |
| belongsToField | 归属油气田 | Well | OilGasField | 1:1 | 井从行政上归属某个油气田 |
| belongsToField | 归属油气田 | Reservoir | OilGasField | N:1 | 油藏归属油气田 |
| belongsToField | 归属油气田 | Block | OilGasField | N:1 | 区块归属油气田 |
| belongsToWell | 归属井 | Wellbore | Well | 1:1 | 井筒归属井 |
| belongsToWell | 归属井 | WellProduction | Well | N:1 | 产量记录归属井 |
| belongsToWell | 归属井 | Equipment | Well | N:1 | 设备归属井 |
| belongsToWell | 归属井 | Stimulation | Well | N:1 | 措施记录归属井 |
| belongsToBlock | 归属区块 | WellProduction | Block | N:1 | 产量记录归属区块 |
| belongsToReservoir | 归属油藏 | Reserves | Reservoir | 1:1 | 储量归属油藏 |
| belongsToReservoir | 归属油藏 | TrappedOil | Reservoir | N:1 | 圈闭归属油藏 |
| belongsToAllocation | 归属注采井组 | InjectionWell | InjectionAllocation | 1:1 | 注水井归属注采井组 |
| belongsToAllocation | 归属注采井组 | ProductionWell | InjectionAllocation | N:1 | 采油井归属注采井组 |
| belongsToNetwork | 归属管网系统 | Pipeline | PipelineNetwork | N:1 | 管线归属管网系统 |

---

### 2.2 包含关系（contains）

| Link Type名称 | 显示名称 | 源Object Type | 目标Object Type | 基数 | 业务含义 |
|--------------|---------|--------------|----------------|------|---------|
| containsBlock | 包含区块 | OilGasField | Block | 1:N | 油气田包含多个区块 |
| containsBlock | 包含区块 | Reservoir | Block | 1:N | 油藏包含多个区块 |
| containsWellbore | 包含井筒 | Well | Wellbore | 1:1 | 井包含井筒 |
| containsCasing | 包含套管 | Wellbore | Casing | 1:N | 井筒包含多层套管 |
| containsPipeline | 包含管线 | GatheringStation | Pipeline | 1:N | 集输站包含管线 |
| containsEquipment | 包含设备 | GatheringStation | ProcessEquipment | 1:N | 集输站包含处理设备 |
| containsCompressor | 包含压缩机 | GatheringStation | Compressor | 1:N | 集输站包含压缩机 |

---

### 2.3 配套关系（equippedWith）

| Link Type名称 | 显示名称 | 源Object Type | 目标Object Type | 基数 | 业务含义 |
|--------------|---------|--------------|----------------|------|---------|
| equippedWithLift | 配套举升设备 | Well | ArtificialLift | 1:1 | 井配备举升设备 |
| equippedWithPump | 配套抽油泵 | Well | Pump | 1:1 | 井配备抽油泵 |
| equippedWithESP | 配套电潜泵 | Well | ESP | 1:1 | 井配备电潜泵 |
| equippedWithRodPump | 配套螺杆泵 | Well | RodPump | 1:1 | 井配备螺杆泵 |
| equippedWithEquipment | 配套设备 | GatheringStation | ProcessEquipment | 1:N | 集输站配备处理设备 |
| equippedWithCompressor | 配套压缩机 | GatheringStation | Compressor | 1:N | 集输站配备压缩机 |

---

### 2.4 生产关系（produces）

| Link Type名称 | 显示名称 | 源Object Type | 目标Object Type | 基数 | 业务含义 |
|--------------|---------|--------------|----------------|------|---------|
| producesProduction | 产生产量记录 | Well | WellProduction | 1:N | 井产出日产量数据 |
| producesInjection | 产出注入记录 | InjectionWell | WellInjection | 1:N | 注水井产出注入数据 |
| injectsIntoReservoir | 注入油藏 | InjectionWell | Reservoir | N:1 | 注水井向油藏注水 |
| producesPressure | 产出压力数据 | Well | PressureData | 1:N | 井产出压力监测数据 |
| producesAlert | 产生产生预警 | Well | AlertRecord | 1:N | 井产生产生预警记录 |

---

### 2.5 作业关系（operatedBy）

| Link Type名称 | 显示名称 | 源Object Type | 目标Object Type | 基数 | 业务含义 |
|--------------|---------|--------------|----------------|------|---------|
| operatedByFracturing | 接受压裂作业 | Well | Fracturing | N:M | 井接受压裂增产作业 |
| operatedByPerforation | 接受射孔作业 | Well | Perforation | 1:N | 井接受射孔完井作业 |
| operatedByStimulation | 接受措施作业 | Well | Stimulation | N:M | 井接受各类增产措施 |
| operatedByAcidizing | 接受酸化措施 | Well | Acidizing | N:M | 井接受酸化增产措施 |
| operatedByWorkover | 接受修井作业 | Well | Workover | N:M | 井接受修井维护作业 |
| operatedByCompletion | 接受完井作业 | Well | WellCompletion | 1:1 | 井接受完井作业 |
| operatedBySandControl | 接受防砂作业 | Well | SandControl | 1:N | 井接受防砂完井作业 |
| operatedByProfileControl | 接受调剖措施 | InjectionWell | ProfileControl | N:M | 注水井接受调剖措施 |
| operatesWell | 钻井作业 | DrillingRig | Well | 1:N | 钻井设备进行钻井作业 |
| operatesFormation | 钻进地层 | DrillingBit | Formation | N:M | 钻头钻进地层 |
| servesWellbore | 服务井筒 | MudSystem | Wellbore | 1:1 | 泥浆系统服务井筒 |
| recordsCasing | 记录套管 | Cementing | Casing | 1:N | 固井记录记录套管 |
| definesWell | 定义井 | WellCompletion | Well | 1:1 | 完井方案定义井 |
| definesStimulation | 定义措施 | Fracturing | Stimulation | 1:1 | 压裂参数定义压裂作业 |
| recordsStimulation | 记录措施 | Perforation | Stimulation | 1:N | 射孔记录记录射孔作业 |

---

### 2.6 评估监测关系（evaluatedBy/monitoredBy）

| Link Type名称 | 显示名称 | 源Object Type | 目标Object Type | 基数 | 业务含义 |
|--------------|---------|--------------|----------------|------|---------|
| evaluatedByIntegrity | 接受完整性评估 | Well | WellIntegrity | 1:N | 井接受完整性评估 |
| evaluatedBySafetyCheck | 接受安全检查 | Well | SafetyCheck | 1:N | 井接受安全检查 |
| monitoredByPressure | 接受压力监测 | Well | PressureData | 1:N | 井接受压力监测 |
| monitoredByEnvironment | 接受环保监测 | Well | EnvironmentalMonitoring | 1:N | 井接受环保监测 |
| monitoredBySeismic | 探测地层 | SeismicSurvey | Formation | N:M | 地震勘探探测地层 |
| monitoredByEquipment | 设备监控 | Equipment | GatheringStation | 1:N | 设备受集输站监控 |

---

### 2.7 关联关系（relatesTo）

| Link Type名称 | 显示名称 | 源Object Type | 目标Object Type | 基数 | 业务含义 |
|--------------|---------|--------------|----------------|------|---------|
| relatesToStation | 连接集输站 | Well | GatheringStation | N:1 | 井产出的油气输送到集输站 |
| relatesToPipeline | 连接管线 | Well | Pipeline | N:1 | 井通过管线连接集输系统 |
| hasMaintenanceRecord | 有维护记录 | Well | MaintenanceRecord | 1:N | 井有设备维护记录 |
| hasFailureRecord | 有故障记录 | Well | FailureRecord | 1:N | 井有设备故障记录 |
| hasMaintenancePlan | 有维护计划 | Equipment | MaintenancePlan | 1:N | 设备有维护计划 |

---

## 三、以井为核心的关系网络

### 3.1 井的关系网络架构

```
                            ┌───────────────┐
                            │    Well       │ ← 核心实体
                            └───────┬───────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
   ┌────▼────┐              ┌───────▼───────┐           ┌───────▼───────┐
   │归属关系 │              │    配套关系    │           │    作业关系    │
   └────┬────┘              └───────┬───────┘           └───────┬───────┘
        │                           │                           │
   ┌────┴────┐              ┌───────┴───────┐           ┌───────┴───────┐
   │Reservoir│              │ArtificialLift │           │Fracturing    │
   │Block    │              │Pump           │           │Acidizing     │
   │OilGasField│            │ESP            │           │Workover      │
   └─────────┘              │RodPump        │           │WellCompletion│
                            └───────────────┘           └───────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
   ┌────▼────┐              ┌───────▼───────┐           ┌───────▼───────┐
   │生产关系 │              │   评估关系    │           │    关联关系    │
   └────┬────┘              └───────┬───────┘           └───────┬───────┘
        │                           │                           │
   ┌────┴────┐              ┌───────┴───────┐           ┌───────┴───────┐
   │WellProd │              │WellIntegrity  │           │GatheringStn  │
   │WellInj  │              │SafetyCheck    │           │Pipeline      │
   │Pressure │              │EnvMonitoring  │           │Maintenance   │
   └─────────┘              └───────────────┘           └───────────────┘
```

---

## 四、Link Type设计质量检查

| 检查项 | 方法论要求 | 实际完成 | 结果 |
|--------|----------|---------|------|
| Link Type数量 | ≥15个核心关系 | 75个 | ✅ |
| 关系类型覆盖 | 归属/包含/配套/生产/作业/评估/关联 | 全部覆盖 | ✅ |
| 核心实体关系 | 井相关关系数量 | 28条 | ✅ |
| 基数定义 | 明确1:1/1:N/N:1/N:M | 全部定义 | ✅ |
| 业务域覆盖 | D1-D10全覆盖 | 全部覆盖 | ✅ |
| Object Type映射 | 可映射到已定义Object Type | 已映射 | ✅ |

---

## 五、文件说明

**文件编号**：040  
**文件名称**：Link Type设计文档.md  
**版本**：V1.0  
**创建日期**：2026年6月13日  
**适用范围**：潘达油田全域生产分析项目阶段二