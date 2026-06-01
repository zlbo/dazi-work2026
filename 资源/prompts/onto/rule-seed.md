# 提示词：规则种子脚本

**提示词 ID**: `onto/rule-seed`  
**场景**: 编写规则种子脚本

---

请为以下业务规则编写搭子规则种子脚本：

## 规则需求

{{rule_description}}

## 种子脚本模板

```python
def main(params: dict, s=None) -> dict:
    """
    规则种子：[规则集名称]
    写入 ads_ontology_rules 表。
    """
    rules = [
        {
            "code": "rule_001",           # 规则唯一编码
            "name": "规则名称",            # 人类可读名称
            "rule_set": "my_rule_set",    # 规则集（相关规则分组）
            "expression": "x > 0",        # 规则表达式（可选）
            "description": "规则描述",
            "metadata": {}
        },
    ]
    
    result = s.ontology_rules.upsert(rules)
    return {"upserted": len(rules), "result": result}
```

执行命令（v3；**勿用** `dazi-onto`）：
```powershell
.\scripts\dazi.ps1 onto rule run-seed --space <space-id> --stem <seed_file_stem>
```
详见提示词 `onto/script-publish-run`。
