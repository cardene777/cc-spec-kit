<div align="center">
    <img src="./media/logo.webp" alt="Grove Logo" width="200" height="200"/>
    <h1>🌳 Grove</h1>
    <h3><em>品質保証機能を組み込んだAI駆動開発ツールキット</em></h3>
</div>

<p align="center">
    <strong>仕様駆動開発 × TDD × AI自動レビュー = 高品質なソフトウェアを高速で構築</strong>
</p>

<p align="center">
    <a href="https://github.com/cardene/grove/stargazers"><img src="https://img.shields.io/github/stars/cardene/grove?style=social" alt="GitHub stars"/></a>
    <a href="https://github.com/cardene/grove/blob/main/LICENSE"><img src="https://img.shields.io/github/license/cardene/grove" alt="License: MIT"/></a>
    <a href="./README.md">English</a>
</p>

---

## 🎯 Groveとは

**Grove**は、AIエージェントを活用した仕様駆動開発ツールキットです。

従来の開発では、「コードを書く → レビュー → 修正」というサイクルが手動で、時間がかかり、エラーが発生しやすい状況でした。

Groveは、**仕様から実装まで自動化**し、**TDDワークフロー**と**AI自動レビュー**を組み込むことで、高品質なコードを高速で生成します。

### なぜGroveなのか

✅ **仕様が常に最新**: 仕様書から直接コード生成するため、ドキュメントとコードが乖離しない
✅ **品質が保証される**: TDD + 3層AIレビューで自動品質チェック
✅ **高速フィードバック**: バックグラウンド並列実行で約28%高速化
✅ **AI同士の協調**: 複数AIエージェントでクロスチェック
✅ **多言語対応**: 日本語・英語完全対応

## 🚀 3つの特徴

### 1. 🧪 t-wada式TDD統合

すべてのタスクで**Test-Driven Development**を強制実行:

```
各タスクごとに:
  Red      → テスト失敗を確認
  Green    → 最小実装でテストを通す
  Refactor → リファクタリング
  Review   → AI自動検証
```

日本発のTDD暗黙知を形式知化し、AIに実行させます。

### 2. 🔍 3層AIレビューシステム

**Implementation → Self Review → Cross Review** の3段階品質保証:

| レイヤー | 実行者 | タイミング | 目的 |
|---------|-------|-----------|------|
| **Layer 1: Implementation** | AI Agent | 実装時 | TDDワークフローでコード生成 |
| **Layer 2: Self Review** | 同じAI Agent | 実装直後（バックグラウンド） | 8項目自動検証 + Auto-Fix |
| **Layer 3: Cross Review** | 別のAI Agent | 必要に応じて | 異なる視点での追加検証 |

**Self Reviewの自動化**:
```
T001実装完了 → Self Review起動（バックグラウンド）
T002実装完了 → Self Review起動（バックグラウンド）
T003実装完了 → Self Review起動（バックグラウンド）
      ↓
全検証完了 → レポート生成 → Auto-Fix（最大3回）
```

**8項目検証チェックリスト**:
1. ✅ 仕様適合性
2. ✅ 技術スタック遵守
3. ✅ タスク完了度
4. ✅ テストカバレッジ
5. ✅ エラーハンドリング
6. ✅ セキュリティ
7. ✅ パフォーマンス
8. ✅ コード品質

**スコアリング**: 0-100点（Critical: -30, High: -20, Medium: -10, Low: -5）
**合格基準**: 80点以上

### 3. ⚡ バックグラウンド並列実行

**従来の逐次実行**:
```
実装 → 検証（待機） → 実装 → 検証（待機） → ...
```

**Groveの並列実行**:
```
実装 → 検証（バックグラウンド）
  ↓
実装 → 検証（バックグラウンド）
  ↓
実装 → 検証（バックグラウンド）
  ↓
全完了 → 結果収集 → 修正
```

待ち時間を削減し、開発速度を向上させます。

## 📦 インストール

### 1回だけインストール（推奨）

```bash
uv tool install grove-cli --from git+https://github.com/cardene/grove.git
```

### プロジェクト初期化

```bash
# 新規プロジェクト
grove init my-app --ai claude --lang ja

# 既存プロジェクト
grove init . --ai claude --lang ja

# または
grove init --here --ai claude --lang ja
```

### アップグレード

```bash
uv tool install grove-cli --force --from git+https://github.com/cardene/grove.git
```

## 🎬 使い方

### 基本ワークフロー

