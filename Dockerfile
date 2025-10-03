# Dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y --no-install-recommends freecad python3 python3-pip xvfb \
 && rm -rf /var/lib/apt/lists/*

# FreeCAD’s Python libs live here on Ubuntu
ENV PYTHONPATH=/usr/lib/freecad/lib
ENV MPLBACKEND=Agg
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir discord.py numpy numpy-stl matplotlib python-dotenv
RUN mkdir -p /app/output

# Run the Discord bot under Xvfb
CMD ["python3","/app/bot.py"]
