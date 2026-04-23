# b4b-apps

Windows 向けの小さな Python ツールをまとめたリポジトリです。

## 含まれるアプリ

- `comment-sender`: 定型コメントを素早く送信する GUI ツール
- `player-jiggle`: `W / A / S / D` をランダムに入力する簡易ツール

## 各アプリの使い方

詳細はそれぞれの README を参照してください。

- [comment-sender/README.md](comment-sender/README.md)
- [player-jiggle/README.md](player-jiggle/README.md)

## CI / Release

- `CI`: `push` / `pull_request` / `workflow_dispatch` で各アプリを Windows 上で並列ビルドします
- `Release`: `v*` タグ push で各アプリの配布用 zip を並列生成し、GitHub Release に添付します

リリース例:

```bash
git tag v1.0.0
git push origin v1.0.0
```

## ライセンス

MIT License
