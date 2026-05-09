# Beancount Bot 交易日期补丁

这个补丁修改了 beancount_bot 的行为，使其使用**交易日期**而不是**当前日期**来生成文件路径。

## 修改内容

### 1. transaction_patch.py
- 重写 `TransactionManager.create()` 方法
- 从交易文本中提取日期 (YYYY-MM-DD)
- 使用交易日期格式化 `beancount_file` 路径

### 2. Dockerfile
- 添加 `transaction_patch.py` 到镜像
- 添加 `beancount_bot_wrapper.py` 作为启动包装器
- 设置 `PYTHONPATH` 包含 `/app`

### 3. docker-entrypoint.sh
- 使用 `beancount_bot_wrapper.py` 启动，确保 patch 被加载

### 4. beancount_bot_wrapper.py
- 先加载 `transaction_patch.py`
- 然后启动 beancount_bot

## 使用方法

### 本地构建
```bash
cd D:\Redmi-DS918\beancount_bot_docker
docker build -t your-username/beancount_bot_docker:latest .
```

### 推送到 Docker Hub

1. 在 GitHub 仓库设置中添加 Secrets：
   - `DOCKER_USERNAME`: 你的 Docker Hub 用户名
   - `DOCKER_PASSWORD`: 你的 Docker Hub 密码或访问令牌

2. 创建并发布 Release：
   - 进入 GitHub 仓库 → Releases → Draft a new release
   - 创建新标签（如 `v1.2.2`）
   - 发布 Release

3. GitHub Actions 会自动构建并推送到 Docker Hub

### 使用新镜像

修改你的 `docker-compose.yml`：

```yaml
services:
  beancount_bot_docker:
    container_name: bean-wwd-bot
    image: your-username/beancount_bot_docker:latest  # 使用你的镜像
    volumes:
      - ./wwd:/bean
      - ./config:/config
    environment:
      - PYTHONPATH=/config/modules
      - TZ=Asia/Shanghai
    restart: always
```

## 效果

配置 `beancount_file: '/bean/{year}-{month}月/{month}月交易.bean'` 后：

- 交易日期 `2026-08-05` → 保存到 `/bean/2026-08月/08月交易.bean`
- 交易日期 `2026-05-09` → 保存到 `/bean/2026-05月/05月交易.bean`

不再需要使用 `format.py` 后处理脚本！
