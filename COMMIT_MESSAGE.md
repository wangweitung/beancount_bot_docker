# 提交说明

## 修改目标
使 beancount_bot 使用**交易日期**而不是**当前日期**来生成文件路径。

## 修改文件

### 新增文件
1. `transaction_patch.py` - 重写 TransactionManager 类
2. `beancount_bot_wrapper.py` - 启动包装器，确保 patch 被加载
3. `PATCH_README.md` - 补丁说明文档

### 修改文件
1. `Dockerfile` - 使用 python:3.9-slim，添加 patch 文件
2. `docker-entrypoint.sh` - 使用 wrapper 启动
3. `.github/workflows/docker-publish.yml` - 更新到最新 action 版本

## 修复记录

### v1.2.2-2
- 修复：使用 `os.system()` 调用 beancount_bot 命令行，而非导入 __main__

### v1.2.2-1
- 修复：使用 python:3.9-slim 替代 alpine 解决编译问题

## 发布步骤

1. 提交并推送代码到 GitHub
2. 创建 Release，GitHub Actions 会自动构建并推送
