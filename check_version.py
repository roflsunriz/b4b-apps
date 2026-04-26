#!/usr/bin/env python3
"""
バージョンチェックスクリプト
このスクリプトは各アプリのバージョンを確認します
"""

import os
import sys

def get_comment_sender_version():
    """comment-senderのバージョンを取得"""
    with open("comment-sender/comment-sender.pyw", "r", encoding="utf-8") as f:
        for line in f:
            if "バージョン" in line:
                return line.strip()
    return "バージョン情報なし"

def get_player_jiggle_version():
    """player-jiggleのバージョンを取得"""
    with open("player-jiggle/player-jiggle.pyw", "r", encoding="utf-8") as f:
        for line in f:
            if "バージョン" in line:
                return line.strip()
    return "バージョン情報なし"

def main():
    """メイン関数"""
    print("b4b-apps バージョンチェック")
    print("=" * 40)
    
    # バージョン情報を取得
    print(f"Comment Sender: {get_comment_sender_version()}")
    print(f"Player Jiggle: {get_player_jiggle_version()}")
    print()
    
    # 現在のディレクトリを表示
    print(f"現在のディレクトリ: {os.getcwd()}")
    
    # 環境情報
    print(f"Python バージョン: {sys.version}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())