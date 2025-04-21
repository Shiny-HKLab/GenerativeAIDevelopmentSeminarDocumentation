[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shiny-HKLab/GenerativeAIDevelopmentSeminarDocumentation/blob/main/section02-jsonplaceholder/notebook-colab.ipynb)

# Python + requestsライブラリでjsonplaceholderでAPIを試してみよう！

## はじめに

前回はAPIの基本的な概念について学びました。今回は実際にPythonを使ってWebAPIにアクセスする方法を見ていきましょう。

> 📝 **補足**: APIにはさまざまな種類がありますが、今回扱うのは「WebAPI」です。現代のシステム開発（ChatGPTの機能をアプリに組み込むなど）では、主にこのWebAPIが使われています。一般的に「API」と言えば「WebAPI」を指すことが多いので覚えておきましょう。

## 今回使用するツール

1. **Python**: プログラミング言語
2. **requestsライブラリ**: PythonでHTTPリクエストを簡単に行うためのライブラリ
3. **JSONPlaceholder**: テスト用の無料WebAPIサービス

## JSONPlaceholderとは？

[JSONPlaceholder](https://jsonplaceholder.typicode.com/)は、APIのテストや学習に最適な無料のダミーAPIサービスです。特徴は以下の通りです：

- 登録不要で誰でも利用可能
- ユーザー情報、投稿、コメントなどのダミーデータを提供
- GET, POST, PUT, DELETEなどの様々なHTTPメソッドをテスト可能
- 実際のAPIの動作を模擬体験できる

## JSONとは何か？

### JSONの基本概念

**JSON (JavaScript Object Notation)** は、データを交換するための軽量なテキスト形式です。APIでデータをやり取りする際に最もよく使われる形式の一つです。

JSONの特徴：
- 人間が読み書きしやすい
- プログラムが解析・生成しやすい
- 言語に依存しない（ほぼすべてのプログラミング言語でJSONを扱えます）
- Webアプリケーションでのデータ交換に最適

### JSONデータの構造

JSONデータは以下の2つの構造を基本として構成されます：

1. **オブジェクト（Object）**: 名前と値のペアの集まり
   - 波括弧 `{}` で囲みます
   - `"キー": 値` の形式で記述します
   - キーは必ず文字列（ダブルクォート `"` で囲む）
   - 複数のキーと値のペアはカンマ `,` で区切ります

2. **配列（Array）**: 値の順序付きリスト
   - 角括弧 `[]` で囲みます
   - 値はカンマ `,` で区切ります

### JSONで使えるデータ型

JSONでは以下のデータ型を使用できます：

- **文字列（String）**: `"こんにちは"`, `"Hello"` など（ダブルクォートで囲む）
- **数値（Number）**: `10`, `3.14`, `-20` など
- **真偽値（Boolean）**: `true` または `false`
- **null**: `null`（値が存在しないことを表す）
- **オブジェクト（Object）**: `{"name": "田中", "age": 30}`
- **配列（Array）**: `[1, 2, 3, 4, 5]`, `["りんご", "みかん", "バナナ"]`

### JSONの実例

以下は、ユーザー情報を表すJSONの例です：

```json
{
  "id": 1,
  "name": "田中太郎",
  "email": "tanaka@example.com",
  "age": 28,
  "isActive": true,
  "hobbies": ["読書", "映画鑑賞", "旅行"],
  "address": {
    "city": "東京",
    "zipcode": "100-0001"
  }
}
```

この例では：
- オブジェクト（`{}`）の中に様々なデータが含まれています
- `name`, `email` などのキー（プロパティ名）とその値のペアがあります
- `hobbies` は配列（`[]`）で、複数の文字列値を持っています
- `address` は入れ子になったオブジェクトです

### PythonでJSONを扱う

Pythonでは、標準ライブラリの `json` モジュールを使ってJSONデータを扱うことができます：

```python
import json

# Pythonの辞書（dict）をJSON文字列に変換（シリアライズ）
python_dict = {
    "name": "田中太郎",
    "age": 28,
    "hobbies": ["読書", "映画鑑賞"]
}
json_str = json.dumps(python_dict, ensure_ascii=False)
print(json_str)
# 出力: {"name": "田中太郎", "age": 28, "hobbies": ["読書", "映画鑑賞"]}

# JSON文字列をPythonの辞書に変換（デシリアライズ）
json_data = '{"name": "鈴木花子", "age": 25}'
python_obj = json.loads(json_data)
print(python_obj["name"])  # 出力: 鈴木花子
print(python_obj["age"])   # 出力: 25
```

### requestsライブラリとJSON

requestsライブラリは、APIからのレスポンスをJSONとして扱う便利なメソッドを提供しています：

1. **JSONレスポンスの取得**:
   ```python
   response = requests.get('https://jsonplaceholder.typicode.com/users/1')
   user_data = response.json()  # レスポンスをJSONとして解析し、Pythonの辞書に変換
   ```

2. **JSONデータの送信**:
   ```python
   # 方法1: jsonパラメータを使用（推奨）
   data = {"name": "新しいユーザー", "email": "newuser@example.com"}
   response = requests.post('https://example.com/api/users', json=data)

   # 方法2: データをJSON文字列に変換して送信
   import json
   data = {"name": "新しいユーザー", "email": "newuser@example.com"}
   headers = {'Content-Type': 'application/json'}
   response = requests.post(
       'https://example.com/api/users',
       data=json.dumps(data),
       headers=headers
   )
   ```

### なぜAPIでJSONを使うのか？

APIでJSONが広く使われる理由は以下の通りです：

1. **テキストベース**: プレーンテキストなので、人間が読みやすく、デバッグしやすい
2. **構造化**: 階層的なデータ構造を表現できる
3. **軽量**: XMLなど他の形式と比べてデータサイズが小さい
4. **クロスプラットフォーム**: 言語やシステムに依存しない
5. **JavaScript互換**: ウェブブラウザで直接使える（JSON = JavaScript Object Notation）

このように、JSONはAPIを通じてデータをやり取りする際の「共通言語」として機能し、異なるシステム間でのデータ交換を容易にします。


## 基本的なAPI呼び出し（GETリクエスト）

さっそくPythonからJSONPlaceholderのAPIを呼び出してみましょう。まずは最も基本的なGETリクエストを使ってユーザー情報を取得します。

```python
import requests

# JSONPlaceholderのユーザー情報APIにGETリクエストを送信
response = requests.get('https://jsonplaceholder.typicode.com/users')

# ステータスコードの確認
print(f"ステータスコード: {response.status_code}")

# レスポンスの内容（JSON形式）を表示
users = response.json()
print(f"取得したユーザー数: {len(users)}")

# 最初のユーザー情報を表示
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

1. `import requests`: requestsライブラリをインポートします
2. `requests.get()`: 指定したURLに対してGETリクエストを送信します
3. `response.status_code`: HTTPステータスコードを取得します（200は成功を意味します）
4. `response.json()`: レスポンスをJSON形式で解析し、Pythonのリスト/辞書に変換します
5. 取得したデータから必要な情報を抽出して表示しています

## 特定のユーザー情報を取得する

APIのエンドポイントにIDを指定することで、特定のユーザー情報だけを取得することもできます：

```python
import requests

# ユーザーID 5の情報を取得
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

## 投稿データを取得する

ユーザーだけでなく、投稿データも取得できます：

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

GETだけでなく、POSTリクエストを使って新しいデータを作成することもできます：

```python
import requests
import json

# 新しい投稿データを作成
new_post = {
    'title': '新しい投稿のタイトル',
    'body': 'これは新しい投稿の本文です。',
    'userId': 1
}

# POSTリクエストを送信
response = requests.post(
    'https://jsonplaceholder.typicode.com/posts',
    json=new_post  # jsonパラメータを使うとPythonの辞書をJSONに変換してくれる
)

# レスポンスの確認
print(f"ステータスコード: {response.status_code}")

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
内容: これは新しい投稿の本文です。
投稿者ID: 1
```

> 📝 **注意**: JSONPlaceholderはテスト用APIなので、実際にはデータが保存されません。しかし、リクエストが成功すると、作成されたかのようにレスポンスが返ってきます。

## PUTリクエスト（データの更新）

既存のデータを更新するには、PUTリクエストを使います：

```python
import requests

# 更新するデータ
updated_post = {
    'id': 1,
    'title': '更新されたタイトル',
    'body': 'これは更新された本文です。',
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

## DELETEリクエスト（データの削除）

データを削除するには、DELETEリクエストを使います：

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

## エラーハンドリング

APIリクエストでは様々なエラーが発生する可能性があります。実際のアプリケーション開発では、これらのエラーを適切に処理することが非常に重要です。

### APIリクエスト時の主なエラータイプ

requestsライブラリを使う際に発生する可能性のある主なエラーは以下の通りです：

1. **HTTPエラー (4xx/5xx)**: サーバーからのエラーレスポンス
   - 400 Bad Request: リクエストの形式が不正
   - 401 Unauthorized: 認証が必要
   - 403 Forbidden: アクセス権限がない
   - 404 Not Found: リソースが見つからない
   - 500 Internal Server Error: サーバー内部エラー

2. **接続エラー (ConnectionError)**:
   - サーバーに接続できない
   - DNSエラー
   - ネットワーク接続の問題

3. **タイムアウト (Timeout)**:
   - 接続タイムアウト: サーバーへの接続に時間がかかりすぎた
   - 読み込みタイムアウト: レスポンスの受信に時間がかかりすぎた

4. **JSONデコードエラー (ValueError)**:
   - レスポンスが有効なJSON形式でない

### エラーハンドリングの実装方法

以下のコードは、上記のエラータイプを適切に処理する方法を示しています：

```python
import requests

try:
    # 存在しないエンドポイントにアクセス
    response = requests.get(
        'https://jsonplaceholder.typicode.com/invalid_endpoint',
        timeout=5  # タイムアウトを5秒に設定
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

2. **タイムアウトを設定する**:
   ```python
   # タイムアウトを設定（接続タイムアウト, 読み込みタイムアウト）
   response = requests.get('https://example.com', timeout=(3, 10))
   ```

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

### エラーハンドリングの重要性

実際のプロジェクトでは、エラーハンドリングが適切に行われていないと以下の問題が発生する可能性があります：

- アプリケーションがクラッシュする
- ユーザーに不適切なエラーメッセージが表示される
- デバッグが困難になる
- システムのセキュリティリスクが高まる

適切なエラーハンドリングは、堅牢なアプリケーション開発において非常に重要な要素です。

## クエリパラメータの使用

APIでは、クエリパラメータを使って検索や絞り込みを行うことができます：

```python
import requests

# クエリパラメータを使って投稿を検索
params = {
    'userId': 1,      # ユーザーID 1 の投稿のみを取得
    '_sort': 'id',    # ID順にソート
    '_order': 'desc', # 降順
    '_limit': 5       # 最大5件まで取得
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

## ヘッダーの追加とAPI認証

実際のAPIを利用する際は、認証情報やメタデータをリクエストヘッダーに含める必要があることが多くあります。ここでは、一般的なヘッダーの追加方法と、様々な認証パターンの実装方法を見ていきましょう。

### 基本的なヘッダーの追加

```python
import requests

# 基本的なヘッダー情報を設定
headers = {
    'User-Agent': 'MyPythonApp/1.0',       # アプリケーション識別子
    'Accept': 'application/json',           # レスポンスで受け取りたい形式
    'Content-Type': 'application/json',     # 送信するデータの形式
    'X-Custom-Header': 'CustomValue'        # カスタムヘッダー
}

# ヘッダーを付けてリクエスト
response = requests.get(
    'https://jsonplaceholder.typicode.com/users',
    headers=headers
)

# レスポンスヘッダーの表示
print("レスポンスヘッダー:")
for header, value in response.headers.items():
    print(f"{header}: {value}")

# コンテンツタイプの確認
print(f"\nコンテンツタイプ: {response.headers.get('Content-Type')}")
```

### APIキー認証の例

多くのAPIでは、APIキーを使った認証が一般的です。APIキーはヘッダーまたはクエリパラメータとして渡すことができます。

```python
import requests

# APIキーをヘッダーに設定する例
api_key = "your_api_key_12345"
headers = {
    'X-API-Key': api_key,  # APIサービスによって名前は異なる（X-API-Key, api-key, apikey など）
    'Accept': 'application/json'
}

# 天気予報APIの例（架空のAPI）
response = requests.get(
    'https://api.example-weather.com/v1/forecast',
    headers=headers,
    params={'city': 'Tokyo', 'days': 5}
)

# APIキーをURLクエリパラメータとして設定する例
params = {
    'api_key': api_key,
    'city': 'Tokyo',
    'days': 5
}
response = requests.get('https://api.example-weather.com/v1/forecast', params=params)

print(f"ステータスコード: {response.status_code}")
# 注: 実際のAPIキーは厳重に管理し、ソースコードには直接記載しないでください
```

### Bearer トークン認証（OAuth2など）

OAuth2などで使われるBearer認証の例です。多くのモダンなAPIで採用されています。

```python
import requests

# アクセストークン（OAuth2認証などで取得）
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6..."

# Bearer認証ヘッダーを設定
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# 保護されたエンドポイントにアクセス
response = requests.get(
    'https://api.example.com/v1/user/profile',
    headers=headers
)

# エラーチェック
if response.status_code == 200:
    user_data = response.json()
    print(f"ユーザー名: {user_data.get('name')}")
    print(f"メールアドレス: {user_data.get('email')}")
elif response.status_code == 401:
    print("認証エラー: トークンが無効か期限切れです")
    # トークンのリフレッシュ処理などを実装
elif response.status_code == 403:
    print("権限エラー: このリソースにアクセスする権限がありません")
else:
    print(f"エラー: {response.status_code}")
```

### Basic認証の例

Basic認証は、ユーザー名とパスワードをBase64でエンコードして送信する古典的な認証方式です。

```python
import requests
from requests.auth import HTTPBasicAuth

username = "api_user"
password = "api_password"

# 方法1: HTTPBasicAuthクラスを使用（推奨）
response = requests.get(
    'https://api.example.com/v1/secure-data',
    auth=HTTPBasicAuth(username, password)
)

# 方法2: 直接ヘッダーに設定する方法（推奨されない）
import base64
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
headers = {
    'Authorization': f'Basic {credentials}'
}
response = requests.get('https://api.example.com/v1/secure-data', headers=headers)

print(f"ステータスコード: {response.status_code}")
```

### 実際のAPIサービスでのヘッダー使用例

#### GitHub API

```python
import requests

# GitHubのパーソナルアクセストークン
github_token = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# GitHubの推奨ヘッダー
headers = {
    'Authorization': f'token {github_token}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'MyGitHubApp'  # GitHubはUser-Agentを必須としています
}

# GitHub APIでリポジトリ情報を取得
response = requests.get(
    'https://api.github.com/repos/python/cpython',
    headers=headers
)

if response.status_code == 200:
    repo = response.json()
    print(f"リポジトリ名: {repo['full_name']}")
    print(f"スター数: {repo['stargazers_count']}")
    print(f"フォーク数: {repo['forks_count']}")
else:
    print(f"エラー: {response.status_code}")
    print(response.json())
```

#### OpenAI API（ChatGPT API）

```python
import requests
import json

# OpenAI APIキー
api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# OpenAI APIのヘッダー
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# 送信するデータ
data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "あなたは役立つアシスタントです。"},
        {"role": "user", "content": "こんにちは、簡単なPythonのコード例を教えてください。"}
    ]
}

