# -*- coding: utf-8 -*-
"""
Patch for beancount_bot - Use transaction date instead of current date for file path
在 beancount_bot 加载时自动应用
"""
import re
import datetime
from typing import Tuple, List

print("[PATCH] Loading transaction_patch.py...")

# 保存原始模块引用
import beancount_bot.transaction as _orig_transaction
import beancount_bot.util as _util

print(f"[PATCH] Original TransactionManager: {_orig_transaction.TransactionManager}")

# 保存原始类
_OriginalTransactionManager = _orig_transaction.TransactionManager


class TransactionManager(_OriginalTransactionManager):
    """
    重写 TransactionManager，使用交易日期而不是当前日期来生成文件路径
    """

    def _get_transaction_date_from_entry(self, entry_str: str) -> Tuple[int, int]:
        """
        从交易文本中提取日期 (YYYY-MM-DD)
        返回: (year, month)
        """
        match = re.match(r'^(\d{4})-(\d{2})-(\d{2})', entry_str.strip())
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            print(f"[PATCH] Extracted date from entry: {year}-{month:02d}")
            return year, month
        # 如果无法解析，使用当前日期
        now = datetime.datetime.now()
        print(f"[PATCH] Failed to extract date, using current: {now.year}-{now.month:02d}")
        return now.year, now.month

    def _format_path_with_date(self, path_template: str, year: int, month: int) -> str:
        """
        使用指定的年月格式化路径模板
        """
        result = path_template.format(
            year=str(year),
            month=f"{month:02d}",
            date=f"{year}-{month:02d}"
        )
        print(f"[PATCH] Formatted path: {path_template} -> {result}")
        return result

    def create(self, entry_str: str, tags: List[str] = None) -> str:
        """
        创建交易，使用交易日期生成文件路径
        """
        print(f"[PATCH] TransactionManager.create() called")
        print(f"[PATCH] Entry: {entry_str[:50]}...")
        
        # 获取交易日期
        year, month = self._get_transaction_date_from_entry(entry_str)
        
        # 使用交易日期格式化路径
        beancount_file = self._format_path_with_date(self.beancount_file, year, month)
        
        # 添加标签（使用交易年月）
        if tags is None:
            tags = []
        
        # 调用父类的 create 方法，但传入格式化后的路径
        # 注意：这里需要临时修改 self.beancount_file
        original_path = self.beancount_file
        self.beancount_file = beancount_file
        
        try:
            result = _OriginalTransactionManager.create(self, entry_str, tags)
            _util.logger.info(f"交易已保存到: {beancount_file} (使用交易日期 {year}-{month:02d})")
            return result
        finally:
            self.beancount_file = original_path


# 替换原始类
_orig_transaction.TransactionManager = TransactionManager

print(f"[PATCH] New TransactionManager: {_orig_transaction.TransactionManager}")

# 确保其他引用也更新
import beancount_bot.bot as _bot
if hasattr(_bot, 'TransactionManager'):
    _bot.TransactionManager = TransactionManager
    print("[PATCH] Updated _bot.TransactionManager")

print("[PATCH] TransactionManager patched successfully!")
