# remote_hotkey_controller
遠隔でPCのホットキーを操作するためのスクリプト。
自分で使うために作ったので、細かい説明などは省きます。
使用の際は全て自己責任でお願いいたします。

自由にフォークして使っていただくなり、改造して使っていただいて構いません。

# 使用方法
## ライブラリのinstall
```
pip install pyautogui
```
Discodebot経由で操作する場合は下記を実施
```
pip install discord
```

## for_discord
1. ディスコードbotで使うには、まずdiscord botを作成してください。
2. 作成したbotのtokenを払い出してください。
3. discordbotを任意のサーバに招待しておく。
4. for_discordディレクトリにあるconfig.jsonを開き、discord_api_keyのvalに2で作成したkeyを入力
5. config.jsonにホットキーの情報を入力する（特殊キーはpyautoguiに準拠）
6. main.pyをホットキーの情報に合わせて書き換える
7. 下記のコマンドで起動する
```
python main.py
```
※discordのサーバで`/rec`とコマンドを叩くとbotが作動するようになっています。
※配信でリプレイバッファにたまっている映像を録画したいモチベーションがあったので、ホットキーをそのように割り当てて録画できるようにしました。
※実際に配信で使用しているコードは、`for_flare`ブランチをご覧ください
