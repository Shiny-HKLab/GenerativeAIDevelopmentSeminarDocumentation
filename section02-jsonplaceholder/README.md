# Python + requestsライブラリでAPIを試してみよう！

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shiny-HKLab/GenerativeAIDevelopmentSeminarDocumentation/blob/main/section02-jsonplaceholder/notebook-colab.ipynb)

## はじめに

前回はAPIの基本的な概念について学びました。今回は実際にPythonを使って「WebAPI」にアクセスする方法を見ていきましょう！

> 📝 **ポイント**: APIにはいろんな種類があるけど、今回扱うのは「WebAPI」というインターネットを通じて使えるタイプのものです。スマホアプリやWebサービスの裏側で、こうしたWebAPIがデータのやりとりをしていることが多いです。

## 今回使用する道具たち

1. **Python**: 人気の高いプログラミング言語です 🐍
2. **requestsライブラリ**: Pythonでインターネットと通信するための便利な道具箱📦
3. **JSONPlaceholder**: お試しで使える無料のWebAPIサービス（練習用のサンドボックスみたいなもの）🏝️

## JSONPlaceholderって何？

[JSONPlaceholder](https://jsonplaceholder.typicode.com/)は、APIの練習や学習に最適な無料のダミーAPIサービスです。まるで「APIの遊び場」のようなものですね！

特徴をご紹介すると：

- 🆓 登録不要、完全無料で誰でも使えます
- 👥 ユーザー情報、投稿、コメントなどの仮想データが用意されています
- 🔄 GET, POST, PUT, DELETEといった様々な操作方法を試せます
- 🎮 実際のAPIの使い方を安全に練習できます

例えるなら、料理を習うときの練習用キッチンのようなものです。失敗しても大丈夫な環境で思う存分練習できます！

## JSONって何？

### JSONの基本

**JSON (JavaScript Object Notation)** は、コンピューター同士がデータをやりとりするときに使う特別な形式です。人間にも読めて、コンピュータにも理解できる、とっても便利な「共通言語」なんです。

まるで、誰にでも読める特別なメモのようなものです！✉️

JSONの素敵なところ：
- 👀 人間が読みやすい（本当に！テキストエディタで開けばそのまま読めます）
- 🤖 コンピュータも簡単に理解できる
- 🌍 どんなプログラミング言語でも使える万国共通のデータ形式
- 🌐 インターネット上でのデータのやりとりに大活躍

### JSONデータの構造：レゴブロックのように組み立てる

JSONデータは主に2つの基本ブロックから作られています：

1. **オブジェクト（Object）**: 名前と値のペアの集まり
   - 波括弧 `{}` で囲みます（まるで抱きしめるようなカッコ）
   - `"キー": 値` の形式で書きます（例：`"名前": "たなか"`）
   - キーは必ず文字列（ダブルクォーテーション `"` で囲む）
   - 複数のペアはカンマ `,` で区切ります

2. **配列（Array）**: 値のリスト
   - 角括弧 `[]` で囲みます（お弁当箱のようなイメージ）
   - 中身はカンマ `,` で区切ります（例：`[1, 2, 3]`）

### JSONで使えるデータ型：カラフルなブロック

JSONでは以下の種類のデータを使えます：

- **文字列（String）**: `"こんにちは"`, `"Hello"` など（お手紙の内容みたいなもの）
- **数値（Number）**: `10`, `3.14`, `-20` など（計算で使う数字）
- **真偽値（Boolean）**: `true` または `false`（YESかNOのような二択）
- **null**: `null`（「何もない」ことを表す特別な値）
- **オブジェクト（Object）**: `{"名前": "田中", "年齢": 12}`（情報のまとまり）
- **配列（Array）**: `[1, 2, 3, 4, 5]`, `["りんご", "みかん", "バナナ"]`（リスト）

### JSONの例：実際に見てみよう

以下は、あるユーザーの情報を表すJSONの例です：

```json
{
  "id": 1,
  "name": "田中太郎",
  "email": "tanaka@example.com",
  "age": 12,
  "isStudent": true,
  "hobbies": ["読書", "サッカー", "プログラミング"],
  "address": {
    "city": "東京",
    "zipcode": "100-0001"
  }
}
```

この例を見ると：
- 全体が波括弧 `{}` で囲まれた一つのオブジェクト
- `name`, `email` などのキーと値のペアがあります
- `hobbies` は角括弧 `[]` で囲まれた配列で、趣味のリストを表しています
- `address` の中にさらに波括弧 `{}` で囲まれたオブジェクトがあります（入れ子構造）

まるで、人物紹介カードのようなものですね！

### PythonでJSONを扱う：翻訳作業

Pythonでは、標準ライブラリの `json` モジュールを使ってJSONデータを簡単に扱えます：

```python
import json

# Pythonの辞書（dict）をJSON文字列に変換（シリアライズ）
python_dict = {
    "name": "田中太郎",
    "age": 12,
    "hobbies": ["読書", "サッカー"]
}
json_str = json.dumps(python_dict, ensure_ascii=False)
print(json_str)
# 出力: {"name": "田中太郎", "age": 12, "hobbies": ["読書", "サッカー"]}

# JSON文字列をPythonの辞書に変換（デシリアライズ）
json_data = '{"name": "鈴木花子", "age": 11}'
python_obj = json.loads(json_data)
print(python_obj["name"])  # 出力: 鈴木花子
print(python_obj["age"])   # 出力: 11
```

これは、日本語と英語を翻訳するようなものです。Pythonの辞書（dictionary）とJSONは形が似ていますが微妙に違うので、変換が必要なんです。

### requestsライブラリとJSON：便利なセット

requestsライブラリは、APIからのレスポンス（返答）をJSONとして簡単に扱う機能があります：

1. **JSONレスポンスの取得**:
   ```python
   response = requests.get('https://jsonplaceholder.typicode.com/users/1')
   user_data = response.json()  # レスポンスをJSONとして解析し、Pythonの辞書に変換
   ```

2. **JSONデータの送信**:
   ```python
   # jsonパラメータを使うと、PythonのデータをJSONに自動変換してくれる便利機能
   data = {"name": "新しいユーザー", "email": "newuser@example.com"}
   response = requests.post('https://jsonplaceholder.typicode.com/posts', json=data)
   ```

### なぜAPIでJSONがよく使われるの？

APIでJSONが大人気の理由は次の通り：

1. **読みやすさ**: テキストなので、人間が直接見ても理解できる（デバッグが楽）
2. **構造化**: 複雑な階層構造も表現できる（入れ子になったデータが扱える）
3. **軽量**: データ量が少なく、通信が速い（特にモバイル通信に向いている）
4. **どこでも使える**: どんなプログラミング言語でも扱える（言語間の架け橋）
5. **ウェブとの相性**: ブラウザでそのまま使える（特にJavaScriptと相性抜群）

つまり、JSONはデータ交換の「万能翻訳者」のような役割を果たしているのです。

## 基本的なAPI呼び出し（GETリクエスト）

さっそくPythonからJSONPlaceholderのAPIを呼び出してみましょう！まずは最も基本的な「GET」リクエストからです。

GETリクエストは、「情報をください」とお願いするようなものです。お店で「この商品について教えてください」と尋ねるイメージですね。

```python
import requests

# JSONPlaceholderのユーザー情報APIにGETリクエストを送信
# （まるで「ユーザー情報をください」と丁寧にお願いするようなもの）
response = requests.get('https://jsonplaceholder.typicode.com/users')

# ステータスコードの確認（200は「はい、どうぞ！」という成功のしるし）
print(f"ステータスコード: {response.status_code}")

# レスポンスの内容（JSON形式）を表示
users = response.json()
print(f"取得したユーザー数: {len(users)}")

# 最初のユーザー情報を表示（配列の0番目の要素）
first_user = users[0]
print("\n最初のユーザー情報:")
print(f"名前: {first_user['name']}")
print(f"ユーザー名: {first_user['username']}")
print(f"メール: {first_user['email']}")
print(f"住所: {first_user['address']['street']}, {first_user['address']['city']}")
print(f"会社: {first_user['company']['name']}")
```

### 実行結果の例

```
ステータスコード: 200
取得したユーザー数: 10

最初のユーザー情報:
名前: Leanne Graham
ユーザー名: Bret
メール: Sincere@april.biz
住所: Kulas Light, Gwenborough
会社: Romaguera-Crona
```

### コードの解説

1. `import requests`: まず道具箱（requestsライブラリ）を開けます
2. `requests.get()`: 指定したURLに「情報をください」とリクエストを送ります
3. `response.status_code`: 返ってきた結果の状態を数字で確認します（200は成功！）
4. `response.json()`: 返ってきたJSONデータをPythonで使える形に変換します
5. あとは欲しい情報を取り出して表示しています（辞書から値を取り出すイメージ）

## 特定のユーザー情報を取得する

APIのエンドポイント（アクセス先のURL）にIDを指定すると、特定のユーザーだけの情報を取得できます。これは、「5番の人の情報だけください」とピンポイントでお願いするようなものです：

```python
import requests

# ユーザーID 5の情報だけを取得（5番目のユーザーを指名）
user_id = 5
response = requests.get(f'https://jsonplaceholder.typicode.com/users/{user_id}')

# レスポンスの確認
if response.status_code == 200:
    user = response.json()
    print(f"ユーザーID {user_id} の情報:")
    print(f"名前: {user['name']}")
    print(f"メール: {user['email']}")
    print(f"電話: {user['phone']}")
    print(f"ウェブサイト: {user['website']}")
else:
    print(f"エラー: ステータスコード {response.status_code}")
```

このコードは、図書館で「5番の本だけ見せてください」と頼むようなものです。全部の本を見る必要はなく、必要な1冊だけをピンポイントで取得できます！

## 投稿データを取得する

ユーザー以外にも、投稿データも取得できます。これは「今度は本ではなく、雑誌のコーナーを見せてください」と場所を変えるようなものです：

```python
import requests

# 投稿データを取得（最初の10件）
response = requests.get('https://jsonplaceholder.typicode.com/posts?_limit=10')

posts = response.json()
print(f"取得した投稿数: {len(posts)}")

# 最初の投稿を表示
first_post = posts[0]
print("\n最初の投稿:")
print(f"タイトル: {first_post['title']}")
print(f"内容: {first_post['body']}")
print(f"投稿者ID: {first_post['userId']}")
```

## POSTリクエスト（新しいデータの作成）

次はPOSTリクエストを試してみましょう。これは「新しいデータを作ってください」とお願いするものです。

お店で例えると「新しい商品を追加してください」と注文するようなイメージですね。

```python
import requests

# 新しい投稿データを作成（これから送る新しい情報）
new_post = {
    'title': '新しい投稿のタイトル',
    'body': 'これは新しい投稿の本文です。わくわくするような内容を書きました！',
    'userId': 1
}

# POSTリクエストを送信（「これを追加してください」というお願い）
response = requests.post(
    'https://jsonplaceholder.typicode.com/posts',
    json=new_post  # jsonパラメータを使うとPythonの辞書をJSONに変換してくれる
)

# レスポンスの確認
print(f"ステータスコード: {response.status_code}")  # 201は「作成成功」を意味する

# 作成された投稿データを表示
created_post = response.json()
print("\n作成された投稿:")
print(f"ID: {created_post['id']}")
print(f"タイトル: {created_post['title']}")
print(f"内容: {created_post['body']}")
print(f"投稿者ID: {created_post['userId']}")
```

### 実行結果の例

```
ステータスコード: 201

作成された投稿:
ID: 101
タイトル: 新しい投稿のタイトル
内容: これは新しい投稿の本文です。わくわくするような内容を書きました！
投稿者ID: 1
```

> 📝 **ポイント**: ステータスコード201は「作成成功」を意味します。200（単なる成功）とは少し違うんですよ。細かいけど大事なポイントです！

> 📝 **実験用の注意**: JSONPlaceholderはテスト用なので、実際にはデータが保存されません。でも、ちゃんと保存されたかのように反応してくれるので、APIの使い方の練習にはぴったりです！

## PUTリクエスト（データの更新）

既存のデータを更新するには、PUTリクエストを使います。これは「この内容に書き換えてください」とお願いするようなものです。

例えると、図書館の本の内容を修正するようなイメージですね。

```python
import requests

# 更新するデータ（ID:1の投稿の内容を書き換える）
updated_post = {
    'id': 1,
    'title': '更新されたタイトル',
    'body': 'これは更新された本文です。前よりもっと良い内容になりました！',
    'userId': 1
}

# PUTリクエストを送信
response = requests.put(
    'https://jsonplaceholder.typicode.com/posts/1',
    json=updated_post
)

# レスポンスの確認
print(f"ステータスコード: {response.status_code}")

# 更新された投稿データを表示
updated = response.json()
print("\n更新された投稿:")
print(f"ID: {updated['id']}")
print(f"タイトル: {updated['title']}")
print(f"内容: {updated['body']}")
```

PUTリクエストは「全部書き換え」のイメージです。一部だけ変更したい場合は、PATCHというリクエストも使えますよ（今回は説明を省略します）。

## DELETEリクエスト（データの削除）

データを削除するには、DELETEリクエストを使います。これは「このデータを削除してください」とお願いするものです。

例えると、図書館から古い本を処分するようなイメージですね。

```python
import requests

# 削除するデータのID
post_id = 1

# DELETEリクエストを送信
response = requests.delete(f'https://jsonplaceholder.typicode.com/posts/{post_id}')

# レスポンスの確認
print(f"ステータスコード: {response.status_code}")
print(f"投稿ID {post_id} が削除されました。")
```

DELETEリクエストはシンプルで、削除したいリソースのIDをURLで指定するだけです。特に送るデータ（本文）はありません。

## エラーハンドリング

APIリクエストでは様々なエラーが発生する可能性があります。実際のアプリケーション開発では、これらのエラーを適切に処理することが非常に重要です。まるで、料理中に起こるかもしれないミスに備えるようなものですね！

### APIリクエスト時の主なエラータイプ

requestsライブラリを使う際に発生する可能性のある主なエラーをご紹介します：

1. **HTTPエラー (4xx/5xx)**: サーバーからのエラーレスポンス
   - 400 Bad Request: リクエストの形式が間違っている（料理の注文書の書き方が間違っているようなもの）
   - 401 Unauthorized: 認証が必要（会員証がないとサービスが受けられないようなもの）
   - 403 Forbidden: アクセス権限がない（立入禁止の部屋に入ろうとしているようなもの）
   - 404 Not Found: リソースが見つからない（存在しない本を図書館で探すようなもの）
   - 500 Internal Server Error: サーバー内部エラー（お店のキッチンで問題が起きているようなもの）

2. **接続エラー (ConnectionError)**:
   - サーバーに接続できない（お店が閉まっているようなもの）
   - DNSエラー（お店の住所が間違っているようなもの）
   - ネットワーク接続の問題（道路が工事中で行けないようなもの）

3. **タイムアウト (Timeout)**:
   - 接続タイムアウト: サーバーへの接続に時間がかかりすぎた（電話がずっと繋がらないようなもの）
   - 読み込みタイムアウト: レスポンスの受信に時間がかかりすぎた（注文した料理がいつまでも出てこないようなもの）

4. **JSONデコードエラー (ValueError)**:
   - レスポンスが有効なJSON形式でない（もらった手紙が読めない言語で書かれているようなもの）

### エラーハンドリングの実装方法

以下のコードは、上記のエラータイプを適切に処理する方法を示しています：

```python
import requests

try:
    # 存在しないエンドポイントにアクセス（存在しないお店にお願いするようなもの）
    response = requests.get(
        'https://jsonplaceholder.typicode.com/invalid_endpoint',
        timeout=5  # タイムアウトを5秒に設定（5秒待ってもレスポンスがなければあきらめる）
    )

    # ステータスコードのチェック
    response.raise_for_status()  # 4xx/5xxエラーの場合、例外を発生させる

    # 正常なレスポンスの処理
    data = response.json()
    print("データの取得に成功しました。")

except requests.exceptions.HTTPError as err:
    # HTTPエラー（4xx/5xxステータスコード）
    print(f"HTTPエラー: {err}")
    print(f"ステータスコード: {response.status_code}")

    # エラーコードに応じた処理
    if response.status_code == 404:
        print("リソースが見つかりませんでした。URLを確認してください。")
    elif response.status_code == 401:
        print("認証が必要です。APIキーや認証情報を確認してください。")
    elif response.status_code == 429:
        print("リクエスト制限を超えました。しばらく待ってからリトライしてください。")

except requests.exceptions.ConnectionError as err:
    # 接続エラー（サーバーに接続できない）
    print(f"接続エラー: {err}")
    print("サーバーに接続できませんでした。以下を確認してください：")
    print("- インターネット接続が正常か")
    print("- サーバーのURLが正しいか")
    print("- サーバーが稼働しているか")

except requests.exceptions.Timeout as err:
    # タイムアウトエラー
    print(f"タイムアウト: {err}")
    print("リクエストがタイムアウトしました。以下を試してください：")
    print("- タイムアウト時間を長くする")
    print("- ネットワーク接続を確認する")
    print("- サーバーの負荷状況を確認する")

except requests.exceptions.RequestException as err:
    # その他のrequests関連エラー（上記以外の全てのrequestsエラーのベースクラス）
    print(f"リクエストエラー: {err}")
    print("APIリクエスト中に予期しないエラーが発生しました。")

except ValueError as err:
    # JSONデコードエラー
    print(f"JSONエラー: {err}")
    print("レスポンスをJSONとして解析できませんでした。レスポンスの内容を確認します：")
    print(response.text[:200])  # レスポンスの先頭部分を表示

except Exception as err:
    # その他の予期しないエラー
    print(f"予期しないエラー: {err}")
```

### エラーハンドリングのベストプラクティス

1. **具体的な例外から先に処理する**:
   - より具体的な例外（HTTPError）から先にキャッチし、より一般的な例外（RequestException）を後にキャッチします。
   - これは、「風邪の症状」より「発熱」という具体的な症状を先に確認するようなものです。

2. **タイムアウトを設定する**:
   ```python
   # タイムアウトを設定（接続タイムアウト, 読み込みタイムアウト）
   response = requests.get('https://example.com', timeout=(3, 10))
   ```
   これは、「3秒以内に電話に出ないと切る」「注文して10分以上料理が来ないと店員さんに確認する」というようなものです。

3. **リトライメカニズムの実装**:
   ```python
   # シンプルなリトライ実装
   for attempt in range(3):
       try:
           response = requests.get('https://example.com', timeout=5)
           response.raise_for_status()
           return response.json()
       except (requests.exceptions.RequestException, ValueError) as err:
           print(f"エラー発生（試行 {attempt+1}/3）: {err}")
           if attempt < 2:  # 最後の試行ではリトライしない
               import time
               time.sleep(2)  # 2秒待機してからリトライ
   return None  # すべての試行が失敗
   ```
   これは、「一度失敗しても、最大3回まで挑戦してみる」というもので、友達に電話がつながらなくても、しばらく待ってからかけ直すようなものです。

4. **ロギングを活用する**:
   ```python
   import logging

   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   try:
       response = requests.get('https://example.com')
       response.raise_for_status()
   except requests.exceptions.RequestException as err:
       logger.error(f"APIリクエストエラー: {err}")
   ```
   これは、何か問題が起きたときに記録を残して、後から確認できるようにするものです。日記をつけるようなイメージですね。

### エラーハンドリングの重要性

実際のプロジェクトでは、エラーハンドリングが適切に行われていないと以下の問題が発生する可能性があります：

- アプリケーションが突然止まる（ゲームが突然クラッシュするようなもの）
- ユーザーに不親切なエラーメッセージが表示される（「エラーコード0x80004005」だけ表示されて何のことかわからない、みたいな）
- 問題の原因追求が難しくなる（どこで何が起きたのかわからない）
- システムの安全性に問題が生じる（鍵のかかっていないドアのようなもの）

エラーハンドリングは、頑丈で信頼性の高いアプリケーションを作るための重要な要素です。まるで、料理の失敗に備えた心構えと代替案を持っておくようなものですね！

## クエリパラメータの使用

APIでは、クエリパラメータを使って検索や絞り込みを行うことができます。これは、お店で「赤色の商品だけ見せてください」「価格が安い順に並べてください」とお願いするようなものです：

```python
import requests

# クエリパラメータを使って投稿を検索（特別なお願い付きで検索）
params = {
    'userId': 1,      # ユーザーID 1 の投稿のみを取得（この人が書いた記事だけ）
    '_sort': 'id',    # ID順にソート（番号順に並べる）
    '_order': 'desc', # 降順（大きい番号から表示）
    '_limit': 5       # 最大5件まで取得（最初の5件だけ見せて）
}

response = requests.get(
    'https://jsonplaceholder.typicode.com/posts',
    params=params  # クエリパラメータを指定
)

# 結果の表示
posts = response.json()
print(f"取得した投稿数: {len(posts)}")
print(f"リクエストURL: {response.url}")  # 実際のURLを表示

# 各投稿のタイトルを表示
print("\n取得した投稿:")
for post in posts:
    print(f"ID {post['id']}: {post['title']}")
```

クエリパラメータは、図書館で「2000年以降に出版された料理の本だけ、人気順に5冊見せてください」とお願いするような便利な機能です。一度に大量のデータを取得するのではなく、必要な部分だけをピンポイントで取得できます！

## ヘッダーの追加とAPI認証

実際のAPIを利用する際は、認証情報やメタデータをリクエストヘッダーに含める必要があることが多くあります。これは、お店に入るときに会員証を見せるようなものです。

### 基本的なヘッダーの追加

```python
import requests

# 基本的なヘッダー情報を設定（自己紹介シートのようなもの）
headers = {
    'User-Agent': 'MyPythonApp/1.0',       # アプリケーション識別子（私は〇〇というアプリです）
    'Accept': 'application/json',           # レスポンスで受け取りたい形式（JSONで返してください）
    'Content-Type': 'application/json',     # 送信するデータの形式（私からの情報もJSONです）
    'X-Custom-Header': 'CustomValue'        # カスタムヘッダー（特別な情報）
}

# ヘッダーを付けてリクエスト（身分証明書を持ってお店に行く）
response = requests.get(
    'https://jsonplaceholder.typicode.com/users',
    headers=headers
)

# レスポンスヘッダーの表示（お店からの返事に含まれる情報）
print("レスポンスヘッダー:")
for header, value in response.headers.items():
    print(f"{header}: {value}")

# コンテンツタイプの確認
print(f"\nコンテンツタイプ: {response.headers.get('Content-Type')}")
```

### APIキー認証の例

多くのAPIでは、APIキーを使った認証が一般的です。これは特別な会員番号のようなもので、ヘッダーまたはクエリパラメータとして渡すことができます。

```python
import requests

# APIキーをヘッダーに設定する例（会員証をポケットに入れておく）
api_key = "your_api_key_12345"
headers = {
    'X-API-Key': api_key,  # APIサービスによって名前は異なる
    'Accept': 'application/json'
}

# 天気予報APIの例（架空のAPI）
response = requests.get(
    'https://api.example-weather.com/v1/forecast',
    headers=headers,
    params={'city': 'Tokyo', 'days': 5}
)

# APIキーをURLクエリパラメータとして設定する例（会員番号を見えるところに付ける）
params = {
    'api_key': api_key,
    'city': 'Tokyo',
    'days': 5
}
response = requests.get('https://api.example-weather.com/v1/forecast', params=params)

print(f"ステータスコード: {response.status_code}")
# 注: 実際のAPIキーは厳重に管理し、ソースコードには直接記載しないでください
```

### セッションの利用：繰り返しのリクエストを効率化

```python
# requestsのSessionを使うと、ヘッダーやクッキーを複数リクエストで共有できる
# （同じお店で何度も買い物するとき、毎回会員証を出す手間が省ける）
session = requests.Session()
session.headers.update({'Authorization': f'Bearer {api_key}'})

# 同じセッション内の複数リクエスト
response1 = session.get('https://api.example.com/endpoint1')
response2 = session.post('https://api.example.com/endpoint2', json=data)
```

ヘッダーを適切に設定することで、APIアクセスの認証、データ形式の指定、カスタム情報の送信など、様々な処理をコントロールすることができます。特に認証関連のヘッダーは、多くのAPIで必須となるため、正しく実装することが重要です。

## 実践的なアプリケーション例（穴埋め問題）

以上の知識を組み合わせて、ユーザーとその投稿を一覧表示する簡単なアプリケーションを作ってみましょう。以下は穴埋め問題になっています。コメントを参考に、空欄（`# TODO:`）を埋めてみてください：

```python
import requests

def get_user(user_id):
    """指定されたIDのユーザー情報を取得する"""
    # TODO: user_idを使って、JSONPlaceholderからユーザー情報を取得するGETリクエストを実装する
    # ヒント: エンドポイントは 'https://jsonplaceholder.typicode.com/users/{user_id}' 形式

    # TODO: ステータスコードが200の場合、JSONレスポンスを返す。それ以外はNoneを返す

def get_posts_by_user(user_id):
    """指定されたユーザーIDの投稿を取得する"""
    # TODO: クエリパラメータを使って、特定ユーザーの投稿を取得する
    # ヒント: paramsに適切なキーと値のペアを設定する

    # TODO: GETリクエストを送信し、ステータスコードが200の場合はJSONレスポンスを返す
    # それ以外の場合は空のリストを返す

def display_user_with_posts(user_id):
    """ユーザー情報とその投稿を表示する"""
    # ユーザー情報の取得
    # TODO: get_user関数を呼び出してユーザー情報を取得する

    # TODO: ユーザーが見つからない場合のエラーメッセージを表示して関数を終了する

    # ユーザー情報の表示
    print(f"\n===== ユーザー情報 =====")
    print(f"名前: {user['name']}")
    print(f"ユーザー名: {user['username']}")
    print(f"メール: {user['email']}")
    print(f"会社: {user['company']['name']}")

    # ユーザーの投稿を取得して表示
    # TODO: get_posts_by_user関数を呼び出してユーザーの投稿を取得する

    print(f"\n===== {user['name']} の投稿 ({len(posts)}件) =====")

    for i, post in enumerate(posts, 1):
        print(f"\n投稿 {i}:")
        print(f"タイトル: {post['title']}")
        print(f"本文: {post['body'][:100]}..." if len(post['body']) > 100 else post['body'])
        print("-" * 50)

# メイン処理
if __name__ == "__main__":
    # ユーザーID 3の情報と投稿を表示
    display_user_with_posts(3)
```

### 実行結果の例

この穴埋め問題を正しく解くと、以下のような出力が得られます：

```
===== ユーザー情報 =====
名前: Clementine Bauch
ユーザー名: Samantha
メール: Nathan@yesenia.net
会社: Romaguera-Jacobson

===== Clementine Bauch の投稿 (10件) =====

投稿 1:
タイトル: optio molestias id quia eum
本文: quo et expedita modi cum officia vel magni
doloribus qui repudiandae
vero nisi sit
quos veniam quod sed ac...
--------------------------------------------------

投稿 2:
タイトル: et ea vero quia laudantium autem
本文: delectus reiciendis molestiae occaecati non minima eveniet qui voluptatibus
accusamus in eum beatae s...
--------------------------------------------------

[以下省略]
```

### 解答例

穴埋め問題の解答は自分で考えてみることをお勧めしますが、どうしても分からない場合はインターネットで検索するか、前のセクションで学んだことを復習してみてください。学びは挑戦から始まります！

## Pydanticモデルでデータをスマートに扱おう！

APIから取得したJSONデータを扱う時、少し困ったことはありませんか？例えば、次のような悩みがあるかもしれません：

- データの型が正しいか確認するのが面倒
- キーの存在チェックを毎回書くのが大変
- 辞書のネストが深いとアクセスしづらい
- データの構造が分かりにくい

そんな時に便利なのが「Pydantic」というライブラリです。Pydanticを使うと、JSONデータを簡単にPythonのクラスに変換でき、より直感的にデータを扱えるようになります。

### Pydanticとは？

Pydanticは、データの検証と設定管理のためのライブラリです。まるで「データの型を守る優秀な番人」のようなものです。特徴は以下の通りです：

- データの型を自動的に検証してくれる
- 必要なデータが欠けていないか確認してくれる
- JSONデータを簡単にPythonのクラスに変換できる
- コード補完が効くので使いやすい

### Pydanticを使ってみよう

まずはPydanticをインストールしましょう：

```bash
pip install pydantic
```

次に、JSONPlaceholderのユーザーデータのモデルを作ってみましょう：

```python
from pydantic import BaseModel
from typing import List, Optional

# 住所のモデル（ネストされたデータ）
class Geo(BaseModel):
    lat: str
    lng: str

class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo

# 会社のモデル
class Company(BaseModel):
    name: str
    catchPhrase: str
    bs: str

# ユーザーのモデル
class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: Address
    phone: str
    website: str
    company: Company
```

このように、データの構造を明確に定義できます。まるで「設計図」のようなものですね。

### Pydanticモデルの使用例

では、実際にJSONPlaceholderからデータを取得し、Pydanticモデルに変換してみましょう：

```python
import requests
from pydantic import BaseModel, Field
from typing import List, Optional

# 投稿のモデル
class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str

# ユーザーのシンプルなモデル（必要な情報だけ定義）
class User(BaseModel):
    id: int
    name: str
    email: str
    username: str
    
    # カスタムフィールド名も定義できる
    company_name: str = Field(alias="company")
    
    # モデルの設定
    model_config = {
        # JSONのデータ構造を柔軟に扱う設定
        "populate_by_name": True,
        
        # エイリアスを使う場合の設定
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "ユーザー名",
                "email": "user@example.com",
                "username": "user1",
                "company": {"name": "会社名"}
            }
        }
    }

# JSONPlaceholderからユーザーデータを取得
response = requests.get('https://jsonplaceholder.typicode.com/users/1')
user_data = response.json()

# Pydanticモデルに変換
try:
    # UserモデルのインスタンスにJSONデータを変換
    user = User.model_validate({
        "id": user_data["id"],
        "name": user_data["name"],
        "email": user_data["email"],
        "username": user_data["username"],
        "company": user_data["company"]["name"]
    })
    
    print(f"ユーザー情報（Pydanticモデル）:")
    print(f"ID: {user.id}")
    print(f"名前: {user.name}")
    print(f"メール: {user.email}")
    print(f"会社名: {user.company_name}")
    
    # 投稿データを取得
    posts_response = requests.get(f'https://jsonplaceholder.typicode.com/posts?userId={user.id}&_limit=3')
    posts_data = posts_response.json()
    
    # 複数の投稿をPydanticモデルに変換
    posts = [Post.model_validate(post) for post in posts_data]
    
    # ヘルパー関数（モデルの外で定義）
    def get_short_body(text: str, length: int = 50) -> str:
        """本文の短縮版を返す"""
        if len(text) <= length:
            return text
        return text[:length] + "..."
    
    print(f"\n{user.name}の投稿（Pydanticモデル）:")
    for i, post in enumerate(posts, 1):
        print(f"\n投稿 {i}:")
        print(f"タイトル: {post.title}")
        print(f"本文（短縮）: {get_short_body(post.body)}")  # ヘルパー関数を使用
        
except Exception as e:
    print(f"エラー: {e}")
```

### 実行結果の例

```
ユーザー情報（Pydanticモデル）:
ID: 1
名前: Leanne Graham
メール: Sincere@april.biz
会社名: Romaguera-Crona

Leanne Grahamの投稿（Pydanticモデル）:

投稿 1:
タイトル: sunt aut facere repellat provident occaecati excepturi optio reprehenderit
本文（短縮）: quia et suscipit
suscipit recusandae consequuntur ...

投稿 2:
タイトル: qui est esse
本文（短縮）: est rerum tempore vitae
sequi sint nihil reprehend...

投稿 3:
タイトル: ea molestias quasi exercitationem repellat qui ipsa sit aut
本文（短縮）: et iusto sed quo iure
voluptatem occaecati omnis e...
```

### Pydanticの正しい使い方

Pydanticモデルは主にデータの構造定義と検証のためのものです。良い設計では、モデル自体には複雑なロジックを含めず、データの整合性を保証することに集中します。これは「単一責任の原則」という考え方に基づいています。

#### モデルとビジネスロジックの分離

Pydanticモデルに複雑な処理や表示ロジックを入れるのではなく、それらは別の場所で定義するのが良い習慣です：

```python
# モデル定義（データ構造と検証のみに集中）
class User(BaseModel):
    id: int
    name: str
    is_active: bool = True  # デフォルト値

# ユーティリティ関数（モデルの外で定義）
def format_user_name(user: User) -> str:
    """ユーザー名を整形して表示する"""
    return f"{user.name} {'(アクティブ)' if user.is_active else '(非アクティブ)'}"

# 使用例
user = User(id=1, name="田中太郎")
print(format_user_name(user))  # 田中太郎 (アクティブ)
```

この方法には以下のメリットがあります：
- モデルがシンプルで理解しやすくなる
- テストが容易になる
- 同じデータに対して異なる処理方法を柔軟に追加できる

### Pydanticの便利な機能

Pydanticには他にも便利な機能がたくさんあります：

1. **デフォルト値の設定**:
   ```python
   class User(BaseModel):
       id: int
       name: str
       is_active: bool = True  # デフォルト値
   ```

2. **バリデーション（値の検証）**:
   ```python
   from pydantic import BaseModel, EmailStr, Field
   
   class User(BaseModel):
       name: str = Field(min_length=2)  # 少なくとも2文字必要
       age: int = Field(ge=0, lt=120)   # 0以上120未満
       email: str  # EmailStrを使用するには追加のパッケージが必要
   ```

3. **JSONへの変換**:
   ```python
   user_json = user.model_dump_json()
   print(user_json)  # {"id": 1, "name": "Leanne Graham", ...}
   ```

### 実践問題：Pydanticモデルで投稿管理アプリを作ろう

次のコードを完成させて、Pydanticモデルを使った投稿管理アプリを作ってみましょう。

```python
import requests
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# TODO: 投稿（Post）のPydanticモデルを定義する
# 必要なフィールド: id, title, body, userId
# 追加で「created_at」というフィールドを追加し、現在の日時を自動的に設定するようにする


# TODO: ユーザー（User）のPydanticモデルを定義する
# 必要なフィールド: id, name, username, email
# email フィールドに対して単純な検証（@が含まれているか）を追加する


# JSONPlaceholderからデータを取得して、Pydanticモデルに変換する関数
def get_user_with_posts(user_id: int):
    # ユーザー情報の取得
    # TODO: Pydanticモデルを使ってユーザー情報を取得・変換する処理を実装する

    
    # ユーザーの投稿を取得
    # TODO: Pydanticモデルを使ってユーザーの投稿を取得・変換する処理を実装する

    
    # 投稿を表示
    # TODO: Pydanticモデルの属性を使って結果を表示する処理を実装する
    # ヒント: 短縮本文はモデルの外で処理する（ユーティリティ関数を作成）


# メイン処理
if __name__ == "__main__":
    # ユーザーID 2の情報と投稿を表示
    get_user_with_posts(2)
```

この問題を解くことで、Pydanticモデルの基本的な使い方が学べます。自分で考えてみることをお勧めしますが、どうしても分からない場合は、上述の例を参考にしてみてください。

Pydanticを使うと、APIから取得したデータをより安全かつ直感的に操作できるようになります。まるで「データに型と構造を与える魔法」のようですね！

実際のプロジェクトでは、こうしたモデル定義を活用することで、コードの可読性と保守性が大幅に向上します。ぜひ、様々なAPIを使ったプロジェクトでPydanticを活用してみてください。

## まとめ

今回は、Pythonのrequestsライブラリを使ってJSONPlaceholderのAPIにアクセスする方法を学びました！

- **requestsライブラリ**のインストールと基本的な使い方
- **GET**, **POST**, **PUT**, **DELETE**などの**HTTPメソッド**の使い方（いろんなお願いの方法）
- **JSONデータ**の取得と解析（特別な形式のメッセージの読み解き方）
- **クエリパラメータ**や**ヘッダー**の設定方法（詳細な注文方法）
- **エラーハンドリング**の方法（問題が起きたときの対処法）
- 実践的なアプリケーション例（実際に使ってみる練習）

これらの知識を活用すれば、様々なWebAPIに接続してデータを取得・操作することができます。次のステップとしては、実際の公開APIを使ったプロジェクトに挑戦してみてはいかがでしょうか？例えば、天気予報API、映画情報API、ニュースAPIなど、多くの無料・有料APIが利用可能です。

APIとPythonを使いこなせるようになれば、世界中のデータやサービスとつながったアプリケーションが開発できるようになります。まるでインターネットの魔法使いのような存在になれるのです。✨

## 参考リンク

- [requests公式ドキュメント](https://docs.python-requests.org/)
- [JSONPlaceholder公式サイト](https://jsonplaceholder.typicode.com/)
- [PythonでのAPI利用についての詳細ガイド](https://realpython.com/api-integration-in-python/)