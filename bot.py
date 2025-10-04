import logging
import os
import asyncio
import subprocess
import tempfile
import discord
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger('discord').setLevel(logging.INFO)

load_dotenv()
print("Starting bot...", flush=True)
TOKEN = os.getenv('DISCORD_TOKEN', '')
if not TOKEN:
    raise SystemExit("DISCORD_TOKEN not found in .env")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logging.info(f"Bot ready - logged in as {client.user}")
    logging.info("Watching for .stl, .step, .stp")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if not message.attachments:
        return

    for a in message.attachments:
        name = a.filename.lower()
        logging.info(f"Received file: {name}")

        if not name.endswith((".stl", ".step", ".stp")):
            continue

        tmpdir = tempfile.mkdtemp(prefix="job_", dir="/app/output")
        in_path = os.path.join(tmpdir, a.filename)
        await a.save(in_path)

        stl_path = in_path
        if name.endswith((".step", ".stp", ".iges", ".igs")):
            stl_path = os.path.join(tmpdir, os.path.splitext(a.filename)[0] + ".stl")
            logging.info(f"Converting {name} to STL...")
            subprocess.run(["python3", "/app/convert.py", in_path, stl_path], check=True)

        png_path = os.path.join(tmpdir, os.path.splitext(os.path.basename(stl_path))[0] + ".gif")
        logging.info("Rendering 3D preview...")
        subprocess.run(["python3", "/app/render_gif.py", stl_path, png_path], check=True)

        logging.info("Sending preview...")
        await message.channel.send(file=discord.File(png_path), reference=message)


if __name__ == "__main__":
    client.run(TOKEN)