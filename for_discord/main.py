import pyautogui
import discord
from discord.ext import commands
import json
import datetime
import os
import shutil
import time

conf_file = open("./config.json","r")
config = json.load(conf_file)
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True  # メッセージに関するデバッグ情報を有効化
allow_recoed_thread_id = []
client = commands.Bot(command_prefix="/", intents=intents)

#configにする unicode errorが出るからひとまずここで
drive_dir = "Your drive dir"
normal = "Your normal size clip dir"
short = "Your shot size clip dir"

after_move_dirs = {}#{thread_id:{"key":"dir_name"}}
before_move_dirs = {"normal":normal,"short":short}


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

def make_save_dir(path):
    try:
        os.mkdir(path)
    except:
        pass

def move_dir(thread_id):
    for key,val in before_move_dirs.items():
        for item in os.listdir(val):#移動元のディレクトリ一覧を取得
            if ("Backtrack" in item):#名前にbacktrackが入っていたら移動する
                shutil.move("{}/{}".format(val, item),after_move_dirs[thread_id][key])
                time.sleep(1)#移動が終わるのを待つ
                shutil.copy("{}/{}".format(after_move_dirs[thread_id][key],item),after_move_dirs[thread_id]["drive_dir_{}".format(key)])

@client.event
async def on_ready():
    print('ログインしました')

@client.event
async def on_message(message):#メッセージをなにかしら受け取ったときの処理
    if type(message.channel) is discord.Thread:#スレッドでメッセージを受け取った時
        if message.author == client.user or message.author.bot:#メッセージの送り主がbotの時は処理しない
            pass
        elif message.channel.id not in allow_recoed_thread_id:#録画を許可しないスレッドは処理しない
            pass
        else:#ここに保存コマンドを書く
            await message.channel.send('動画を保存しています')
            press_hotkey(config["recode_short_key"])
            press_hotkey(config["recode_key"])
            print("動画を保存しています。")
            time.sleep(15)#保存のために少し待つ
            print("移動を開始します")
            move_dir(message.channel.id)
            await message.channel.send('動画を保存しました（多分...）')
    #それ以外はコマンド実行
    await client.process_commands(message)


@client.command("rec")
async def capture(ctx,title):
    channel = ctx.channel #メッセージがあったチャンネルの取得
    #スレッド名の定義
    date = datetime.datetime.now()
    date_str = date.strftime('%Y-%m-%d')
    thread_name = '{}_{}'.format(date_str,title)
    #スレッドの作成
    thread = await channel.create_thread(name=thread_name,reason="クリップ録画API",type=discord.ChannelType.public_thread)#スレッドを作る
    #録画用のために作ったスレッド以外は許容しない
    allow_recoed_thread_id.append(thread.id)
    #移動先のディレクトリ名はスレッドidで管理する
    after_move_dirs[thread.id] = {}
    
    #この辺くそコードなので直したい
    new_normal_dir = "{}\{}_{}".format(normal, date_str, title)
    new_short_dir = "{}\{}_{}".format(short, date_str, title)
    new_drive_dir = "{}\{}_{}".format(drive_dir, date_str, title)
    new_drive_dir_normal = "{}\{}".format(new_drive_dir,"通常")
    new_drive_dir_short = "{}\{}".format(new_drive_dir,"ショート") 
    
    make_save_dir(new_normal_dir)
    make_save_dir(new_short_dir)
    make_save_dir(new_drive_dir)
    make_save_dir(new_drive_dir_normal)
    make_save_dir(new_drive_dir_short)
    
    after_move_dirs[thread.id]["normal"] = new_normal_dir
    after_move_dirs[thread.id]["short"] = new_short_dir 
    after_move_dirs[thread.id]["drive_dir_normal"] = new_drive_dir_normal 
    after_move_dirs[thread.id]["drive_dir_short"] = new_drive_dir_short 

    # メッセージを送信してスレッドを開始します。
    await thread.send("何でもいいのでこのスレッドに送信したらクリップが作成されます。")
    await ctx.send(f'スレッド `{thread_name}` が作成されました： {thread.mention}')


client.run(config["discord_api_key"])
