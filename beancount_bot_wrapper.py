#!/usr/bin/env python3
"""
Beancount Bot Wrapper - 使用交易日期保存到对应年月文件夹
通过直接修改 transaction.py 文件来实现
"""
import sys
import os

print("=> [PATCH] Starting beancount_bot with patched transaction module...")

# 获取 beancount_bot 的安装路径
import beancount_bot
beancount_bot_path = os.path.dirname(beancount_bot.__file__)
transaction_path = os.path.join(beancount_bot_path, 'transaction.py')

print(f"=> [PATCH] beancount_bot path: {beancount_bot_path}")
print(f"=> [PATCH] transaction.py path: {transaction_path}")

# 读取原始 transaction.py
with open(transaction_path, 'r', encoding='utf-8') as f:
    original_content = f.read()

# 创建备份（如果不存在）
backup_path = transaction_path + '.original'
if not os.path.exists(backup_path):
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
    print(f"=> [PATCH] Created backup: {backup_path}")

# 检查是否已经打过补丁
if '# PATCHED_BY_WRAPPER' in original_content:
    print("=> [PATCH] transaction.py already patched, skipping...")
else:
    # 在文件末尾添加补丁代码（在 TransactionManager 类定义之后）
    patch_code = '''

# PATCHED_BY_WRAPPER
# Auto-patched by beancount_bot_wrapper to use transaction date for file paths
import re
import datetime

# 保存原始 create 方法
_original_create = TransactionManager.create

def _patched_create(self, entry_str: str, tags: list = None, **kwargs) -> str:
    """使用交易日期生成文件路径"""
    # 从交易文本中提取日期
    match = re.match(r'^(\\d{4})-(\\d{2})-(\\d{2})', entry_str.strip())
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
    else:
        now = datetime.datetime.now()
        year, month = now.year, now.month
    
    # 使用交易日期格式化路径
    beancount_file = self.beancount_file.format(
        year=str(year),
        month=f"{month:02d}",
        date=f"{year}-{month:02d}"
    )
    
    # 确保目录存在
    dir_path = os.path.dirname(beancount_file)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        print(f"[PATCH] Created directory: {dir_path}")
    
    # 临时修改路径
    original_path = self.beancount_file
    self.beancount_file = beancount_file
    
    try:
        result = _original_create(self, entry_str, tags, **kwargs)
        print(f"[PATCH] Saved to: {beancount_file} (date: {year}-{month:02d})")
        return result
    finally:
        self.beancount_file = original_path

# 替换 create 方法
TransactionManager.create = _patched_create
'''
    # 追加到文件末尾
    new_content = original_content + patch_code
    
    with open(transaction_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"=> [PATCH] Patched transaction.py")

# 现在启动 beancount_bot
print("=> Starting beancount_bot...")
os.system("beancount_bot --config $BEANCOUNT_BOT_CONFIG")
