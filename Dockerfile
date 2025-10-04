FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y --no-install-recommends freecad python3 python3-pip xvfb \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/usr/lib/freecad/lib
ENV MPLBACKEND=Agg
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir discord.py numpy numpy-stl matplotlib python-dotenv
RUN mkdir -p /app/output && chmod 777 /app/output

CMD ["python3","/app/bot.py"]
