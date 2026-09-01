from flask import ctx
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands

import threading

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

import sys
import traceback

def handle_exception(exc_type, exc_value, exc_traceback):
    print("\nmmmmmmmmmmmmmmmmmmmmmm\n")
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    print("\nmmmmmmmmmmmmmmmmmmmmmmm\n")
    input("\nViskas...")

sys.excepthook = handle_exception


import os

if getattr(sys, "frozen", False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

discord.opus.load_opus(
    os.path.join(BASE_PATH, "libopus-0.dll")
)



# MTU0MDQ4MzAzMDI0NDkyNTUwMA.GGYdZ3.YCjvK6N3FoIZr1e_vvVrMZ0JRcEAs2A4Afe7SU GoldFm
# MTUxNTM1Mjc0MTc4NDk3NzU5OA.GsYOVF.Nwttcri3wrKfkK1jQxYlxXAF4C0sQQ88QmEblU VLK
# yes I know you warned me before, but dont worry, these tokens are very old and not used. I am Hiding my real token in a seperate file.
Radio_URL = "https://stream.goldfm.lt/goldfm.aac"
# https://stream.goldfm.lt/goldfm.aac
# https://ice2.powerhitradio.lt/PHR_AAC
# https://stream-live.lrt.lt/radio_radijas/320k/lrt_radijas.m3u8
# https://stream-live.lrt.lt/radio_opus/320k/lrt_opus.m3u8

Audio = "audio.mp3" 

FFMPEG = r"ffmpeg.exe"


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="+", intents=intents)


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def radio(ctx):
    voice = ctx.voice_client

    if voice is None:
        await ctx.author.voice.channel.connect()
        voice = ctx.voice_client

    #stop viskam
    if voice.is_playing() or voice.is_paused():
        voice.stop()

    voice.play(
        discord.FFmpegPCMAudio(
            Radio_URL,
            executable=FFMPEG
        )
    )


@bot.command()
async def pause(ctx):
    voice = ctx.voice_client
    if voice.is_playing():
        voice.pause()

@bot.command()
async def resume(ctx):
    voice = ctx.voice_client
    if not voice.is_playing():
        voice.resume()


@bot.command()
async def audio(ctx):
    voice = ctx.voice_client

    if voice is None:
        await ctx.author.voice.channel.connect()
        voice = ctx.voice_client

    # Stop the radio or any other audio currently playing
    if voice.is_playing() or voice.is_paused():
        voice.stop()

    # Start the MP3
    voice.play(
        discord.FFmpegPCMAudio(
            Audio,
            executable=FFMPEG
        )
    )


#@bot.command()
#async def song(ctx):
#    songnameurl = "https://powerhitradio.tv3.lt/Pwr/lastSong"  #+song url
    # https://powerhitradio.tv3.lt/Pwr/lastSong
    # https://goldfm.lt/wp-content/themes/radio-gold-fm/radio/php/radio-get.php

#    response = requests.get(songnameurl) 
#   data = response.json()

#    song_name = data.get("song")
    

#    await ctx.send(song_name)




#@bot.command()
#async def song(ctx):
#    songnameurl = "https://goldfm.lt/wp-content/themes/radio-gold-fm/radio/php/radio-get.php"

#    headers = {"User-Agent": "Mozilla/5.0" }

#    response = requests.get(songnameurl, headers=headers)

#    song_name = response.text.strip()

#    await ctx.send(song_name)



