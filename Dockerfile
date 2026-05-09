FROM python:3.9-slim

WORKDIR /app
ADD requirements.txt /app

# 安装编译依赖，然后安装 Python 包，最后清理
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev libxml2-dev libxslt1-dev git && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove gcc libc6-dev && \
    rm -rf /var/lib/apt/lists/*

VOLUME ["/config", "/bean"]

ENV BEANCOUNT_BOT_CONFIG=/config/beancount_bot.yml
ENV PYTHONPATH=/config:/config/modules:/app

# Add beancount_bot wrapper for transaction date patch
ADD beancount_bot_wrapper.py /app/beancount_bot_wrapper.py

# Copy config files (will be overridden by volume mount if exists)
ADD config/ /config/

ADD docker-entrypoint.sh /app
RUN chmod +x /app/docker-entrypoint.sh

CMD ["/app/docker-entrypoint.sh"]
