import os
from bot import data, download_dir
from pyrogram.types import Message
from .ffmpeg_utils import encode, get_thumbnail, get_duration, get_width_height

def on_task_complete():
    del data[0]
    if len(data) > 0:
      add_task(data[0])

def add_task(message: Message):
    try:
      msg = message.reply_text("```Download ediyorum...```", quote=True)
      filepath = message.download(file_name=download_dir)
      msg.edit("```Video dönüştürülüyor...```")
      new_file = encode(filepath)
      if new_file:
        msg.edit("```Video Encoded, getting metadata...```")
        duration = get_duration(new_file)
        thumb = get_thumbnail(new_file, download_dir, duration / 4)
        width, height = get_width_height(new_file)
        msg.edit("```Upload ediyorum...```")
        message.reply_video(new_file, quote=True, supports_streaming=True, thumb=thumb, duration=duration, width=width, height=height)
        os.remove(new_file)
        os.remove(thumb)
        msg.edit("```Video dönüştürüldü to x265```")
      else:
        msg.edit("```Bir şey yanlış gitti. Gönderdiğin dosyanın HEVC formatında olduğundan emin ol.```")
        os.remove(filepath)
    except Exception as e:
      msg.edit(f"```{e}```")
    on_task_complete()
