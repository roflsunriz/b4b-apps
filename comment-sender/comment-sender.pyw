#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Back 4 Blood コメント送信ツール v1.1.0
定型コメントを素早く送信する GUI ツール
"""

import sys
import subprocess
import json
import tkinter as tk
from tkinter import simpledialog, messagebox
import time
import threading
import clipman
import os
import traceback

# pkg_resourcesの代わりにimportlib.metadataを使用
try:
    from importlib import metadata  # Python 3.8+
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "importlib-metadata"])
    from importlib import metadata

# 必須ライブラリの自動インストール
def install_required_packages():
    required_packages = ['pyautogui','keyboard', 'clipman']
    installed_packages = {dist.metadata['name'].lower() for dist in metadata.distributions()}
    
    # ステータス表示用の簡易ウィンドウ
    status_window = tk.Tk()
    status_window.title("ライブラリインストール")
    status_window.geometry("400x100")
    status_window.attributes("-topmost", True)  # 常に最前面に表示
    
    status_label = tk.Label(status_window, text="初期化中...", padx=10, pady=10)
    status_label.pack(fill=tk.X)
    
    for package in required_packages:
        if package not in installed_packages:
            try:
                print(f"{package} をインストール中...")
                status_label.config(text=f"{package} をインストールしています。しばらくお待ちください...")
                status_window.update()
                
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"{package} のインストールが完了しました！")
                status_label.config(text=f"{package} のインストールが完了しました！")
                status_window.update()
                time.sleep(1)  # 1秒間メッセージを表示
                
            except subprocess.CalledProcessError:
                error_msg = f"{package} のインストールに失敗しました。\n手動で以下のコマンドを実行してください：\npip install {package}"
                print(error_msg)
                status_label.config(text=error_msg)
                status_window.update()
                time.sleep(3)  # エラーメッセージを3秒間表示
                status_window.destroy()
                sys.exit(1)
    
    # すべてのパッケージが正常にインストールされた場合
    status_label.config(text="すべてのライブラリが正常にインストールされました。")
    status_window.update()
    time.sleep(1)
    status_window.destroy()

# pyautoguiのインポートをtry-exceptで囲む
try:
    import pyautogui
    import keyboard
    import clipman
except ImportError:
    print("必須ライブラリがインストールされていません。自動インストールを試みます...")
    install_required_packages()
    import pyautogui
    import keyboard
    import clipman

# JSONファイルからコメントを読み込む
def load_comments():
    # 設定ファイルのパス
    config_dir = os.path.join(os.path.expanduser('~'), 'mini-tools', 'comment-sender')
    config_file = os.path.join(config_dir, 'settings.json')
    
    # デフォルトの設定
    default_settings = {
        "comments": [
            "Zombie horde incoming! (丧尸大军来袭！)",
            "This is infinite horde! Throw the pipe bombs or firecrackers to attract zombies and RUN! (这是无限的僵尸大军！投掷管状炸弹或鞭炮来吸引僵尸，然后快跑！)",
            "Boss mutation zombie will appear, so buy flashbangs, alarm bombs, a few armors. (Boss 变异僵尸将会出现，所以要购买闪光弹、报警炸弹和一些盔甲。)",
            "I got caught by hocker! I need help! Shove to release me! (我被小偷抓住了！我需要帮助！推开我！)",
            "I got caught by sleeper! I need help! (我被卧铺车撞倒了！我需要帮助！)",
            "Stay inside the room to survive zombie horde! Try not to get crowded by zombies! (留在房间里，在僵尸大军中生存下来！尽量不要被僵尸围住！)",
            "There's traps on the ground, watch out! (地上有陷阱，小心！)",
            "Keep eyes on the sleepers! They gonna catch you! (注意那些睡觉的人！他们会抓住你的！)",
            "For mutations have armors, aim its head or legs to let them lie down! (对于变异体有铠甲，瞄准它的头或腿让它们躺下！)",
            "Stay together as much as you can to live longer! Teamwork is the key! (尽可能地团结起来以延长生存时间！团队合作是关键！)",
            "I need ammo! I have low ammo! (我需要弹药！我的弹药不多了！)",
            "I have defibrillator to revive you! (我有除颤器可以让你苏醒过来！)",
            "Use firecrackers as they don't allow game to spawn extra zombies unless kill them! (使用爆竹，因为它们不允许游戏产生额外的僵尸，除非杀死它们！)",
            "Try not to make hordes as much as you can! It make the game lower the difficulties! (尽量不要制造太多的怪物！这样可以降低游戏难度！)",
            "Molotovs and fire is not efficient for mutation zombies, but it's efficient for common zombies. (燃烧瓶和火焰对于变异僵尸来说效果不大，但是对于普通僵尸来说却很有效。)",
            "Use first aid cabinet to heal trauma damage! (使用急救柜治疗创伤损伤！)",
            "Bring few grenades to destroy mine shaft! (带上几枚手榴弹来摧毁矿井！)",
            "Don't burn kerosene cans as they can block the tunnel! (不要燃烧煤油罐，因为它们会堵塞隧道！)",
            "Bring razor wires as much as you can! (尽可能多地携带铁丝网！)",
            "Don't steal my items! Give me back! (不要偷我的东西！还给我！)",
            "Use Cursed Toolkit to open stash doors, white loot boxes, alaramd doors! (使用诅咒工具包打开藏匿门、白色战利品箱、警报门！)",
            "I'm going to the toilet! (我要去厕所！)",
            "Get into the Saferoom as soon as possible!(尽快进入安全室！)",
            "Let's exit this hell hole now!(我们现在就离开这个地狱之洞吧！)",
            "Nice job! You did it well! (干得好！你做得很好！)",
            "Good game guys! Have a nice day! (玩得真好！祝大家有愉快的一天！)",
            "Bring shells from the front truck; shells from other places disappear when taken. The truck supplies unlimited shells. Place 5 behind the howitzer, load 1, and grab another from the truck to prepare 6. Only 5 can stay on the ground—extra ones vanish. You need 7, but this method ensures smooth firing. Save shells from other sources for emergencies.",
            "炮弹从前方卡车运来，其他地方的炮弹取走会消失。卡车无限供应炮弹。放5发在榴弹炮后，装1发，再从卡车拿1发，可准备6发。地面最多放5发，多余的会消失。需7发，但此法能顺利发射。其他炮弹留作紧急备用为宜。",
            "榴弾は前方のトラックから運び、他の場所の榴弾は取ると消えます。トラックは無制限に榴弾を供給。5発を榴弾砲の後ろに置き、1発を込め、さらにもう1発をトラックから持ってくると6発準備可能。地面には最大5発までで、それ以上は消えます。7発必要ですが、この方法でスムーズに発射できます。他の榴弾は緊急用に残しておくのが賢明です。",
            "포탄은 앞쪽 트럭에서 가져오세요. 다른 곳의 포탄은 꺼내면 사라집니다. 트럭은 무제한으로 포탄을 공급합니다. 곡사포 뒤에 5발을 놓고, 1발을 장전한 뒤 트럭에서 1발 더 가져오면 6발 준비 가능합니다. 땅에는 최대 5발까지 놓을 수 있고, 초과분은 사라집니다. 7발이 필요하지만 이 방법으로 원활히 발사할 수 있습니다. 다른 포탄은 비상용으로 남겨두는 게 현명합니다.",
            "Don't use the \"Nemesis\" - it will only make enemies notice you randomly and you will be surrounded by them in no time. The \"Nemesis\" is a Legendary RPK (a gold or blue weapon that cannot have attachments).",
            "请停止使用\"Nemesis\"。这只会让敌人随机注意到你，你很快就会被他们包围。 Nemesis 是一款传奇 RPK（金色或蓝色武器，不能带有附件）。",
            "「ネメシス」の使用はやめてください。敵に無差別に気づかれるだけなので、すぐに敵に取り囲まれてしまいます。「ネメシス」はレジェンダリー RPK (金色または青色でアタッチメントを付けられない武器) です。",
            "\"네메시스\"를 사용하지 마십시오. 적에게 무차별로 알아차릴 뿐이므로, 즉시 적에게 둘러싸여 버립니다. 네메시스는 레전더리 RPK(금색 또는 청색으로 부착할 수 없는 무기)입니다."
        ],
        "interval": 1.0,
        "repeat": 1
    }
    
    try:
        # ディレクトリがなければ作成
        os.makedirs(config_dir, exist_ok=True)
        
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 旧バージョンとの互換性を保つ
            if isinstance(data, list):
                return data, default_settings["interval"], default_settings["repeat"]
            return data["comments"], data.get("interval", default_settings["interval"]), data.get("repeat", default_settings["repeat"])
    except FileNotFoundError:
        print(f"{config_file}が見つかりません。デフォルトの設定でファイルを作成します。")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_settings, f, indent=2, ensure_ascii=False)
        return default_settings["comments"], default_settings["interval"], default_settings["repeat"]
    except json.JSONDecodeError:
        print(f"{config_file}が壊れています。デフォルトの設定で上書きします。")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_settings, f, indent=2, ensure_ascii=False)
        return default_settings["comments"], default_settings["interval"], default_settings["repeat"]

# コメント送信関数
def send_comment(comment, interval, repeat, stop_flag_getter):
    for i in range(repeat):
        # 中止フラグをチェック
        if stop_flag_getter():
            print("送信中止が検出されました")
            return
        
        time.sleep(0.1)  # 0.1秒のディレイ
        pyautogui.hotkey('enter')  # チャットを開く
        time.sleep(0.1)  # 0.1秒のディレイ
        
        # クリップボードを使用して送信
        try:
            clipman.copy(comment)
            pyautogui.hotkey('ctrl', 'v')  # 貼り付け
        except Exception as e:
            print(f"送信エラー: {e}")
            
        time.sleep(0.1)  # 0.1秒のディレイ
        pyautogui.hotkey('enter')  # 送信
        time.sleep(0.1)  # 0.1秒のディレイ
        
        # 最後の繰り返しでなければインターバルを待つ
        if i < repeat - 1:
            # インターバル中も定期的に中止フラグをチェック
            wait_start = time.time()
            while time.time() - wait_start < interval:
                if stop_flag_getter():
                    print("インターバル中に中止が検出されました")
                    return
                time.sleep(0.1)  # 短い間隔でチェック

# GUIの作成
class CommentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Back 4 Blood コメント送信ツール")
        
        # ボーダーレスウィンドウにする
        self.root.overrideredirect(True)
        
        # ウィンドウの透明度を設定（0.8 = 80%）
        self.root.attributes("-alpha", 0.8)
        
        # 常に最前面に表示
        self.root.attributes("-topmost", True)
        
        # 画面外に出ない位置へ配置する
        screen_width = self.root.winfo_screenwidth()
        window_width = 500
        window_height = 400
        x_position = max(0, screen_width - window_width - 20)
        y_position = 20
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        # 設定を読み込む
        self.comments, self.interval_value, self.repeat_value = load_comments()
        
        # ルート直下のメインフレーム
        self.base_frame = tk.Frame(root)
        self.base_frame.pack(fill=tk.BOTH, expand=True)
        
        # メインコンテンツフレーム
        self.main_frame = tk.Frame(self.base_frame)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 閉じるボタンを追加
        close_button = tk.Button(self.main_frame, text="×", command=self.root.destroy, 
                               bg="red", fg="white", font=("Arial", 12), bd=0)
        close_button.pack(anchor=tk.NE)  # 右上に配置
        
        # コメントリストフレーム
        self.list_frame = tk.Frame(self.main_frame)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # コメント選択用のチェックボックスリスト
        self.comment_vars = [tk.BooleanVar(value=False) for _ in range(len(self.comments))]
        self.comment_list = tk.Listbox(self.list_frame, selectmode=tk.SINGLE, height=15)
        self.comment_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # コメントをリストボックスに追加
        for i, comment in enumerate(self.comments):
            self.comment_list.insert(tk.END, f"{i+1}. {comment}")
        
        # 編集ボタン
        self.edit_button = tk.Button(self.list_frame, text="編集", command=self.edit_comment)
        self.edit_button.pack(side=tk.LEFT, pady=5)
        
        # 保存ボタン
        self.save_button = tk.Button(self.list_frame, text="保存", command=self.save_comments)
        self.save_button.pack(side=tk.RIGHT, pady=5)
        
        # 設定フレーム
        self.settings_frame = tk.Frame(self.main_frame)
        self.settings_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        
        # インターバル設定
        self.interval_frame = tk.Frame(self.settings_frame)
        self.interval_frame.pack(pady=5)
        
        self.interval_label = tk.Label(self.interval_frame, text="送信間隔（秒）:")
        self.interval_label.pack(side=tk.LEFT)
        
        self.interval_entry = tk.Entry(self.interval_frame, width=5)
        self.interval_entry.insert(0, str(self.interval_value))  # 保存された値を使用
        self.interval_entry.pack(side=tk.LEFT)

        # 繰り返し回数設定
        self.repeat_frame = tk.Frame(self.settings_frame)
        self.repeat_frame.pack(pady=5)
        
        self.repeat_label = tk.Label(self.repeat_frame, text="繰り返し回数:")
        self.repeat_label.pack(side=tk.LEFT)
        
        self.repeat_entry = tk.Entry(self.repeat_frame, width=5)
        self.repeat_entry.insert(0, str(self.repeat_value))  # 保存された値を使用
        self.repeat_entry.pack(side=tk.LEFT)

        # 送信ボタンフレーム
        self.send_frame = tk.Frame(self.settings_frame)
        self.send_frame.pack(pady=20)
        
        # 送信ボタン
        self.send_button = tk.Button(self.send_frame, text="送信開始", command=self.start_sending, bg="#4CAF50", fg="white", width=15)
        self.send_button.pack()

        # 中止フラグ
        self.stop_sending = False
        
        # 中止ボタン
        self.stop_button = tk.Button(self.send_frame, text="中止", command=self.stop_sending_thread, bg="#FF0000", fg="white", width=15)
        self.stop_button.pack(pady=10)
        self.stop_button.config(state=tk.DISABLED)  # 初期状態では無効

        # ホットキー表示
        self.hotkey_frame = tk.LabelFrame(self.settings_frame, text="ホットキー", padx=8, pady=6)
        self.hotkey_frame.pack(fill=tk.X, pady=(5, 10))
        hotkey_lines = [
            "j+8 : 送信",
            "j+9 : 前のコメント",
            "j+0 : 次のコメント",
            "j+p : UI操作を無効化 切替",
        ]
        for line in hotkey_lines:
            tk.Label(self.hotkey_frame, text=line, anchor=tk.W, justify=tk.LEFT).pack(fill=tk.X)

        # グローバルホットキーの設定
        keyboard.add_hotkey('j+8', self.send_with_mouse)  # 送信
        keyboard.add_hotkey('j+9', self.prev_comment)     # 前のコメント
        keyboard.add_hotkey('j+0', self.next_comment)     # 次のコメント
        keyboard.add_hotkey('j+p', self.toggle_mouse_mode)  # マウスモード切り替え

        # ステータスバーフレーム - ルート直下のbase_frameに配置
        self.status_frame = tk.Frame(self.base_frame, bd=1, relief=tk.SUNKEN, height=25)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
        # frameが縮小されないようにする
        self.status_frame.pack_propagate(False)
        
        # ステータスラベル
        self.status_var = tk.StringVar()
        self.status_var.set("待機中")  # 初期状態
        self.status_label = tk.Label(self.status_frame, textvariable=self.status_var, 
                                  anchor=tk.W, bg="lightgray", fg="black", padx=5)
        self.status_label.pack(fill=tk.BOTH, expand=True)
        
        # マウスモード用のチェックボックス
        self.mouse_mode_var = tk.BooleanVar(value=False)
        self.mouse_mode_checkbox = tk.Checkbutton(self.settings_frame, text="UI操作を無効化", 
                                                 variable=self.mouse_mode_var, 
                                                 command=lambda: self.toggle_mouse_mode(None))
        self.mouse_mode_checkbox.pack(side=tk.LEFT, pady=5)

    def __del__(self):
        # ホットキーのクリーンアップ
        keyboard.unhook_all_hotkeys()

    def edit_comment(self):
        selected = self.comment_list.curselection()
        if not selected:
            self.status_var.set("警告: 編集するコメントを選択してください")
            return
        
        index = selected[0]
        # 新しい編集用ウィンドウを作成
        edit_window = tk.Toplevel(self.root)
        edit_window.title("コメント編集")
        edit_window.geometry("500x300")  # ウィンドウサイズを大きくする
        
        # テキストエリアを作成
        text_area = tk.Text(edit_window, wrap=tk.WORD, height=10, width=50)
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text_area.insert(tk.END, self.comments[index])
        
        # 保存ボタン
        def save_changes():
            new_comment = text_area.get("1.0", tk.END).strip()
            if new_comment:
                self.comments[index] = new_comment
                self.comment_list.delete(index)
                self.comment_list.insert(index, f"{index+1}. {new_comment}")
                self.comment_list.selection_set(index)
                edit_window.destroy()
                self.status_var.set("コメントが正常に編集されました")
        
        save_button = tk.Button(edit_window, text="保存", command=save_changes)
        save_button.pack(pady=5)

    def save_comments(self):
        try:
            interval = float(self.interval_entry.get())
            repeat = int(self.repeat_entry.get())
            self.save_comments_to_file(self.comments, interval, repeat)
        except ValueError:
            self.status_var.set("エラー: 数値を正しく入力してください")

    def save_comments_to_file(self, comments, interval, repeat):
        try:
            # 設定ファイルのパス
            config_dir = os.path.join(os.path.expanduser('~'), 'mini-tools', 'comment-sender')
            config_file = os.path.join(config_dir, 'settings.json')
            
            # ディレクトリがなければ作成
            os.makedirs(config_dir, exist_ok=True)
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "comments": comments,
                    "interval": interval,
                    "repeat": repeat
                }, f, indent=2, ensure_ascii=False)
            self.status_var.set("設定が正常に保存されました！")
        except Exception as e:
            self.status_var.set(f"保存エラー: 設定の保存に失敗しました: {str(e)}")

    def stop_sending_thread(self):
        """送信を中止する"""
        print("中止ボタンが押されました")
        self.stop_sending = True
        self.stop_button.config(state=tk.DISABLED)
        self.send_button.config(state=tk.NORMAL)
        self.status_var.set("送信中止")  # ステータスを更新

    def send_comments_thread(self, comments, interval, repeat):
        """コメント送信用スレッド"""
        try:
            # ステータスを更新
            self.root.after(0, lambda: self.status_var.set("送信中..."))
            
            # 選択されたコメントを送信する
            selected_index = self.comment_list.curselection()
            if selected_index:
                selected_comment = self.comments[selected_index[0]]
                # 中止フラグの参照を関数として渡す
                send_comment(selected_comment, interval, repeat, lambda: self.stop_sending)
        finally:
            # 送信完了または中止後の処理
            self.root.after(0, self.on_sending_finished)

    def on_sending_finished(self):
        """送信完了または中止後の処理"""
        if self.stop_sending:
            self.root.title("送信中止")
        else:
            self.root.title("送信完了！")
            self.status_var.set("送信完了")  # ステータスを更新
            
        # 中止フラグをリセット
        self.stop_sending = False
        self.stop_button.config(state=tk.DISABLED)
        self.send_button.config(state=tk.NORMAL)

    def start_sending(self):
        selected_indices = [i for i, var in enumerate(self.comment_vars) if var.get()]
        if not selected_indices and not self.comment_list.curselection():
            self.status_var.set("警告: 送信するコメントを選択してください")
            return
        
        try:
            interval = float(self.interval_entry.get())
            repeat = int(self.repeat_entry.get())
        except ValueError:
            self.status_var.set("エラー: 数値を正しく入力してください")
            return
        
        # ステータスを更新
        self.status_var.set("送信準備中...")
        
        # ボタンの状態を更新
        self.send_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # 0.3秒のカウントダウン
        for i in [0.3, 0.2, 0.1]:
            if self.stop_sending:
                return
            self.root.title(f"送信開始まで {i}秒...")
            self.status_var.set(f"送信開始まで {i}秒...")  # ステータスバーにカウントダウンを表示
            self.root.update()
            time.sleep(0.1)
        
        # 別スレッドで送信を開始
        self.stop_sending = False
        
        # 選択方法による分岐
        if selected_indices:
            selected_comments = [self.comments[i] for i in selected_indices]
        else:
            selected_index = self.comment_list.curselection()[0]
            selected_comments = [self.comments[selected_index]]
            
        threading.Thread(target=self.send_comments_thread, args=(selected_comments, interval, repeat), daemon=True).start()

    def send_with_mouse(self, event=None):
        """ホットキーでコメントを送信"""
        selected_index = self.comment_list.curselection()
        if not selected_index:
            self.status_var.set("警告: 送信するコメントを選択してください")
            return
        
        selected_comment = self.comments[selected_index[0]]
        try:
            interval = float(self.interval_entry.get())
            repeat = int(self.repeat_entry.get())
        except ValueError:
            self.status_var.set("エラー: 数値を正しく入力してください")
            return
        
        # ボタンの状態を更新
        self.send_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # 0.3秒のカウントダウン
        for i in [0.3, 0.2, 0.1]:
            if self.stop_sending:
                return
            self.root.title(f"送信開始まで {i}秒...")
            self.status_var.set(f"送信開始まで {i}秒...")  # ステータスバーにカウントダウンを表示
            self.root.update()
            time.sleep(0.1)
        
        # 別スレッドで送信を開始
        self.stop_sending = False
        threading.Thread(target=self.send_comments_thread, args=([selected_comment], interval, repeat), daemon=True).start()

    def prev_comment(self, event=None):
        """前のコメントに移動"""
        selected_index = self.comment_list.curselection()
        if not selected_index:
            self.comment_list.selection_set(0)  # 未選択なら最初のコメントを選択
        else:
            prev_index = max(0, selected_index[0] - 1)
            self.comment_list.selection_clear(0, tk.END)
            self.comment_list.selection_set(prev_index)
        self.comment_list.see(self.comment_list.curselection()[0])
        self.status_var.set(f"選択: {self.comments[self.comment_list.curselection()[0]][:30]}...")

    def next_comment(self, event=None):
        """次のコメントに移動"""
        selected_index = self.comment_list.curselection()
        if not selected_index:
            self.comment_list.selection_set(0)  # 未選択なら最初のコメントを選択
        else:
            next_index = min(len(self.comments) - 1, selected_index[0] + 1)
            self.comment_list.selection_clear(0, tk.END)
            self.comment_list.selection_set(next_index)
        self.comment_list.see(self.comment_list.curselection()[0])
        self.status_var.set(f"選択: {self.comments[self.comment_list.curselection()[0]][:30]}...")
        
    def toggle_mouse_mode(self, event=None):
        """マウスモードの切り替え"""
        # ホットキーで呼ばれた場合は手動でトグル
        if event is not None:
            current_state = self.mouse_mode_var.get()
            self.mouse_mode_var.set(not current_state)
        
        # チェックボックスの状態を取得
        is_disabled = self.mouse_mode_var.get()
        
        # マウスモードの状態に応じてUI要素の状態を変更
        widgets = [self.edit_button, self.save_button, 
                  self.interval_entry, self.repeat_entry, 
                  self.send_button]
        
        # 停止ボタンは送信中のみ有効
        if self.stop_button['state'] != tk.DISABLED:
            widgets.append(self.stop_button)
            
        for widget in widgets:
            widget.config(state=tk.DISABLED if is_disabled else tk.NORMAL)
        
        # チェックボックスの状態を強制的に設定（見た目のずれを防ぐ）
        if is_disabled:
            self.mouse_mode_checkbox.select()
        else:
            self.mouse_mode_checkbox.deselect()
            
        # ステータスバーを更新（より詳細なステータス表示）
        mode_text = "無効" if is_disabled else "有効"
        message = f"マウス操作: {mode_text} (j+p キーで切り替え可能)"
        if is_disabled:
            message += " - ホットキー(j+8/9/0)は引き続き使用可能"
        self.status_var.set(message)
        print(f"マウスモード: {mode_text} - ホットキーは常に有効")

# メイン実行部分
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = CommentApp(root)
        root.mainloop()
    except Exception as e:
        error_details = traceback.format_exc()
        print(error_details)
        messagebox.showerror("起動エラー", f"GUI の起動に失敗しました。\n\n{e}\n\n{error_details}")
