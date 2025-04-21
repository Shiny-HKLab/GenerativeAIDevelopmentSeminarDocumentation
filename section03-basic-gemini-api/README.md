# PythonでGemini APIを実行してAIを動かす！ requestsと最新SDK (google-genai)、それぞれの方法を徹底解説

生成AIの進化は目覚ましく、私たちの開発にAIの機能を組み込む機会も増えています。Googleが提供する高性能な大規模言語モデルであるGeminiも、そのAPIを利用することで、Pythonアプリケーションから手軽に操作できます。

この記事では、「PythonでGemini APIを実行し、AIの応答をコンソールで出力させる」ことを目標に、以下の2つの方法を解説します。

1. Python標準ライブラリrequestsを使用して直接APIを呼び出す方法
2. Google公式の最新Python SDK (google-genai) を利用する方法

まずはAPIの基礎を理解するためにrequestsを使った方法を学び、その後に推奨される最新SDKを利用してより簡単に記述できる方法を見ていきます。それぞれのメリット・デメリットも比較し、状況に応じて最適な方法を選択できるようになりましょう。

## 事前準備：APIキーの取得

Gemini APIを利用するには、APIキーが必要です。まだ取得していない場合は、以下の手順で取得してください。

1. [Google AI Studio](https://aistudio.google.com/) にアクセスします。
2. Googleアカウントでログインします。
3. 左メニューの「Get API key」を選択します。
4. 「Create API key in new project」をクリックすると、APIキーが生成されます。

生成されたAPIキーは、後ほどコードで使用しますので控えておいてください。APIキーは重要な情報なので、公開したり、直接コードに埋め込んだりせず、環境変数などで管理することを強く推奨します。 今回の記事では解説の都合上コード内に記述する場合がありますが、実際の開発ではご注意ください。

## 方法1：requestsライブラリでGemini APIを実行する

まずは、PythonでHTTPリクエストを送信するための標準的なライブラリであるrequestsを使って、直接Gemini APIを呼び出してみましょう。この方法では、APIがどのように動作しているかの理解が深まります。

### インストール

requestsライブラリは、以下のコマンドでインストールできます。

```bash
pip install requests
```

### APIの呼び出し方

Gemini APIのエンドポイントに対して、HTTP POSTリクエストを送信します。リクエストのURL、ヘッダー、ボディには、APIキー、使用するモデル、プロンプト（AIへの指示）などの情報を含めます。

基本となるAPIエンドポイントは以下の形式です。

```
https://generativelanguage.googleapis.com/v1beta/models/{model-id}:generateContent
```

`{model-id}`には、使用したいGeminiモデルのID（例: gemini-pro）が入ります。APIキーは、URLのクエリパラメータとして`key=YOUR_API_KEY`の形式で渡します。

リクエストボディはJSON形式で、以下のような構造になります。

```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "ここにプロンプトを入力"
        }
      ]
    }
  ]
}
```

応答もJSON形式で返ってきます。生成されたテキストは、応答ボディの`candidates -> 最初の要素 -> content -> parts -> 最初の要素 -> text` の階層に格納されています。

### 通常出力（バッチ処理）

まずは、リクエストを送信して、応答がすべて返ってくるのを待つ通常出力の方法です。

```python
import requests
import json
import os # APIキーを環境変数から読み込む場合

# あなたのAPIキーに置き換えてください（環境変数からの読み込みを推奨）
# API_KEY = os.environ.get("YOUR_GEMINI_API_KEY")
API_KEY = "YOUR_YOUR_GEMINI_API_KEY" # 直接記述する場合

MODEL_ID = "gemini-pro"
API_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent"

def generate_text_batch_requests(prompt):
    headers = {
        'Content-Type': 'application/json',
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    params = {
        'key': API_KEY
    }

    try:
        response = requests.post(API_ENDPOINT, headers=headers, params=params, data=json.dumps(payload))
        response.raise_for_status() # HTTPエラーがあれば例外を発生させる

        response_data = response.json()

        # 応答からテキストを抽出
        if 'candidates' in response_data and response_data['candidates']:
            first_candidate = response_data['candidates'][0]
            if 'content' in first_candidate and 'parts' in first_candidate['content'] and first_candidate['content']['parts']:
                first_part = first_candidate['content']['parts'][0]
                if 'text' in first_part:
                    return first_part['text']

        return "応答からテキストを抽出できませんでした。"

    except requests.exceptions.RequestException as e:
        print(f"APIリクエスト中にエラーが発生しました: {e}")
        return None
    except json.JSONDecodeError:
        print("応答のJSONパースに失敗しました。")
        # エラー時の応答内容を確認する
        if 'response' in locals() and response.text:
             print("応答内容:", response.text)
        return None
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        return None


# 実行例
prompt = "PythonでHTTPリクエストを送信する方法を教えてください。"
print("--- requests バッチ出力 ---")
generated_text = generate_text_batch_requests(prompt)
if generated_text:
    print(generated_text)
```

このコードでは、`requests.post`メソッドを使ってAPIにリクエストを送信し、返ってきたJSONデータをパースして、生成されたテキスト部分を取り出しています。`response.raise_for_status()`を使うことで、4xxや5xxのエラーレスポンスがあった場合に例外を発生させ、エラーハンドリングをしやすくしています。

### ストリーミング出力（requests）

大量のテキスト生成や、リアルタイムな応答表示を行いたい場合は、ストリーミング出力が便利です。APIがテキストを生成する傍から、少しずつ応答を受け取ることができます。

requestsでストリーミングを行うには、`requests.post`の際に`stream=True`オプションを指定し、応答オブジェクトをイテレートします。Gemini APIのストリーミング応答は、一般的にServer-Sent Events (SSE) の形式に似ており、`data: `の後にJSONデータが続く形で送られてきます。各チャンク（断片）には、生成されたテキストの続きが含まれています。

```python
import requests
import json
import os

# あなたのAPIキーに置き換えてください（環境変数からの読み込みを推奨）
# API_KEY = os.environ.get("YOUR_GEMINI_API_KEY")
API_KEY = "YOUR_YOUR_GEMINI_API_KEY" # 直接記述する場合

MODEL_ID = "gemini-pro"
# ストリーミング用のエンドポイントは通常出力と同じです
API_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent"

def generate_text_stream_requests(prompt):
    headers = {
        'Content-Type': 'application/json',
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    params = {
        'key': API_KEY
    }

    print("\n--- requests ストリーミング出力 ---")
    try:
        # stream=True を指定してリクエストを送信
        with requests.post(API_ENDPOINT, headers=headers, params=params, data=json.dumps(payload), stream=True) as response:
            response.raise_for_status() # HTTPエラーがあれば例外を発生させる

            # 応答を1行ずつ読み込み、'data:'で始まる行を処理
            for line in response.iter_lines():
                if line: # 空行をスキップ
                    decoded_line = line.decode('utf-8')
                    # SSE形式の 'data: ' を取り除く
                    if decoded_line.startswith('data: '):
                        json_data_str = decoded_line[len('data: '):].strip()
                        if json_data_str:
                            try:
                                chunk_data = json.loads(json_data_str)

                                # チャンクからテキスト部分を抽出して出力
                                # ストリーミングチャンクもバッチ応答と似た構造を持つ
                                if 'candidates' in chunk_data and chunk_data['candidates']:
                                    first_candidate = chunk_data['candidates'][0]
                                    if 'content' in first_candidate and 'parts' in first_candidate['content'] and first_candidate['content']['parts']:
                                        first_part = first_candidate['content']['parts'][0]
                                        if 'text' in first_part:
                                            print(first_part['text'], end='', flush=True) # 逐次出力

                            except json.JSONDecodeError:
                                print(f"\nWarning: チャンクのJSONパースに失敗しました: {json_data_str}")
                            except Exception as e:
                                print(f"\nWarning: チャンク処理中に予期しないエラーが発生しました: {e}")

            print("\n--- requests ストリーミング完了 ---") # 終了を示す

    except requests.exceptions.RequestException as e:
        print(f"\nAPIリクエスト中にエラーが発生しました: {e}")
    except Exception as e:
        print(f"\n予期しないエラーが発生しました: {e}")


# 実行例
prompt = "日本の首都について詳しく教えてください。"
generate_text_stream_requests(prompt)
```

ストリーミング出力では、`response.iter_lines()`を使って応答を一行ずつ読み込みます。各行が`data:`で始まる場合は、その後のJSONデータをパースし、テキスト部分を取り出してすぐにコンソールに出力しています。`end=''`と`flush=True`を指定することで、改行せずに逐次表示されるようにしています。この手動でのパース処理が必要になる点が、SDKとの大きな違いです。

### requestsを使うメリット・デメリット

**メリット:**

- Python標準ライブラリとrequestsだけで実装できるため、外部ライブラリへの依存が少ない。
- APIの生のリクエスト・レスポンスを確認できるため、APIの動作原理の理解が深まる。
- 細かなHTTPリクエストの設定（タイムアウト、プロキシなど）を直接制御できる。

**デメリット:**

- リクエストURLの構築、JSONボディの作成、応答のパース、エラーハンドリングなど、APIの仕様に合わせて自分で記述する必要がある。
- 特にストリーミング応答の解析（`data:`の除去、JSONパース）が煩雑になりがち。
- APIのバージョンアップや仕様変更があった場合、コードの修正が必要になる可能性が高い。
- 会話履歴の管理、埋め込み生成、安全設定などの高度な機能を利用する際に、すべて自分で実装する必要がある。

## 方法2：Google公式最新Python SDK (google-genai) でGemini APIを実行する

Googleが提供している公式の最新Python SDK (google-genai) を利用すると、APIへのアクセスが非常に簡単になります。SDKはAPIの複雑な部分を抽象化し、Pythonオブジェクトとして操作できるように設計されています。

> **注意**: 以前の google-generativeai ライブラリは非推奨となりました。今後は google-genai を使用してください。

### インストール

最新SDKは以下のコマンドでインストールできます。

```bash
pip install google-genai
```

### APIの呼び出し方

SDKを使用する場合、まずAPIキーを設定し、次に利用したいモデルを指定してインスタンスを作成します。プロンプトを渡すだけで、テキスト生成などの操作が直感的に行えます。

```python
import genai # google-genai ライブラリは genai という名前でインポートします
import os

# あなたのAPIキーに置き換えてください（環境変数からの読み込みを推奨）
# 環境変数 GOOGLE_API_KEY に設定する方法が推奨されます
# API_KEY = os.environ.get("GOOGLE_API_KEY")
API_KEY = "YOUR_YOUR_GEMINI_API_KEY" # 直接記述する場合

# APIキーを設定
# 環境変数 GOOGLE_API_KEY が設定されていれば省略可能
genai.configure(api_key=API_KEY)

# 使用するモデルを指定してGenerativeModelインスタンスを作成
model = genai.GenerativeModel('gemini-pro')

def generate_text_batch_sdk(prompt):
    try:
        # テキスト生成を実行（バッチ）
        response = model.generate_content(prompt)

        # 応答からテキストを抽出
        # SDKは通常、生成されたテキストをresponse.textで取得できます
        # ただし、安全フィルタに引っかかった場合などはエラーや空になる可能性あり
        if response.text:
            return response.text
        else:
            # テキストが生成されなかった場合の診断情報を表示
            print("\nテキストが生成されませんでした。詳細:")
            if response.prompt_feedback:
                print("  プロンプトフィードバック:", response.prompt_feedback)
            if response.candidates:
                print("  候補:", response.candidates)
            return "テキスト生成に失敗したか、内容がブロックされました。"


    except Exception as e:
        print(f"SDKでのバッチAPIリクエスト中にエラーが発生しました: {e}")
        return None

# 実行例
prompt = "世界の三大珍味は何ですか？"
print("\n--- SDK (`google-genai`) バッチ出力 ---")
generated_text = generate_text_batch_sdk(prompt)
if generated_text:
    print(generated_text)
```

SDKを使うと、わずか数行のコードでテキスト生成が実行できることがわかります。応答オブジェクト(`response`)には、生成されたテキスト以外にも、安全性に関する情報(`prompt_feedback`, `candidates[i].safety_ratings`)などが含まれており、これらも簡単にアクセスできます。`response.text`で生成されたテキスト部分に直接アクセスできるのが便利です。テキストが生成されなかった（例えば安全設定でブロックされた）場合なども考慮したエラーハンドリングを追加しています。

APIキーは、`genai.configure(api_key=API_KEY)` で設定するか、環境変数 `GOOGLE_API_KEY` に設定しておくことでも自動的に読み込まれます。

### ストリーミング出力（SDK google-genai）

SDKでもストリーミング出力は非常に簡単です。`generate_content`メソッドに`stream=True`引数を追加し、返ってきた応答オブジェクトを`for`ループで回すだけです。

```python
import genai # google-genai ライブラリは genai という名前でインポートします
import os

# あなたのAPIキーに置き換えてください（環境変数からの読み込みを推奨）
# 環境変数 GOOGLE_API_KEY に設定する方法が推奨されます
# API_KEY = os.environ.get("GOOGLE_API_KEY")
API_KEY = "YOUR_YOUR_GEMINI_API_KEY" # 直接記述する場合

# APIキーを設定
# 環境変数 GOOGLE_API_KEY が設定されていれば省略可能
genai.configure(api_key=API_KEY)

# 使用するモデルを指定してGenerativeModelインスタンスを作成
model = genai.GenerativeModel('gemini-pro')

def generate_text_stream_sdk(prompt):
    print("\n--- SDK (`google-genai`) ストリーミング出力 ---")
    try:
        # テキスト生成を実行（ストリーミング）
        response = model.generate_content(prompt, stream=True)

        # 応答オブジェクトをイテレートして、チャンクを順次出力
        # SDKはストリーミングチャンクからtext属性で簡単にアクセスできる
        for chunk in response:
            if chunk.text:
                 print(chunk.text, end='', flush=True)

        print("\n--- SDK (`google-genai`) ストリーミング完了 ---") # 終了を示す

    except Exception as e:
        print(f"\nSDKでのストリーミングAPIリクエスト中にエラーが発生しました: {e}")
        # ストリーミングの場合、エラー情報はイテレーション中に発生する可能性がある
        # 終了後にresponseオブジェクトを確認することも可能だが、リアルタイムのエラーハンドリングは別途検討
        # if response.prompt_feedback: print("プロンプトフィードバック:", response.prompt_feedback)


# 実行例
prompt = "夕食のメニューについて提案をいくつかください。"
generate_text_stream_sdk(prompt)
```

SDKのストリーミングは、requestsでの実装と比較して、はるかにシンプルです。応答オブジェクトがイテラブルになっており、`for`ループで回すだけで各チャンクのテキスト部分にアクセスできます。内部的には、requestsを使った場合と同様にHTTPストリームを処理し、JSONをパースしてくれています。

## requestsとSDK (google-genai) の比較

| 項目 | requestsライブラリ | Python SDK (google-genai) |
|------|-------------------|--------------------------|
| 実装の容易さ | 低い（手動でHTTPリクエストを構築・解析） | 高い（直感的で簡単なAPI呼び出し） |
| コード量 | 多い | 少ない |
| API理解 | 深い（HTTPリクエスト・レスポンスを直接扱う） | 浅い（抽象化されている） |
| ストリーミング | 手動での応答解析（data:処理、JSONパース）が必要 | SDKが自動的に処理し、イテレートするだけ |
| エラーハンドリング | 手動でHTTPステータスコードや応答ボディを確認する必要あり | SDKに組み込まれたエラー処理や、応答オブジェクトからの情報取得が容易 |
| 機能 | 基本的なAPI呼び出しのみ | 会話履歴管理、安全設定、埋め込み、ファンクションコーリングなど高度な機能をサポート |
| メンテナンス | API仕様変更の影響を受けやすい | SDKの更新で対応されることが多い |
| 依存関係 | requestsのみ（比較的少ない） | google-genai SDKへの依存が発生 |
| 推奨度 | APIの仕組み理解や特殊な用途向け | 推奨（Google公式の推奨ライブラリ） |

## まとめ

この記事では、PythonからGemini APIを使ってAIと連携する方法を、requestsライブラリと最新の公式SDK (google-genai) の両面から解説しました。

requestsを使った方法は、APIの基本的な仕組みを理解するのに役立ち、細かい制御が可能ですが、実装の手間がかかります。特にストリーミング処理は、応答形式に合わせて丁寧にコードを書く必要があります。

一方、公式Python SDK (google-genai) を使う方法は、APIの複雑さを吸収してくれるため、コードが非常にシンプルで分かりやすくなります。テキスト生成だけでなく、会話履歴の管理や安全設定などの高度な機能も容易に扱えます。また、公式ライブラリとして継続的にメンテナンスされ、APIの更新にも追従していくことが期待できます。

特別な理由がない限り、Gemini APIを利用したPython開発では公式Python SDK (google-genai) を使用することを強く推奨します。 より少ないコードで、堅牢かつ機能豊富なアプリケーションを開発できます。しかし、APIの挙動を深く理解したい場合や、SDKに依存したくない特定の要件がある場合には、requestsで直接APIを呼び出す方法も有効な選択肢となります。

これらの知識を元に、ぜひPythonアプリケーションにGeminiの強力なAI機能を組み込んでみてください。