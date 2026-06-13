# setup

初始化（`ontology_init`）与灌数（`seed`）脚本；**最后**执行 `profit01_category_mount.py`（平台分类 + 本体域成员）。

**域成员补挂**（已 init/seed/函数 publish 但域树灰色时）：

```powershell
# 在 dazi-work 根目录
.\项目\DAZI_TEST\本体\ontos\利润分析01\setup\profit01_remount_domain.ps1
```

发布示例：`dazi onto script publish 项目/.../setup/<file>.py --space space__onto_engine_test --type setup|data`  
函数 publish 推荐加 `--mount-domain auto`。
