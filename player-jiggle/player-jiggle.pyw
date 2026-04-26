#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Back 4 Blood Player Jiggle Tool v1.1.0
キー操作シミュレーションでゲーム内アクティブ状態を維持
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import importlib
import subprocess
import sys
import json
import os

# 設定ファイルのパス
SETTINGS_DIR = os.path.join(os.path.expanduser('~'), 'mini-tools', 'player-jiggle')
SETTINGS_FILE = os.path.join(SETTINGS_DIR, 'settings.json')

def load_settings():
    """設定ファイルから設定を読み込む"""
    default_settings = {"interval": 5.0}
    try:
        os.makedirs(SETTINGS_DIR, exist_ok=True)
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {**default_settings, **data}
    except (FileNotFoundError, json.JSONDecodeError):
        save_settings(default_settings)
        return default_settings

def save_settings(settings):
    """設定ファイルに設定を保存する"""
    try:
        os.makedirs(SETTINGS_DIR, exist_ok=True)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"設定の保存に失敗しました: {e}")

# 必要なパッケージの自動インストール
def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package}のインストールが完了しました")
    except subprocess.CalledProcessError:
        print(f"{package}のインストールに失敗しました")
        sys.exit(1)

# 必要なパッケージを確認し、なければインストール
for package in ['pyautogui', 'keyboard']:
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"{package}が見つかりません。インストールします...")
        install_package(package)

import pyautogui
import keyboard  # キーボードショートカット用のモジュール
import random  # ランダム選択のためにインポート

class PlayerJiggle:
    def __init__(self, root):
        self.root = root
        self.root.title("Player Jiggle")
        self.root.geometry("320x240")
        self.root.resizable(False, False)
        
        self.is_running = False
        self.thread = None
        
        # 設定を読み込む
        self.settings = load_settings()
        
        # グローバルホットキーの設定
        keyboard.add_hotkey('l+1', self.start)
        keyboard.add_hotkey('l+2', self.stop)
        
        # メインフレーム
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 間隔設定用のフレーム
        interval_frame = ttk.Frame(main_frame)
        interval_frame.pack(pady=10)
        
        ttk.Label(interval_frame, text="押下間隔（秒）:").pack(side=tk.LEFT)
        self.interval_var = tk.StringVar(value=str(self.settings.get("interval", 5.0)))
        self.interval_entry = ttk.Entry(interval_frame, width=10, textvariable=self.interval_var)
        self.interval_entry.pack(side=tk.LEFT, padx=5)
        
        # ボタン用のフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        self.start_button = ttk.Button(button_frame, text="ON", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = ttk.Button(button_frame, text="停止", command=self.stop, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(button_frame, text="終了", command=self.quit).pack(side=tk.LEFT, padx=10)
        
        # ステータス表示
        self.status_var = tk.StringVar(value="待機中")
        ttk.Label(main_frame, textvariable=self.status_var, font=("", 12)).pack(pady=5)
        
        # ホットキーの常設表示
        hotkey_frame = ttk.LabelFrame(main_frame, text="ホットキー", padding="8")
        hotkey_frame.pack(fill=tk.X, pady=(8, 0))
        ttk.Label(hotkey_frame, text="l+1 : 開始").pack(anchor=tk.W)
        ttk.Label(hotkey_frame, text="l+2 : 停止").pack(anchor=tk.W)
        
    def jiggle_loop(self):
        """キー操作を定期的に実行するループ"""
        try:
            interval = float(self.interval_var.get())
            if interval <= 0:
                interval = 1.0
        except ValueError:
            interval = 5.0
            self.interval_var.set("5")
        
        self.status_var.set("実行中 - Ctrl+W,S,A,D 間隔: " + str(interval) + "秒")
        
        # 押下可能なキーのリスト
        direction_keys = ['w', 's', 'a', 'd']
        
        try:
            # 最初にCtrlキーを押す（押しっぱなしにする）
            pyautogui.keyDown('ctrl')
            
            while self.is_running:
                # ランダムにキーを選択
                selected_key = random.choice(direction_keys)
                
                # 選択されたキーを押下（Ctrlは押しっぱなし）
                pyautogui.keyDown(selected_key)
                time.sleep(0.1)  # 短い時間だけキーを押す
                pyautogui.keyUp(selected_key)
                
                # 長い待機は小さく分割して、その間にホットキーを確認する
                wait_time = 0
                check_interval = 0.1  # 0.1秒ごとにショートカットをチェック
                while wait_time < interval and self.is_running:
                    time.sleep(check_interval)
                    wait_time += check_interval
                    # k+2が押されたかチェック
                    if keyboard.is_pressed('l') and keyboard.is_pressed('2'):
                        # メインスレッドでGUIを更新するようにする
                        self.root.after(0, self.stop)
                        return  # ループを終了
                    
        except Exception as e:
            print(f"エラー: {e}")
            self.root.after(0, self.stop)  # メインスレッドでGUIを更新
    
    def start(self):
        """キー操作シミュレートを開始"""
        if self.is_running:
            return
            
        self.is_running = True
        self.thread = threading.Thread(target=self.jiggle_loop)
        self.thread.daemon = True
        self.thread.start()
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.interval_entry.config(state=tk.DISABLED)
    
    def stop(self):
        """キー操作シミュレートを停止"""
        self.is_running = False
        if self.thread:
            self.thread.join(1.0)
            
        # 必ずCtrlキーを離す
        pyautogui.keyUp('ctrl')
        
        # 念のため全てのキーを離す
        for key in ['w', 's', 'a', 'd']:
            pyautogui.keyUp(key)
        
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.interval_entry.config(state=tk.NORMAL)
        self.status_var.set("待機中")
    
    def quit(self):
        """プログラムを終了"""
        self.stop()
        # 現在のinterval値を設定ファイルに保存
        try:
            interval = float(self.interval_var.get())
        except ValueError:
            interval = 5.0
        self.settings["interval"] = interval
        save_settings(self.settings)
        # ホットキーを解除
        keyboard.remove_hotkey('l+1')
        keyboard.remove_hotkey('l+2')
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlayerJiggle(root)
    root.protocol("WM_DELETE_WINDOW", app.quit)
    root.mainloop()
