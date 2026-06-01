# 本体规则（Rule）管理

**文档 ID**: `onto/rule-guide`

## 规则概念

规则（Rule）存储在 `ads_ontology_rules` 表，通过种子脚本写入，通常用于：
- 数据校验规则
- 业务约束条件
- 权限规则集

## 列出规则

```bash
.\scripts\dazi.ps1 onto rule list --space <space-id>

# 按规则集过滤
.\scripts\dazi.ps1 onto rule list --space <space-id> --rule-set finance_rules
```

## 执行规则种子

```bash
.\scripts\dazi.ps1 onto rule run-seed --space <space-id> --stem cw_001_rules_seed
```

## 种子脚本示例

```python
def main(params: dict, s) -> dict:
    rules = [
        {
            "code": "fin_001",
            "name": "余额不能为负",
            "rule_set": "finance_rules",
            "expression": "balance >= 0",
        }
    ]
    s.ontology_rules.upsert(rules)
    return {"count": len(rules)}
```

## 删除规则

```bash
# 删除单条
.\scripts\dazi.ps1 onto rule delete fin_001 --space <space-id>

# 按规则集批量删除（先 dry-run）
.\scripts\dazi.ps1 onto rule delete-all --space <space-id> --rule-set old_rules --dry-run
.\scripts\dazi.ps1 onto rule delete-all --space <space-id> --rule-set old_rules --yes
```
