#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Beancount Bot Wrapper - 加载 patch 后启动
"""
import sys
import os

# 先加载 patch
print("=> Loading transaction patch...")
import transaction_patch

# 然后启动 beancount_bot
print("=> Starting Beancount bot...")
from beancount_bot.__main__ import main

if __name__ == '__main__':
    main()
