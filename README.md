# NotionDBToDiscord
まだ編集中です！！！！！

# 使い方

## Requiements
✅ Notionでデータベースが存在すること
    少なくともName,url,Doneのプロパティがあること
✅ Discordのアカウントを持っていること・自分用で何かサーバー立ち上げていること

### 準備
notionのAPIを取得する
notionのデータベースのidを取得する

Discordのwebhookを取得する
など
→→準備の部分は適当にリンクを貼って参照してもらうのでここで細かく解説することはしないです．


### セットアップ

1　仮想環境を作る

2　cronのセットアップ→プライバシーの設定でファイルアクセスを許可すること

これでおk




以下は、あなたのリポジトリ構成と実装内容に基づいた、**利用者向け README（完成版）** です。
コード内容・依存関係（`python-dotenv`, `requests` のみ）・cron運用もすべて正確に反映しています。

---

# 📘 NotionDBToDiscord

Notion に保存している「論文リスト」や「ToDoリスト」から、
**未完了（Done=False）の項目を1件ランダムに選び、Discord に自動投稿する** Python スクリプトです。

毎朝、Notion のデータベースからランダムで1件選び、Discord に通知することで、
「今日読む論文」や「今日のタスク」を自動でリマインドできます。

---

## 🧩 機能概要

| 処理内容         | ファイル                 | 説明                                              |
| ------------ | -------------------- | ----------------------------------------------- |
| 環境変数読み込み     | `utils/config.py`    | `.env` から Notion API や Discord Webhook の設定を読み込み、`TARGETS`（対象ごとのget/pick/send組み合わせ）を構築 |
| Notion API通信 | `get/notion.py`      | 指定データベースからページ情報を取得                              |
| データ選択        | `pick/random.py`     | `Done`/`Status` などをもとに未読のページをランダム抽出してタイトル・URLを取得 |
| メッセージ組み立て    | `utils/message.py`   | タイトル・URL・挨拶文からDiscord投稿用メッセージを組み立て               |
| Discord送信    | `send/discord.py`    | Webhook 経由でメッセージを投稿                             |
| 実行統合         | `run/notion_db_discord.py` | `TARGETS`を引いて get→pick→send を1回実行          |
| 自動化          | `run.sh`             | cron などのスケジューラから実行するためのスクリプト                    |

---

## ✅ 必要環境

* **Python 3.10 以上**
* **Notion API が利用可能なアカウント**
* **Discord サーバーと Webhook URL**

### 🔧 必要パッケージ（最小構成）

```bash
pip install python-dotenv requests
```

> ※ 旧 `requirements.txt` には Flask 関連が含まれていましたが、本スクリプトでは不要です。
> 上記2つのみで完全に動作します。

---

## 🧾 `.env` の設定

`.env` ファイルをプロジェクトルートに作成し、以下を記入します。

```bash
# ---- Notion ----
NOTION_API_KEY=secret_xxxxxxxx
NOTION_DATABASE_ID=1af1fbe7470a801c8926dcc2789c8252
NOTION_VERSION=2022-06-28

# ---- Discord ----
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxxxxx/yyyyyy

# ---- メッセージ設定 ----
MESSAGE_GREETING=おはようございます．今日の論文は.....
MESSAGE_TEMPLATE={greeting}\n{title}\n{url}
SELECTED_PROPERTIES=Name,Done,URL
```

> `NOTION_DATABASE_ID` はデータベースURL内の 32桁ID です
> 例）[https://www.notion.so/username/**1af1fbe7470a801c8926dcc2789c8252](https://www.notion.so/username/**1af1fbe7470a801c8926dcc2789c8252)**

---

## ⚙️ セットアップ手順

### 1️⃣ 仮想環境を作成

```bash
python -m venv .venv
source .venv/bin/activate   # Windowsの場合は .venv\Scripts\activate
```

### 2️⃣ パッケージをインストール

```bash
pip install -r requirements.txt
```

もしくは、軽量構成なら：

```bash
pip install python-dotenv requests
```

### 3️⃣ 動作確認

`.env` を設定後、以下を実行します。

```bash
python -m run.notion_db_discord <paper|book|academic>
```

成功すれば、Notionの「未読ページ」が Discord に送信されます。

---

## ⏰ 定期実行（cron設定例）

macOS / Linux で毎朝8時に実行する場合：

1. `run.sh` を次のように編集します。

```bash
#!/usr/bin/env bash
exec >> /Users/<your_name>/Documents/NotionDBToDiscord/logfile.log 2>&1

cd "/Users/<your_name>/Documents/NotionDBToDiscord" || exit 1
/Users/<your_name>/.pyenv/versions/NotionPaperDiscord/bin/python -m run.notion_db_discord
```

2. cron に登録：

```bash
crontab -e
```

```bash
0 8 * * * /Users/<your_name>/Documents/NotionDBToDiscord/run.sh
```

3. macOS の場合：「システム設定 → プライバシーとセキュリティ → フルディスクアクセス」で
   `cron` にアクセス権を与えてください。
   これを行わないと「書類」フォルダ内の `.env` が読み込まれません。

---

## 💡 トラブルシューティング

| 症状                 | 原因と対策                                      |
| ------------------ | ------------------------------------------ |
| Discordに投稿されない     | `.env` の Webhook URL が正しいか確認               |
| Notionからデータが取得できない | Notion の統合がデータベースに共有されているか確認               |
| cronで動かない          | macOS の「フルディスクアクセス」設定を確認                   |
| 投稿内容が崩れる           | `.env` の `MESSAGE_TEMPLATE` の改行文字（`\n`）を確認 |

---

## 🪄 カスタマイズ例

* 投稿テンプレートを変更
  例：

  ```bash
  MESSAGE_TEMPLATE={greeting} 今日読むのはこちら👇\n📖 {title}\n🔗 {url}
  ```

* Notionの別データベースを使う場合
  → `.env` の `NOTION_DATABASE_ID` を切り替えるだけ

* 定期実行時間を変える
  → `crontab` のスケジュールを調整（例：`30 7 * * *` で毎朝7:30）

---

## 🧾 ライセンス

MIT License
© 2025 Shiryu

---

このREADMEは、あなたのリポジトリのソース (`utils/config.py`, `get/notion.py`, `pick/random.py`, `utils/message.py`, `send/discord.py`, `run.sh.sample`) に基づき、
**利用者（エンジニアでなくてもセットアップできる）向けに最適化**した内容です。

---

必要であれば次に、
👉 **「開発者向けREADME」版（内部設計・依存構造・再利用API解説つき）」** も作成できます。
利用者向けのままで十分ですか？
