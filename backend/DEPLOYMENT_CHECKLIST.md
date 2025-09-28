# F1 Web 项目部署前检查清单

## 📋 部署前必须检查的项目

### 1. 🗃️ 数据库迁移一致性检查

**问题**: 模型定义与迁移文件不匹配，导致VPS部署时表结构不完整

**检查步骤**:
```bash
# 在backend目录下运行
DATABASE_URL=postgresql://f1_user:f1_password@localhost:5432/f1_web python scripts/validate_migrations.py
```

**期望结果**:
```
✅ env.py已导入所有模型！
✅ 模型与数据库结构完全一致！
🎉 所有检查通过！模型与迁移完全一致。
```

### 2. 📦 模型导入检查

**问题**: `alembic/env.py` 未导入所有模型，导致某些表在迁移时被遗漏

**检查项目**:
- [ ] 确保 `alembic/env.py` 导入了 `app/models/__init__.py` 中 `__all__` 列表的所有模型
- [ ] 特别检查积分榜相关模型: `DriverStanding`, `ConstructorStanding`
- [ ] 检查其他数据模型: `QualifyingResult`, `SprintResult`, `DriverSeason`

**当前导入状态** (✅ 已修复):
```python
from app.models.base import Base
from app.models.season import Season
from app.models.circuit import Circuit
from app.models.race import Race
from app.models.driver import Driver
from app.models.constructor import Constructor
from app.models.result import Result
from app.models.driver_season import DriverSeason
from app.models.qualifying_result import QualifyingResult
from app.models.sprint_result import SprintResult
from app.models.standings import DriverStanding, ConstructorStanding
```

### 3. 🔧 环境配置检查

**检查项目**:
- [ ] `.env` 文件包含所有必要的环境变量
- [ ] `DATABASE_URL` 格式正确
- [ ] VPS和本地环境的数据库连接信息对应正确

### 4. 📝 迁移文件检查

**检查步骤**:
```bash
# 检查迁移历史
poetry run alembic history

# 检查当前版本
poetry run alembic current

# 检查是否有未应用的迁移
poetry run alembic show head
```

### 5. 🧪 数据一致性检查

**部署后验证**:
```bash
# 检查关键表的记录数
sudo -u postgres psql -d f1_web_db -c "
SELECT 'circuits' as table_name, COUNT(*) as count FROM circuits
UNION ALL SELECT 'constructors', COUNT(*) FROM constructors
UNION ALL SELECT 'drivers', COUNT(*) FROM drivers
UNION ALL SELECT 'races', COUNT(*) FROM races
UNION ALL SELECT 'results', COUNT(*) FROM results
UNION ALL SELECT 'seasons', COUNT(*) FROM seasons
UNION ALL SELECT 'constructor_standings', COUNT(*) FROM constructor_standings
UNION ALL SELECT 'driver_standings', COUNT(*) FROM driver_standings;"
```

### 6. 🌐 API功能验证

**测试关键端点**:
```bash
# 测试基础数据
curl -s 'https://your-domain.com/api/v1/seasons/'
curl -s 'https://your-domain.com/api/v1/drivers/?page=1&size=5'

# 测试积分榜功能
curl -s 'https://your-domain.com/api/v1/standings/constructors?year=2024'
curl -s 'https://your-domain.com/api/v1/standings/drivers?year=2024'

# 测试健康检查
curl -s 'https://your-domain.com/health'
```

## 🚨 常见问题及解决方案

### 问题1: position_text字段缺失
**症状**: 导入数据时出现 `column "position_text" does not exist` 错误
**原因**: env.py未导入积分榜模型
**解决**: 检查并修复env.py的模型导入

### 问题2: 迁移版本不一致
**症状**: VPS和本地的表结构不同，但迁移版本相同
**原因**: 迁移执行不完整或有错误
**解决**: 手动修复表结构或重新执行迁移

### 问题3: 新模型字段遗漏
**症状**: 新增字段在本地有效，VPS无效
**原因**: 模型导入不完整
**解决**: 运行验证脚本检查模型一致性

## 📋 部署流程建议

1. **开发阶段**: 每次修改模型后运行验证脚本
2. **提交前**: 确保验证脚本通过
3. **部署前**: 再次运行验证脚本确认
4. **部署后**: 立即验证API和数据完整性
5. **定期检查**: 定期运行验证脚本确保持续一致性

## 🛠️ 工具使用

### 验证脚本
```bash
# 完整验证
DATABASE_URL=your_db_url python scripts/validate_migrations.py

# 手动检查模型一致性
DATABASE_URL=your_db_url poetry run alembic revision --autogenerate -m "test"
# 检查生成的文件是否为空迁移（只包含pass）
```

### 迁移管理
```bash
# 生成新迁移
poetry run alembic revision --autogenerate -m "描述"

# 应用迁移
poetry run alembic upgrade head

# 回退迁移
poetry run alembic downgrade -1

# 查看迁移历史
poetry run alembic history
```

---

> **重要提示**: 每次部署前必须运行验证脚本，确保模型与迁移的完全一致性！