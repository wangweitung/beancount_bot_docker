#!/usr/bin/env python3
"""
Beancount Bot Wrapper - 加载 transaction patch 后启动
"""
import sys
import os

# 确保当前目录在路径中
sys.path.insert(0, '/app')

# 先加载 patch
print("=> Loading transaction patch...")
import transaction_patch

# 启动 beancount_bot
print("=> Starting Beancount bot...")
os.system("beancount_bot --config $BEANCOUNT_BOT_CONFIG")
