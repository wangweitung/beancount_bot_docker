#!/usr/bin/env python3
"""
Beancount Bot Wrapper - 加载 transaction patch 后启动
"""
import sys
import os

# 确保当前目录在路径中
sys.path.insert(0, '/app')

# 先加载 patch（在导入 beancount_bot 之前）
print("=> Loading transaction patch...")
import transaction_patch

# 现在导入并启动 beancount_bot
print("=> Starting Beancount bot...")

# 使用 exec 启动，确保 patch 已经生效
os.system("beancount_bot --config $BEANCOUNT_BOT_CONFIG")
