import pyautogui
import discord
from discord.ext import commands
import json

conf_file = open("./config.json")
config = json.load(conf_file)
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="/", intents=intents)

def all_key_up():
    for key in pyautogui.KEYBOARD_KEYS:
        pyautogui.keyUp(key)
    

def press_hotkey(keys):
    try:
        for key in keys:
            pyautogui.keyDown(key)
        for key in keys:
            pyautogui.keyUp(key)
    except:
        all_key_up()

@client.event
async def on_ready():
    print('ログインしました')


@client.command("rec")
async def test(ctx):
    await ctx.send('キャプチャーコマンドを送りました。')
    press_hotkey(config["recode_short_key"])
    press_hotkey(config["recode_key"])



client.run(config["discord_api_key"])