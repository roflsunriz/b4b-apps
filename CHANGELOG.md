# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- CI と Dependabot の分類の実行順が前後しても更新を取りこぼさないよう、同じ PR 番号と head SHA を再照合する経路を追加した。

### Changed

- CIとReleaseの実行環境を最新のメジャー版に追従させるため、actions/checkoutをv4からv7へ、actions/setup-pythonをv5からv7へ、actions/upload-artifactをv4からv7へ、actions/download-artifactをv4からv8へ、softprops/action-gh-releaseをv2からv3へ引き上げた。
- 依存更新を安全に省力化するため、Dependabot の patch／minor PR を既存 CI の全チェック成功後に自動取り込みし、失敗ジョブを一度再実行する設定を追加した。
- 作業開始時の共通指針見落としを防ぐため、調査やコマンド実行より前に `COMMON-AGENTS.md` を先頭から末尾まで読み、EOFを確認する必須ゲートを追加した。

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
