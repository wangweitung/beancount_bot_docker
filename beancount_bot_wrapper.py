#!/usr/bin/env python3
"""
Beancount Bot Wrapper - 使用交易日期保存到对应年月文件夹
"""
import sys
import os
import re
import datetime
from typing import Tuple, List

print("=> [PATCH] Loading wrapper with monkey patch...")

# 先导入 beancount_bot，然后进行 monkey patch
from beancount_bot import transaction
from beancount_bot import util

# 保存原始类
_OriginalTransactionManager = transaction.TransactionManager

class TransactionManager(_OriginalTransactionManager):
    """
    重写 TransactionManager，使用交易日期而不是当前日期来生成文件路径
    """

    def _get_transaction_date_from_entry(self, entry_str: str) -> Tuple[int, int]:
        """从交易文本中提取日期 (YYYY-MM-DD)"""
        match = re.match(r'^(\d{4})-(\d{2})-(\d{2})', entry_str.strip())
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            print(f"[PATCH] Extracted date: {year}-{month:02d}")
            return year, month
        now = datetime.datetime.now()
        print(f"[PATCH] Using current date: {now.year}-{now.month:02d}")
        return now.year, now.month

    def _format_path_with_date(self, path_template: str, year: int, month: int) -> str:
        """使用指定的年月格式化路径模板"""
        result = path_template.format(
            year=str(year),
            month=f"{month:02d}",
            date=f"{year}-{month:02d}"
        )
        print(f"[PATCH] Path: {path_template} -> {result}")
        return result

    def create(self, entry_str: str, tags: List[str] = None) -> str:
        """创建交易，使用交易日期生成文件路径"""
        print(f"[PATCH] create() called for: {entry_str[:50]}...")
        
        # 获取交易日期
        year, month = self._get_transaction_date_from_entry(entry_str)
        
        # 使用交易日期格式化路径
        beancount_file = self._format_path_with_date(self.beancount_file, year, month)
        
        # 确保目录存在
        dir_path = os.path.dirname(beancount_file)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"[PATCH] Created directory: {dir_path}")
        
        # 添加标签
        if tags is None:
            tags = []
        
        # 临时修改路径，调用父类方法
        original_path = self.beancount_file
        self.beancount_file = beancount_file
        
        try:
            result = _OriginalTransactionManager.create(self, entry_str, tags)
            util.logger.info(f"[PATCH] Saved to: {beancount_file} (date: {year}-{month:02d})")
            return result
        finally:
            self.beancount_file = original_path


# 替换原始类
transaction.TransactionManager = TransactionManager
print(f"[PATCH] TransactionManager patched: {transaction.TransactionManager}")

# 确保其他引用也更新
from beancount_bot import bot
if hasattr(bot, 'TransactionManager'):
    bot.TransactionManager = TransactionManager

# 现在启动 beancount_bot
print("=> Starting Beancount bot...")
from beancount_bot.__main__ import main
main()