STOTYS = {
    "goldfm": {
        "rawstreamas": "https://stream.goldfm.lt/goldfm.aac",
        "song_url": "https://goldfm.lt/wp-content/themes/radio-gold-fm/radio/php/radio-get.php",
        "tipas": "text"
    },

    "power": {
        "rawstreamas": "https://ice2.powerhitradio.lt/PHR_AAC",
        "song_url": "https://powerhitradio.tv3.lt/Pwr/lastSong",
        "tipas": "json",
        "jsonadresas": ["song"]
    },
    "LRT": {
        "rawstreamas": "https://stream-live.lrt.lt/radio_radijas/320k/lrt_radijas.m3u8",
        "song_url": "https://www.lrt.lt/rest-api/live/lrt-radijas",
        "tipas": "json",
        "jsonadresas": ["currentProgram", "title"]
    },
    
    "101rureggae": {
        "rawstreamas": "https://srv01.gpmradio.ru:443/stream/pro/aac/64/88?",
        "song_url": "https://101.ru/api/channel/getListServersChannel/88",
        "tipas": "json",
        "jsonadresas": ["result", 0, "titleChannel"]
   
    }, 
    "101diskotekacccr" : {
        "rawstreamas": "https://srv01.gpmradio.ru/stream/pro/aac/64/144?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiJiZmI1NTZmYmUwMDAwOWJkMzcwNDU0MzE5ZDg0NzY4YSIsIklQIjoiODQuMTUuMTg5LjIyNSIsIlVBIjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzE1MC4wLjAuMCBTYWZhcmkvNTM3LjM2IE9QUi8xMzQuMC4wLjAiLCJSZWYiOiJodHRwczovLzEwMS5ydS8iLCJ1aWRfY2hhbm5lbCI6IjE0NCIsInR5cGVfY2hhbm5lbCI6ImNoYW5uZWwiLCJ0eXBlRGV2aWNlIjoiUEMiLCJCcm93c2VyIjoiQ2hyb21lIiwiQnJvd3NlclZlcnNpb24iOiIxNTAuMC4wLjAiLCJTeXN0ZW0iOiJXaW5kb3dzIDEwIiwiZXhwIjoxNzg4MDgwMjAzfQ.FHqwTTjd2efpSS5BvD8Y-QWU-TNzFJgcphkoX-jcehU",
        "song_url": "https://101.ru/api/channel/getListServersChannel/144",
        "tipas": "json",
        "jsonadresas": ["result", 0, "titleChannel"]
    },
    "rublues": {
        "rawstreamas": "https://srv01.gpmradio.ru:443/stream/pro/aac/64/76?",
        "song_url": "https://101.ru/api/channel/getListServersChannel/76",
        "tipas": "json",
        "jsonadresas": ["result", 0, "titleChannel"]
    },
    "rudeephouse": {
        "rawstreamas": "https://srv01.gpmradio.ru/stream/trust/mp3/128/173?",
        "song_url": "https://101.ru/api/channel/getListServersChannel/173",
        "tipas": "json",
        "jsonadresas": ["result", 0, "titleChannel"]
    },
    "rutechhouse": {
        "rawstreamas": "https://srv01.gpmradio.ru/stream/trust/mp3/128/170?",
        "song_url": "https://101.ru/api/channel/getListServersChannel/170",
        "tipas": "json",
        "jsonadresas": ["result", 0, "titleChannel"]
    },
    "spinningseal": {
        "rawstreamas": "https://stream-178.surfernetwork.com/9q3ez3k3fchvv?zt=eyJhbGciOiJIUzI1NiJ9.eyJzdHJlYW0iOiI5cTNlejNrM2ZjaHZ2IiwiaG9zdCI6InN0cmVhbS0xNzguc3VyZmVybmV0d29yay5jb20iLCJydHRsIjo1LCJqdGkiOiI5MUFWSEhUSVR5MlFDakh6Z0JCLUdBIiwiaWF0IjoxNzg4MTI0MjUwLCJleHAiOjE3ODgxMjQzMTB9.c9yLAqR-Qk6_5_vUFTgZbB7WGhzpXpCX06Lqxnmz7qQ",
        "song_url": "https://content-api.zeno.fm/zenofm/gdpr",
        "tipas": "text"
    },
    "jazz" : {
        "rawstreamas": "https://srv01.gpmradio.ru:443/stream/pro/aac/64/85?",
        "song_url": "https://101.ru/api/channel/getListServersChannel/85",
        "tipas": "json",
        "jsonadresas": ["result", 0, "titleChannel"]
    }
}




