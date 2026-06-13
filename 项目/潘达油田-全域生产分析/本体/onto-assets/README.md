# onto-assets

从服务端缓存的本体资源（侧栏 Onto 点击或右键「拉取」写入）。

| 子目录 | 内容 |
| --- | --- |
| `objects/` | 本体对象类型 JSON |
| `functions/` | 函数定义 JSON + 函数脚本 `.py` |
| `actions/` | 活动定义 JSON + 脚本 `.py` |
| `rules/` | 规则定义 JSON |

**规则**：本地已存在同名文件时，点击不会重复下载；右键「拉取」会强制覆盖。

脚本**真理源**在 `本体/ontos/<实现名>/setup/`、`functions/`；本目录为平台副本与运维入口。
