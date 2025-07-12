# Pre-commit Hooks 设置指南

本项目使用 pre-commit hooks 来自动运行代码质量检查工具，确保代码提交的一致性和质量。

## 安装 Pre-commit

### 1. 全局安装 pre-commit

```bash
# 使用 pip 安装
pip install pre-commit

# 或使用 conda 安装
conda install -c conda-forge pre-commit

# 或使用 homebrew (macOS)
brew install pre-commit
```

### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 安装 pre-commit hooks
pre-commit install

# 手动运行所有文件的检查（可选）
pre-commit run --all-files
```

### 3. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
pnpm install

# 安装 pre-commit hooks
pre-commit install

# 手动运行所有文件的检查（可选）
pre-commit run --all-files
```

## 配置的检查工具

### 后端 (Python)

1. **通用检查**：

   - 移除尾随空格
   - 确保文件以换行符结尾
   - 检查 YAML、JSON、TOML 文件格式
   - 检查大文件和合并冲突

2. **代码格式化**：

   - **Black**: 代码格式化
   - **isort**: 导入语句排序

3. **代码质量**：
   - **Ruff**: 快速 Python linter
   - **MyPy**: 类型检查
   - **Bandit**: 安全性检查
   - **Pydocstyle**: 文档字符串风格检查

### 前端 (TypeScript/JavaScript)

1. **通用检查**：

   - 移除尾随空格
   - 确保文件以换行符结尾
   - 检查 YAML、JSON 文件格式
   - 检查大文件和合并冲突

2. **代码格式化**：

   - **Prettier**: 代码格式化（包含 Tailwind CSS 插件）

3. **代码质量**：
   - **ESLint**: JavaScript/TypeScript 代码检查
   - **TypeScript**: 类型检查
   - **Next.js Lint**: Next.js 特定的检查

## 使用方法

### 自动运行

安装后，每次运行 `git commit` 时，pre-commit hooks 会自动运行。如果检查失败，提交会被阻止。

### 手动运行

```bash
# 运行所有 hooks
pre-commit run --all-files

# 运行特定的 hook
pre-commit run black
pre-commit run eslint
pre-commit run prettier

# 只检查已暂存的文件
pre-commit run
```

### 跳过 hooks（不推荐）

```bash
# 跳过所有 hooks
git commit --no-verify

# 跳过特定的 hook
SKIP=mypy git commit -m "commit message"
```

## 常见问题

### 1. Black 格式化冲突

如果 Black 修改了您的代码，您需要重新添加文件到暂存区：

```bash
git add .
git commit -m "your message"
```

### 2. TypeScript 类型错误

确保所有 TypeScript 错误都已修复：

```bash
cd frontend
pnpm run type-check
```

### 3. ESLint 错误

运行 ESLint 自动修复：

```bash
cd frontend
pnpm run lint --fix
```

### 4. 依赖问题

如果遇到依赖问题，重新安装：

```bash
# 后端
cd backend
poetry install

# 前端
cd frontend
pnpm install
```

## 更新 Pre-commit Hooks

```bash
# 更新 hooks 到最新版本
pre-commit autoupdate

# 清理缓存
pre-commit clean
```

## 集成到 CI/CD

Pre-commit hooks 也可以在 CI/CD 中运行：

```yaml
# GitHub Actions 示例
- name: Run pre-commit
  uses: pre-commit/action@v3.0.0
```

## 自定义配置

您可以在 `.pre-commit-config.yaml` 文件中自定义配置：

- 添加或移除 hooks
- 修改 hooks 的参数
- 设置文件过滤器
- 配置跳过的文件

## 团队使用建议

1. **强制使用**: 确保所有团队成员都安装了 pre-commit hooks
2. **定期更新**: 定期运行 `pre-commit autoupdate` 更新工具版本
3. **统一配置**: 保持 `.pre-commit-config.yaml` 在版本控制中
4. **文档化**: 将特殊的配置和跳过规则记录在文档中

## 性能优化

1. **并行运行**: Pre-commit 默认并行运行多个 hooks
2. **缓存**: Pre-commit 会缓存环境以提高速度
3. **增量检查**: 只检查修改的文件，而不是整个代码库

通过使用 pre-commit hooks，我们确保每次提交的代码都符合项目的质量标准，减少了代码审查的时间，并提高了代码库的整体质量。
