SELECT 
  `space__misc_01`.`cost_report_08`.`基本信息_组织` AS organization,
  `space__misc_01`.`cost_report_08`.`基本信息_年度` AS year,
  `space__misc_01`.`cost_report_08`.`基本信息_月度` AS month,
  `space__misc_01`.`cost_report_08`.`基本信息_项目` AS project,
  `space__misc_01`.`cost_report_08`.`成本项_管理费` AS management_fee,
  `space__misc_01`.`cost_report_08`.`成本项_间接成本` AS indirect_cost,
  `space__misc_01`.`cost_report_08`.`成本项_税金` AS tax,
  `space__misc_01`.`cost_report_08`.`成本项_直接成本_安全文明施工费` AS safety_construction_fee,
  `space__misc_01`.`cost_report_08`.`成本项_直接成本_材料` AS materials,
  `space__misc_01`.`cost_report_08`.`成本项_直接成本_机械` AS machinery,
  `space__misc_01`.`cost_report_08`.`成本项_直接成本_劳务分包` AS labor_subcontract,
  `space__misc_01`.`cost_report_08`.`成本项_直接成本_专业分包` AS professional_subcontract,
  `space__misc_01`.`cost_report_08`.`成本项_直接成本_直接成本` AS direct_cost_total,
  `space__misc_01`.`cost_report_08`.`成本比较_实际成本` AS actual_cost,
  `space__misc_01`.`cost_report_08`.`成本比较_目标成本` AS target_cost,
  `space__misc_01`.`cost_report_08`.`成本比较_实目比` AS actual_target_ratio
FROM `space__misc_01`.`cost_report_08`