@bot.command()
async def stations(ctx):
    await ctx.send("Available stations:\n" + "\n" + "+lrt\n+goldfm\n+power\n+rmfreggae\n+rureggae\n+diskotekacccr\n+rublues\n+rudeephouse\n+rutechhouse\n+seal")
@bot.command()
async def stotys(ctx):
    await ctx.send("Available stations:\n" + "\n" + "+lrt\n+goldfm\n+power\n+rmfreggae\n+rureggae\n+diskotekacccr\n+rublues\n+rudeephouse\n+rutechhouse\n+seal")


dabartine_stotis = "goldfm"

@bot.command()
async def song(ctx):
    stotis = STOTYS[dabartine_stotis]

    response = requests.get(
        stotis["song_url"],
        headers={"User-Agent": "Mozilla/5.0"}
    )
    if stotis["tipas"] == "json":
        data = response.json()

        song_name = data

        for k in stotis["jsonadresas"]:
            song_name = song_name[k]

    if stotis["tipas"] == "text":
        song_name = response.text.strip()
    await ctx.send(f"{song_name}")



@bot.command()
async def goldfm(ctx):
    global dabartine_stotis

    dabartine_stotis = "goldfm"

    voice = ctx.voice_client

    if voice is None:
        await ctx.author.voice.channel.connect()
        voice = ctx.voice_client

    if voice.is_playing() or voice.is_paused():
        voice.stop()

    voice.play(
        discord.FFmpegPCMAudio(
            STOTYS["goldfm"]["rawstreamas"],
            executable=FFMPEG
        )
    )



@bot.command()
async def power(ctx):
    global dabartine_stotis

    dabartine_stotis = "power"

    voice = ctx.voice_client

    if voice is None:
        await ctx.author.voice.channel.connect()
        voice = ctx.voice_client

    if voice.is_playing() or voice.is_paused():
        voice.stop()

    voice.play(
        discord.FFmpegPCMAudio(
            STOTYS["power"]["rawstreamas"],
            executable=FFMPEG
        )
    )


@bot.command()
async def lrt(ctx):
    global dabartine_stotis

    dabartine_stotis = "LRT"

    voice = ctx.voice_client

    if voice is None:
        await ctx.author.voice.channel.connect()
        voice = ctx.voice_client

    if voice.is_playing() or voice.is_paused():
        voice.stop()

    voice.play(
        discord.FFmpegPCMAudio(
            STOTYS["LRT"]["rawstreamas"],
            executable=FFMPEG
        )
    )



@bot.command()
async def rureggae(ctx):
    global dabartine_stotis

    dabartine_stotis = "101rureggae"

    voice = ctx.voice_client

    if voice is None:
        await ctx.author.voice.channel.connect()
        voice = ctx.voice_client

    if voice.is_playing() or voice.is_paused():
        voice.stop()

    voice.play(
        discord.FFmpegPCMAudio(
            STOTYS["101rureggae"]["rawstreamas"],
            executable=FFMPEG
        )
    )



@bot.command()
async def diskotekacccr(ctx):
    global dabartine_stotis

    dabartine_stotis = "101diskotekacccr"

    voice = ctx.voice_client

    if voice is None:
        await ctx.author.voice.channel.connect()
        voice = ctx.voice_client

    if voice.is_playing() or voice.is_paused():
        voice.stop()

    voice.play(
        discord.FFmpegPCMAudio(
            STOTYS["101diskotekacccr"]["rawstreamas"],
            executable=FFMPEG
        )
    )



@bot.command()
async def rublues(ctx):
    global dabartine_stotis

    dabartine_stotis = "rublues"

    voice = ctx.voice_client

    if voice is None:
        await ctx.author.voice.channel.connect()
        voice = ctx.voice_client

    if voice.is_playing() or voice.is_paused():
        voice.stop()

    voice.play(
        discord.FFmpegPCMAudio(
            STOTYS["rublues"]["rawstreamas"],
            executable=FFMPEG
        )
    )