# OpenAI APIにリクエスト
response = requests.post(
    'https://api.openai.com/v1/chat/completions',
    headers=headers,
    data=json.dumps(data)
)

if response.status_code == 200:
    result = response.json()
    print("ChatGPTの応答:")
    print(result['choices'][0]['message']['content'])
else:
    print(f"エラー: {response.status_code}")
    print(response.text)
```

### ヘッダー設定のベストプラクティス

1. **認証情報の保護**:
   ```python
   # 環境変数から認証情報を読み込む（セキュリティ対策）
   import os
   api_key = os.environ.get('API_KEY')
   ```

2. **ヘッダーの再利用**:
   ```python
   # 認証ヘッダーを設定するヘルパー関数
   def get_auth_headers(api_key):
       return {
           'Authorization': f'Bearer {api_key}',
           'Content-Type': 'application/json',
           'Accept': 'application/json'
       }

   # 複数のリクエストで再利用
   headers = get_auth_headers(api_key)
   response1 = requests.get('https://api.example.com/endpoint1', headers=headers)
   response2 = requests.post('https://api.example.com/endpoint2', headers=headers, json=data)
   ```

3. **セッションの利用**:
   ```python
   # requestsのSessionを使うと、ヘッダーやクッキーを複数リクエストで共有できる
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

