# findings.md

このリポジトリ固有の実現手段と調査知見の正本です。作業前に全文を読み、行動規範は [AGENTS.md](AGENTS.md) と [COMMON-AGENTS.md](COMMON-AGENTS.md) に従ってください。移動元の本文は以下に保持しています。

## 共通方針の適用と具体的な例外

| 項目 | このリポジトリでの扱い |
| --- | --- |
| 対象の共通ルール | 検証の言語別適用 |
| 理由と適用範囲 | Windows向けPython GUIであり、TypeScript/Bun向けコマンドは適用しない。各アプリのrequirementsと既存CIを使う。 |
| 同等の品質を保つ手段・検証 | Pythonの型・構文検査とWindows CIのPyInstallerビルドを使う。根拠: `comment-sender/`、`player-jiggle/`、`.github/workflows/ci.yml`。GUI操作の成否はビルド結果と区別する。 |

## 文書の役割と適用範囲

- 共通ルールの対象は「ローカル AGENTS.md との関係」「設計と実装方針」「検証」「ドキュメント」。この文書は本リポジトリの構成と既存運用に適用し、共通の行動規範を弱めません。
- ファイル配置・ツール・環境をここに集約する理由は、作業規範と実装上の事実を分け、次の作業者が根拠を確認できるようにするためです。下記の既存手段は同じ対象の設定・CI・検証記録と照合して使います。
- README は利用開始・操作、更新手順は更新と復旧、verification.md は検証手順と実測証跡、専門の設計・研究文書は詳細な根拠を担います。これらの用途は維持し、この文書から参照します。
- 更新・検証の代替は一律のBunコマンドに固定せず、下記の採用技術と既存CIに対応する検査を使います。実行不能や未検証の条件は成功扱いせず verification.md に残します。

<a id="readme-1"></a>

## コード品質

- mypyによる型チェック対応
- Python構文チェック
- 安全な外部パッケージインポート

移動元: `README.md`。

<a id="readme-2"></a>

## CI / Release

- `CI`: `push` / `pull_request` / `workflow_dispatch` で各アプリを Windows 上で並列ビルドします
- `Release`: `v*` タグ push で各アプリの配布用 zip を並列生成し、GitHub Release に添付します

リリース例:

```bash
git tag v1.1.0
git push origin v1.1.0
```

移動元: `README.md`。

<a id="readme-3"></a>

## 開発

```bash
# 型チェック
python -m mypy comment-sender/comment-sender.pyw
python -m mypy player-jiggle/player-jiggle.pyw

# 構文チェック
python -m py_compile comment-sender/comment-sender.pyw
python -m py_compile player-jiggle/player-jiggle.pyw
```

移動元: `README.md`。

<a id="readme-4"></a>

## 依存更新の自動処理

Dependabot は対象の依存関係を毎週確認します。patch／minor 更新は PR のチェック（CI）が成功した後に自動で squash merge されます。CI の失敗ジョブは 1 回だけ再実行します。再失敗した PR は残して手動で修正します。major 更新は手動で確認します。

移動元: `README.md`。

## 根拠と検証記録

- [README.md](README.md): 利用者向けの導入と操作。
- [verification.md](verification.md): 検証手順、実測結果、未確認事項。
- [how-to-update.md](how-to-update.md): 更新・復旧の実手順。
