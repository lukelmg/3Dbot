FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y --no-install-recommends freecad python3 python3-pip xvfb libegl1 libgl1-mesa-glx libgles2-mesa \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/usr/lib/freecad/lib
ENV MPLBACKEND=Agg
ENV PYTHONUNBUFFERED=1
ENV PYOPENGL_PLATFORM=egl

WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir discord.py numpy numpy-stl python-dotenv pyrender trimesh imageio
RUN mkdir -p /app/output && chmod 777 /app/output

CMD ["python3","/app/bot.py"]