```bash
# AIエージェントを起動してプロジェクトディレクトリへ移動
# 以下のコマンドが使用可能になります

# 1. プロジェクト原則を定義
/grove.constitution コード品質、テスト基準、パフォーマンス要件を重視した原則を作成

# 2. 機能仕様を作成
/grove.specify タスク管理アプリケーションを構築。プロジェクト、タスク、カンバンボード機能を含む

# 3. (オプション) フロントエンドデザイン仕様
/grove.design デザインシステム、コンポーネント、レイアウトを定義

# 4. 技術実装計画を作成
/grove.plan React + TypeScript、Node.js、PostgreSQLを使用

# 5. タスクに分解
/grove.tasks

# 6. 実装実行（TDD + Self Review自動実行）
/grove.implement

# 7. (オプション) クロスレビュー（別AIで実行）
/grove.review

# 8. (オプション) 問題の自動修正
/grove.fix
```

### 実行例

```
T001 Implementation completed.
🔄 T001 Self Review launched in background (job: a703da0)
   Report will be saved to: reports/self-review/task-T001.md

T002 Implementation completed.
🔄 T002 Self Review launched in background (job: aa59562)
   Report will be saved to: reports/self-review/task-T002.md

⏳ Waiting for 2 verification agents to complete...
✓ All verification agents completed

Parsing reports...
✓ T001: PASS (Score: 95/100)
✗ T002: FAIL (Score: 65/100, 3 issues)

🔧 Auto-fixing T002...
✓ T002 Auto-Fix SUCCESS (Score: 85/100)

Self Review completed.
```

## 🤖 対応AIエージェント

17種類以上のAIエージェントに対応:

| AIエージェント | 対応 | 備考 |
|--------------|------|------|
| **Claude Code** | ✅ | **推奨** - Self Reviewバックグラウンド実行完全対応 |
| Cursor | ✅ | |
| GitHub Copilot | ✅ | |
| Codex CLI | ✅ | |
| Gemini CLI | ✅ | |
| Windsurf | ✅ | |
| その他12種類 | ✅ | Qoder, Amp, Auggie, CodeBuddy, IBM Bob, Jules, Kilo Code, opencode, Qwen, Roo, SHAIなど |

詳細は[対応AI一覧](./docs/agents.md)を参照してください。

## 📋 コマンド一覧

### 必須コマンド（開発フロー）

| コマンド | 説明 |
|---------|------|
| `/grove.constitution` | プロジェクト原則・開発ガイドライン作成 |
| `/grove.specify` | 機能仕様作成（要件・ユーザーストーリー） |
| `/grove.plan` | 技術実装計画作成（技術スタック・アーキテクチャ） |
| `/grove.tasks` | タスク分解（TDDワークフロー付き） |
| `/grove.implement` | 実装実行（TDD + Self Review自動実行） |

### 品質保証コマンド

| コマンド | 説明 |
|---------|------|
| `/grove.review` | AIレビュー実行（Self/Cross Review自動判定） |
| `/grove.fix` | レビュー問題の自動修正（TDDアプローチ） |

### オプションコマンド

| コマンド | 説明 |
|---------|------|
| `/grove.clarify` | 仕様の曖昧な部分を明確化 |
| `/grove.design` | フロントエンドデザイン仕様作成 |
| `/grove.analyze` | 成果物間の整合性分析 |
| `/grove.checklist` | カスタム品質チェックリスト生成 |

## 🔍 Self Reviewの仕組み

### 1. バックグラウンド起動

実装完了と同時に、Verification Agentがバックグラウンドで起動:

```python
Task(
    description="Verify task T001",
    prompt="...",
    subagent_type="verification-agent",
    run_in_background=True  # バックグラウンド実行
)
```

### 2. 自律的な検証・レポート生成

Verification Agentが以下を自動実行:

1. **Context読み込み**: spec.md, plan.md, tasks.md
2. **実装ファイル読み込み**: タスクで指定されたファイル
3. **8項目検証**: チェックリストに基づく検証
4. **スコア計算**: 0-100点（重要度別ペナルティ）
5. **レポート生成**: Markdown形式（日本語）
6. **ファイル保存**: `reports/self-review/task-{ID}.md`

### 3. レポート形式

```markdown
# Task T001 検証レポート

**日時:** 2025-12-21 10:30:00
**タスクID:** T001
**説明:** ユーザー認証機能実装
**フェーズ:** Phase 1

---

## 1. サマリー

| 項目   | 値           |
| ------ | ------------ |
| スコア | 85/100       |
| 状態   | **PASS**     |
| 問題数 | 1            |

---

## 2. 検証チェックリスト

- [x] 仕様適合性: PASS
- [x] 技術スタック遵守: PASS
- [x] タスク完了度: PASS
- [x] テストカバレッジ: PASS
- [x] エラーハンドリング: FAIL
- [x] セキュリティ: PASS
- [x] パフォーマンス: PASS
- [x] コード品質: PASS

---

## 3. 検証結果

##### Issue 1

| 項目   | 詳細                |
| ------ | ------------------- |
| 重要度 | Medium              |
| 場所   | `src/auth.py:42`    |

- **説明**: ログイン失敗時のエラーハンドリングが不足
- **原因**: try-exceptブロックがない
- **推奨修正**: 例外処理を追加
- **証拠**: [コードスニペット]

---

## 4. 結論

Task T001の検証が完了しました。スコア: 85/100

軽微な問題が1件ありますが、合格基準（80点）を満たしています。
```

