#!/usr/bin/env python3
"""检查 beancount_bot 的结构"""
import subprocess
import sys

# 安装 beancount_bot
subprocess.check_call([sys.executable, "-m", "pip", "install", "beancount_bot==1.2.1", "-q"])

# 导入并检查结构
from beancount_bot import transaction
import inspect

print("TransactionManager 类:")
print(f"  文件: {inspect.getfile(transaction.TransactionManager)}")
print(f"  方法: {[m for m in dir(transaction.TransactionManager) if not m.startswith('_')]}")

# 检查 create 方法
if hasattr(transaction.TransactionManager, 'create'):
    print(f"\ncreate 方法签名:")
    print(inspect.signature(transaction.TransactionManager.create))
    print(f"\ncreate 方法源码:")
    print(inspect.getsource(transaction.TransactionManager.create))
