# b4b-apps

Windows 向けの小さな Python ツールをまとめたリポジトリです。

## 含まれるアプリ

- `comment-sender`: Back 4 Blood用の定型コメントを素早く送信する GUI ツール
- `player-jiggle`: Back 4 Blood用の`W / A / S / D`をランダムに入力する簡易ツール

## 各アプリの使い方

詳細はそれぞれの README を参照してください。

- [comment-sender/README.md](comment-sender/README.md)
- [player-jiggle/README.md](player-jiggle/README.md)

## 機能

### Comment Sender v1.1.0
- 多言語対応（英語、中国語、日本語、韓国語）
- ホットキー対応（j+8/9/0/p）
- 設定の永続化（~/.mini-tools/comment-sender/settings.json）
- UI操作の無効化モード

### Player Jiggle v1.1.0
- キー操作シミュレーション
- ホットキー対応（l+1/2）
- 設定の永続化（~/.mini-tools/player-jiggle/settings.json）
- ランダムな方向キー入力

## コード品質

- mypyによる型チェック対応
- Python構文チェック
- 安全な外部パッケージインポート

## CI / Release

- `CI`: `push` / `pull_request` / `workflow_dispatch` で各アプリを Windows 上で並列ビルドします
- `Release`: `v*` タグ push で各アプリの配布用 zip を並列生成し、GitHub Release に添付します

リリース例:

```bash
git tag v1.1.0
git push origin v1.1.0
```

## 開発

```bash
# 型チェック
python -m mypy comment-sender/comment-sender.pyw
python -m mypy player-jiggle/player-jiggle.pyw

# 構文チェック
python -m py_compile comment-sender/comment-sender.pyw
python -m py_compile player-jiggle/player-jiggle.pyw
```

## ライセンス

MIT License