### 4. Auto-Fix

FAILしたタスクは自動的に修正:

```
🔧 Auto-fixing T002 (Score: 65/100, 3 issues)...

Issue 1 (Critical): パスワードハッシュ化なし
  Red:    テスト追加
  Green:  bcrypt実装
  Refactor: テスト確認 ✓

Issue 2 (High): 入力検証なし
  Red:    テスト追加
  Green:  バリデーション実装
  Refactor: テスト確認 ✓

Issue 3 (Medium): エラーハンドリング不足
  Red:    テスト追加
  Green:  例外処理追加
  Refactor: テスト確認 ✓

Re-verification: Score 85/100 (0 issues) ✓
```

最大3回まで自動修正を試行します。

## 🌍 多言語対応

日本語・英語完全対応:

```bash
# 日本語
grove init my-app --ai claude --lang ja

# 英語
grove init my-app --ai claude --lang en
```

テンプレート、コマンド、レポートすべてが選択した言語で生成されます。

## 📚 ドキュメント

- **[Groveガイド（日本語）](./articles/grove.md)** - 詳細な解説記事
- **[開発方法論](./spec-driven.md)** - 仕様駆動開発の全体像
- **[インストールガイド](./docs/installation.md)** - セットアップ手順
- **[クイックスタート](./docs/quickstart.md)** - 5分で始める
- **[ローカル開発](./docs/local-development.md)** - 貢献方法

## 🛠️ システム要件

- **OS**: Linux / macOS / Windows
- **AI Agent**: [対応AI](#-対応aiエージェント)のいずれか
- **Python**: 3.11以上
- **パッケージ管理**: [uv](https://docs.astral.sh/uv/)
- **バージョン管理**: [Git](https://git-scm.com/)

## 💡 よくある質問

### Q: Spec Kitとの違いは？

A: GroveはSpec Kitを拡張したツールです:

| 機能 | Spec Kit | Grove |
|------|---------|-------|
| 仕様駆動開発 | ✅ | ✅ |
| TDD統合 | ❌ | ✅ t-wada方式 |
| Self Review | ❌ | ✅ バックグラウンド並列実行 |
| Cross Review | ❌ | ✅ 複数AI対応 |
| Auto-Fix | ❌ | ✅ TDDアプローチ |
| 多言語対応 | ❌ | ✅ 日本語・英語 |
| Verification Agent | ❌ | ✅ Claude Code対応 |

### Q: どのAIエージェントが推奨？

A: **Claude Code**を推奨します。バックグラウンドSelf ReviewとVerification Agentに完全対応しています。

他のAIエージェントでも動作しますが、Self Reviewは同期実行になります。

### Q: 既存プロジェクトに導入できる？

A: はい。`grove init . --ai claude`または`grove init --here --ai claude`で既存プロジェクトに導入できます。

### Q: レビューをスキップできる？

A: はい。`/grove.implement --skip-self-review`でSelf Reviewをスキップできます。

ただし、品質保証のため推奨しません。

## 🤝 コントリビューション

プルリクエスト・Issue報告を歓迎します！

詳細は[CONTRIBUTING.md](./CONTRIBUTING.md)を参照してください。

## 💬 サポート

- **バグ報告**: [GitHub Issues](https://github.com/cardene/grove/issues)
- **機能リクエスト**: [GitHub Issues](https://github.com/cardene/grove/issues)
- **質問・議論**: [GitHub Discussions](https://github.com/cardene/grove/discussions)

## 🙏 謝辞

Groveは以下のプロジェクト・個人の成果を基に開発されています:

**Spec Kit** (GitHub):
- [Den Delimarsky](https://github.com/localden)
- [John Lam](https://github.com/jflam)

**Grove拡張機能開発**:
- [Cardene](https://github.com/cardene)

**TDD方法論**:
- [t-wada](https://github.com/twada) - Test-Driven Development

すべての貢献者に感謝します。

## 📄 ライセンス

MITライセンスの下で公開されています。詳細は[LICENSE](./LICENSE)を参照してください。

---

<p align="center">
    <strong>🌳 Grove - AI時代の高品質開発ツールキット</strong><br>
    Built with ❤️ by the Grove community
</p>
