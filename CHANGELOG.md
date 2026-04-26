# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-XX-XX

### Added
- Player Jiggle: 設定ファイル機能を追加（intervalの永続化）
- Comment Sender: 設定ファイルの保存先をユーザーディレクトリに変更（移植性向上）
- 型チェック（mypy）と構文チェックの設定

### Changed
- Player Jiggle: 設定ファイルを `~/.mini-tools/player-jiggle/settings.json` に保存
- Comment Sender: 設定ファイルを `~/.mini-tools/comment-sender/settings.json` に保存
- .gitignore: Claw Code関連ファイルを追加

### Fixed
- 各スクリプトの型アノテーションの改善
- 循環依存の可能性を排除

### Security
- 外部パッケージの安全なインポートを確保

## [1.0.0] - 2024-XX-XX

### Added
- Player Jiggle: Back 4 Bloodプレイヤー用キー操作シミュレータ
- Comment Sender: Back 4 Blood用多言語チャットコメント送信ツール
- 初回リリース