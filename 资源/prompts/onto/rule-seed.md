# 提示词：规则种子脚本

**提示词 ID**: `onto/rule-seed`  
**场景**: 编写规则种子脚本

---

请为以下业务规则编写搭子规则种子脚本：

## 规则需求

{{rule_description}}

## 种子脚本模板

建议将种子脚本保存到 `项目/<业务名>/本体/ontos/<实现名>/setup/<stem>_seed_rules.py`（与同实现的 init/seed 脚本并列）。  
`space_id` 取自 `ontos/<实现名>/README.md`。

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

发布与执行（v3；**勿用** `dazi-onto`）：

```powershell
dazi onto script publish 项目/<业务名>/本体/ontos/<实现名>/setup/<stem>_seed_rules.py --space <space-id> --type data
dazi onto rule run-seed --space <space-id> --stem <seed_file_stem>
```

详见提示词 `onto/script-publish-run`。