@bot.command()
async def rudeephouse(ctx):
    global dabartine_stotis

    dabartine_stotis = "rudeephouse"

    voice = ctx.voice_client

    if voice is None:
        await ctx.author.voice.channel.connect()
        voice = ctx.voice_client

    if voice.is_playing() or voice.is_paused():
        voice.stop()

    voice.play(
        discord.FFmpegPCMAudio(
            STOTYS["rudeephouse"]["rawstreamas"],
            executable=FFMPEG
        )
    )


@bot.command()
async def rutechhouse(ctx):
    global dabartine_stotis

    dabartine_stotis = "rutechhouse"

    voice = ctx.voice_client

    if voice is None:
        await ctx.author.voice.channel.connect()
        voice = ctx.voice_client

    if voice.is_playing() or voice.is_paused():
        voice.stop()

    voice.play(
        discord.FFmpegPCMAudio(
            STOTYS["rutechhouse"]["rawstreamas"],
            executable=FFMPEG
        )
    )



@bot.command()
async def seal(ctx):
    global dabartine_stotis

    dabartine_stotis = "spinningseal"

    voice = ctx.voice_client

    if voice is None:
        await ctx.author.voice.channel.connect()
        voice = ctx.voice_client

    if voice.is_playing() or voice.is_paused():
        voice.stop()

    voice.play(
        discord.FFmpegPCMAudio(
            STOTYS["spinningseal"]["rawstreamas"],
            executable=FFMPEG
        )
    )



@bot.command()
async def jazz(ctx):
    global dabartine_stotis

    dabartine_stotis = "jazz"

    voice = ctx.voice_client

    if voice is None:
        await ctx.author.voice.channel.connect()
        voice = ctx.voice_client

    if voice.is_playing() or voice.is_paused():
        voice.stop()

    voice.play(
        discord.FFmpegPCMAudio(
            STOTYS["jazz"]["rawstreamas"],
            executable=FFMPEG
        )
    )





@bot.command()
async def current(ctx):
    await ctx.send(f"{dabartine_stotis}")

@bot.command()
async def dabar(ctx):
    await ctx.send(f"{dabartine_stotis}")



import random


@bot.command()
async def random(ctx):
    global dabartine_stotis

    max_attempts = 30

    for attempt in range(max_attempts):
        channel_id = random.randint(0, 999)

        try:
            response = requests.get(
                f"https://101.ru/api/channel/getListServersChannel/{channel_id}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=5
            )

            if response.status_code != 200:
                continue

            data = response.json()

            # Check that the API returned a usable channel
            if not data.get("result"):
                continue

            channel = data["result"][0]

            title = channel.get("titleChannel")

            if not title:
                continue

            # Construct the stream URL
            stream_url = (
                f"https://srv01.gpmradio.ru:443/"
                f"stream/pro/aac/64/{channel_id}"
            )

            # Found a valid station
            dabartine_stotis = f"101.ru #{channel_id} - {title}"

            voice = ctx.voice_client

            if voice is None:
                if ctx.author.voice is None:
                    await ctx.send("You need to join a voice channel first.")
                    return

                await ctx.author.voice.channel.connect()
                voice = ctx.voice_client

            if voice.is_playing() or voice.is_paused():
                voice.stop()

            voice.play(
                discord.FFmpegPCMAudio(
                    stream_url,
                    executable=FFMPEG
                )
            )

            await ctx.send(
                f"Random station: **{title}** "
                f"(101.ru channel {channel_id})"
            )

            return

        except (requests.RequestException, ValueError, KeyError, IndexError):
            continue

    await ctx.send(
        f"Couldn't find a working 101.ru station after {max_attempts} attempts."
    )






async def play_station(ctx, stream_url):
    voice = ctx.voice_client

    if voice is None:
        if ctx.author.voice is None:
            await ctx.send("You need to join a voice channel first.")
            return False

        await ctx.author.voice.channel.connect()
        voice = ctx.voice_client

    if voice.is_playing() or voice.is_paused():
        voice.stop()

    voice.play(
        discord.FFmpegPCMAudio(
            stream_url,
            executable=FFMPEG
        )
    )

    return True




bot.run(TOKEN)