穴埋め問題の解答は自分で考えてみることをお勧めしますが、詳しい解説が必要な場合は次のセクションを参照してください。

## まとめ

今回は、Pythonのrequestsライブラリを使ってJSONPlaceholderのAPIにアクセスする方法を学びました。

- **requestsライブラリ**のインストールと基本的な使い方
- **GET**, **POST**, **PUT**, **DELETE**などの**HTTPメソッド**の使い方
- **JSONデータ**の取得と解析
- **クエリパラメータ**や**ヘッダー**の設定方法
- **エラーハンドリング**の方法
- 実践的なアプリケーション例

これらの知識を活用すれば、様々なWebAPIに接続してデータを取得・操作することができます。次のステップとしては、実際の公開APIを使ったプロジェクトに挑戦してみてはいかがでしょうか？例えば、天気予報API、映画情報API、ニュースAPIなど、多くの無料・有料APIが利用可能です。

また、自分でAPI認証を実装したり、より複雑なデータ操作を行ったりするスキルも身につけていくと良いでしょう。

APIとPythonを使いこなせるようになれば、さまざまなサービスやデータと連携したアプリケーションが開発できるようになります！

## 参考リンク

- [requests公式ドキュメント](https://docs.python-requests.org/)
- [JSONPlaceholder公式サイト](https://jsonplaceholder.typicode.com/)
- [PythonでのAPI利用についての詳細ガイド](https://realpython.com/api-integration-in-python/)