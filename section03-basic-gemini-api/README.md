# 初心者のためのGoogle Gen AI SDK入門
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shiny-HKLab/GenerativeAIDevelopmentSeminarDocumentation/blob/main/section03-basic-gemini-api/notebook.ipynb)

このセクションでは、Google Gen AI SDKの使い方を解説します。AIを使って文章を生成したり、チャットボットを作ったりする方法を学んでいきましょう。

## 1. Google Gen AI SDKって何？

Google Gen AI SDKは、Googleが提供する人工知能（AI）のツールキットです。このツールキットを使うと、「Gemini」という高性能なAIモデルを自分のプログラムで簡単に使えるようになります。

考えてみてください。友達と話したり、質問に答えてもらったり、物語を作ってもらったりするAIを、自分のプログラムに組み込めるとしたら、どんなことができるでしょうか？それを実現するのが、このSDKなのです。

> 💡 **SDKとは？**
> SDK（Software Development Kit）とは、ソフトウェアを開発するための道具箱のようなものです。プログラマーがアプリやサービスを作るときに便利な機能がまとまっています。

## 2. インストールと準備

### インストール方法

Google Gen AI SDKをインストールするのは、とても簡単です。コマンドプロンプトやターミナルで、以下のコマンドを実行するだけです。

```bash
pip install google-genai
```

これで、必要なファイルがパソコンにダウンロードされ、Pythonから使えるようになります。

### APIキーの取得

AIを使うには、「APIキー」というパスワードのようなものが必要です。これは、あなたがGoogleのAIサービスを利用する権利があることを証明するものです。

1. [Google AI Studioのウェブサイト](https://aistudio.google.com/)にアクセスします
2. Googleアカウントでログインします
3. 「APIキーを取得」または「Get API Key」というボタンを探して、クリックします
4. 表示されたAPIキーをメモしておきます（他の人には教えないでください！）

### 基本的なセットアップ

さあ、最初のプログラムを書いてみましょう。まずは、Google Gen AI SDKをインポートして、APIキーを設定します。

#### 直接APIキーを設定する方法

```python
from google import genai

# APIキーを設定
client = genai.Client(api_key='ここにあなたのAPIキーを入力してください')
```

#### 環境変数の設定（ローカル環境の場合）

別の方法として、環境変数に設定する方法もあります。

```bash
# Windowsの場合
set GOOGLE_API_KEY=あなたのAPIキー

# MacやLinuxの場合
export GOOGLE_API_KEY=あなたのAPIキー
```

そして、Pythonでは次のように書きます。

```python
from google import genai

# 環境変数からAPIキーを取得
client = genai.Client()
```

#### 環境変数の設定（Google Colabの場合）

Google Colabを使用する場合は、以下の手順でAPIキーを安全に設定できます：

1. Google ColabのシークレットタブからGoogle APIキーの「Google AI Studioでキーを管理」という項目をクリックしてGemini APIキーの管理画面に移動します
2. 管理画面から「APIキーの作成」を行い、APIキーを追加します
3. Google Colabに戻り、シークレットタブからGoogle APIキーの「Google AI Studioからキーをインポート」をクリックして先ほど追加したAPIキーを選択します
4. シークレットタブに「GOOGLE_API_KEY」という名前が追加されているのを確認したら以下のセルを実行し、エラーが発生しないことを確認してください

```python
from google.colab import userdata

GOOGLE_API_KEY = userdata.get("GOOGLE_API_KEY")
assert GOOGLE_API_KEY is not None
```

その後、以下のようにクライアントを作成します：

```python
from google import genai
from google.colab import userdata

# Google ColabのシークレットからAPIキーを取得
api_key = userdata.get("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)
```

これで、Google Gen AI SDKを使う準備が整いました！

## 3. テキスト生成の基本

### シンプルなテキスト生成

最初に挑戦するのは、AIに文章を生成してもらうことです。例えば、「空が青い理由」について説明してもらいましょう。

```python
from google import genai

# クライアントを作成
client = genai.Client(api_key='あなたのAPIキー')

# AIに質問する
response = client.models.generate_content(
    model='gemini-2.0-flash',  # 使用するAIモデル
    contents='空が青い理由を教えてください'  # AIへの指示
)

# 結果を表示
print(response.text)
```

**出力例：**
```
空が青い理由は「レイリー散乱」という現象によるものです。太陽の光は、さまざまな色（波長）の光が混ざっています。この光が地球の大気中の分子にぶつかると、短い波長の光（青色や紫色）ほど強く散乱されます。

青色光は紫色光よりも私たちの目に感じやすく、また大気中の散乱も多いため、空を見上げると青く見えるのです。これが空が青く見える主な理由です。

夕焼けが赤く見えるのは、太陽光が大気中を通る距離が長くなり、青色光がほとんど散乱されてしまい、散乱されにくい赤色光だけが残るためです。
```

このコードを実行すると、AIが「空が青い理由」について説明してくれます。すごいですね！

> 💡 **モデルとは？**
> ここでの「モデル」とは、AIの種類や能力のことです。例えば「gemini-2.0-flash」は、速度を重視したAIモデルです。用途に応じて、より賢い「gemini-2.0-pro-001」などを選ぶこともできます。

### もう少し複雑な例

AIに物語を作ってもらうこともできます。

```python
from google import genai

client = genai.Client(api_key='あなたのAPIキー')

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='猫と犬が友達になる短い物語を書いてください'
)

print(response.text)
```

**出力例：**
```
# 違いを超えて

ミケは裏庭の塀の上でのんびりと日向ぼっこをしていました。この家に越してきて一週間。まだ周りの環境に慣れていない彼女は、警戒心を抱きながらも、新しい縄張りを探検していました。

そんなある日、隣の家から元気な吠え声が聞こえてきました。「ワン！ワン！」

塀の向こう側には、茶色い大きな犬が尻尾を振りながら立っていました。ミケは背中の毛を逆立て、シャーッと威嚇しました。

「こんにちは！僕の名前はパックだよ。君は新しい隣人なんだね！」犬は友好的に言いました。

最初はお互いに距離を保っていた二匹でしたが、日が経つにつれ、塀越しの会話が増えていきました。パックはミケに公園での冒険について話し、ミケはパックに木登りのコツを教えました。

ある雨の日、ミケは雨宿りをしようと急いでいたところ、水たまりに足を取られて転んでしまいました。困っていると、パックが駆けつけ、自分の体で雨をさえぎり、ミケを家まで送り届けました。

それ以来、二匹は種族の違いを超えた親友になりました。日向ぼっこをするときも、お昼寝をするときも、いつも一緒。ミケとパックは、友情に境界線がないことを、ご近所中に証明して見せたのでした。
```

このように、AIにさまざまな指示を出すことができます。例えば、レシピの提案、問題の解決方法、プログラミングのコード例など、多くのことをAIに頼むことができます。

## 4. 従来のrequestsライブラリとの比較

Google Gen AI SDKの便利さを理解するために、従来のrequestsライブラリを使う方法と比較してみましょう。

### requestsライブラリでの実装

```python
import requests
import json

# APIキー
api_key = 'あなたのAPIキー'

# APIエンドポイント
url = 'https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent'

# ヘッダー
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

# リクエストボディ
data = {
    'contents': [
        {
            'parts': [
                {
                    'text': '空が青い理由を教えてください'
                }
            ]
        }
    ]
}

# リクエストを送信
response = requests.post(
    f'{url}?key={api_key}',
    headers=headers,
    data=json.dumps(data)
)

# レスポンスを処理
if response.status_code == 200:
    response_json = response.json()
    try:
        print(response_json['candidates'][0]['content']['parts'][0]['text'])
    except (KeyError, IndexError):
        print('テキストの取得に失敗しました')
else:
    print(f'エラー: {response.status_code}')
    print(response.text)
```

### Google Gen AI SDKでの実装

```python
from google import genai

# クライアントを作成
client = genai.Client(api_key='あなたのAPIキー')

# AIに質問する
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='空が青い理由を教えてください'
)

# 結果を表示
print(response.text)
```

### 比較からわかること

1. **コードの量**: Google Gen AI SDKを使うと、コードがとても短くなります！
2. **わかりやすさ**: 複雑なJSON構造やHTTPリクエストの詳細を気にする必要がありません
3. **エラー処理**: SDKには便利なエラー処理機能が組み込まれています
4. **機能の充実**: ストリーミングやチャットなど、高度な機能が簡単に使えます

SDKを使うと、AI関連の複雑な処理を簡単なコード数行で実現できるので、初心者の方にもおすすめです！

## 5. 設定パラメータの概要

AIの出力をより細かく制御したい場合は、「設定パラメータ」を使います。これは、AIがどのように応答するかを調整する方法です。

### 温度（Temperature）

「温度」は、AIの創造性を調整するパラメータです。値が低いと（0に近いと）予測可能で安定した回答になり、値が高いと（1に近いと）より創造的でバラエティに富んだ回答になります。

```python
from google import genai
from google.genai import types

client = genai.Client(api_key='あなたのAPIキー')

# 温度を0.3に設定（安定した回答）
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='面白い冗談を1つ教えてください',
    config=types.GenerateContentConfig(
        temperature=0.3,
    ),
)

print(response.text)
```

**出力例（temperature=0.3）:**
```
なぜプログラマーはメガネをかけるのでしょうか？

セミコロン（;）が見えないからです！
```

同じ質問でも温度を変えると...

```python
# 温度を0.9に設定（創造的な回答）
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='面白い冗談を1つ教えてください',
    config=types.GenerateContentConfig(
        temperature=0.9,
    ),
)

print(response.text)
```

**出力例（temperature=0.9）:**
```
私の冷蔵庫が最近、ある物を欲しがっているんです。

「それは何？」と友達が聞きました。

私は答えました。「よくわからないんだ。でもドアにずっとメモが貼ってあって『ミルクを買ってきて』って書いてあるんだよ」
```

### 最大出力トークン数

AIの回答の長さを制限したい場合は、「max_output_tokens」を設定します。

```python
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='春について詳しく説明してください',
    config=types.GenerateContentConfig(
        max_output_tokens=50,  # 約50単語の回答に制限
    ),
)

print(response.text)
```

**出力例：**
```
春は四季の中で冬と夏の間にある季節です。温度が上昇し始め、植物が新しい生命を育み始める時期です。多くの植物が芽吹き、花が咲き始め、鮮やかな色彩で世界を彩ります。
```

### システム指示（System Instruction）

AIに特定の役割や振る舞いを指示したい場合は、「system_instruction」を使います。

```python
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='ピザの作り方を教えてください',
    config=types.GenerateContentConfig(
        system_instruction='あなたはプロのイタリアンシェフです。料理の説明をするときは、専門的なアドバイスも含めてください。',
    ),
)

print(response.text)
```

**出力例：**
```
# 本格ピザの作り方

## 生地（パスタ・マードレ）
- 強力粉（タイプ00が理想的）: 500g
- 水（常温）: 300ml
- 塩: 小さじ1
- ドライイースト: 5g
- オリーブオイル（エクストラバージン）: 大さじ1

## ソース（スーゴ）
- サンマルツァーノトマト（缶詰）: 400g
- にんにく: 2片
- バジリコ（フレッシュ）: 数枚
- オリーブオイル: 大さじ2
- 塩: 小さじ1/2

## 手順

### 生地作り（一晩前の準備が理想的）
1. ボウルに強力粉を入れ、中央に窪みを作ります。
2. 水にイーストを溶かし、少しずつ粉に加えながら混ぜていきます。
3. 塩とオリーブオイルを加え、滑らかになるまで10分ほど捏ねます。
4. **プロの技**: 生地を伸ばして折りたたむ動作を繰り返すことで、グルテンネットワークが発達し、弾力のある生地になります。
5. ボウルに戻し、湿らせた布をかけて、室温で2時間、または冷蔵庫で8〜24時間発酵させます。
6. **重要**: 長時間の低温発酵がナポリピッツァの風味を生み出す秘訣です。

### ソース作り
1. オリーブオイルでみじん切りにしたにんにくを弱火で香りが出るまで炒めます。
2. トマトを手で潰しながら加え、弱火で20分ほど煮詰めます。
3. **プロの技**: トマトソースは濃厚すぎると焼いたときに焦げやすくなるので、やや水分を残しておきましょう。
4. 最後に刻んだバジリコと塩で味を調えます。

### 仕上げと焼成
1. 発酵した生地を打ち粉をした台の上で、外側から中心に向かって優しく押し広げます。
2. **プロの技**: 生地を伸ばす際は、中央を薄く、外側をやや厚めに残すと、エッジが美しく膨らみます（コルニチョーネ）。
3. ソースを薄く塗り、モッツァレラチーズをちぎって散らします。
4. 最高温度に予熱したオーブン（家庭用なら250℃以上）で6〜8分焼きます。
5. **理想的環境**: 本格的なピッツァには450℃以上の石窯が理想的です。家庭では、ピザストーンを使用すると熱伝導が良くなります。

出来立てのピッツァには、フレッシュバジリコの葉と高品質のエクストラバージンオリーブオイルを少量かけて香りを引き立てましょう。真のナポリピッツァは中心が少し柔らかく、エッジは香ばしいのが特徴です。

Buon appetito!
```

これらのパラメータを組み合わせることで、AIの応答をより自分の目的に合ったものにすることができます。

## 6. チャットボットの作成

単発の質問だけでなく、会話を続けるチャットボットを作ることもできます。これには「チャットセッション」を使います。

### チャットセッションの作成

```python
from google import genai

client = genai.Client(api_key='あなたのAPIキー')

# チャットセッションを作成
chat = client.chats.create(model='gemini-2.0-flash')

# 最初のメッセージを送信
response = chat.send_message('こんにちは！あなたは誰ですか？')
print(f"AI: {response.text}")

# 会話を続ける
response = chat.send_message('私の趣味について質問してください')
print(f"AI: {response.text}")

# ユーザーの回答
response = chat.send_message('私は読書と料理が好きです')
print(f"AI: {response.text}")
```

**出力例：**
```
AI: こんにちは！私はGeminiという人工知能アシスタントです。Googleによって開発されました。何かお手伝いできることはありますか？

AI: どのような本を読むのが好きですか？また、得意な料理や最近作って美味しかった料理はありますか？

AI: 読書と料理、素晴らしい趣味をお持ちですね！

読書については、どんなジャンルの本を好まれますか？小説、ノンフィクション、自己啓発など、特に好きなジャンルや作家さんはいますか？最近読んだ中で印象に残った本があれば、ぜひ教えてください。

料理に関しては、和食、洋食、中華など、特に得意なジャンルはありますか？自分だけの秘伝のレシピなどもあったら面白いですね。また、新しいレシピに挑戦することは好きですか？

もし良ければ、あなたのお気に入りの本と料理のレシピを教えていただけると嬉しいです。それに基づいて、あなたが興味を持ちそうな本や試してみたいレシピをご提案することもできますよ。
```

このように、チャットセッションを作ることで、AIとの会話の文脈（前後関係）を保持しながら対話を続けることができます。例えば、「それはいいですね」と言った場合、AIは前の会話を覚えているので、何が「いい」のかを理解できます。

## 7. ストリーミング応答

長い回答をAIから受け取る場合、完全な回答が返ってくるまで待つのではなく、文章が生成されるたびに少しずつ表示する「ストリーミング」という方法があります。これを使うと、ユーザーの待ち時間の体感が短くなります。

### テキストのストリーミング

```python
from google import genai

client = genai.Client(api_key='あなたのAPIキー')

# ストリーミングを使用
for chunk in client.models.generate_content_stream(
    model='gemini-2.0-flash',
    contents='日本の四季について100字程度で説明してください'
):
    print(chunk.text, end='')  # 生成されたテキストを即時表示
```

**出力例（徐々に表示されます）:**
```
日本の四季は、それぞれ特徴的な美しさを持っています。

春は桜が咲き誇り、国中がピンク色に彩られます。
夏は蒸し暑いながらも、蝉の声や花火大会が夏の風物詩となります。
秋は紅葉が山々を赤や黄色に染め、収穫の季節を迎えます。
冬は北部では雪景色が広がり、温泉や雪祭りが人々を楽しませます。

この四季の変化は、日本の文化や芸術にも大きな影響を与えてきました。
```

実行すると、AIが考えた回答が、少しずつ画面に表示されていきます。まるで、誰かがリアルタイムでタイピングしているように見えますね！

### チャットでのストリーミング

チャットでもストリーミングを使うことができます。

```python
from google import genai

client = genai.Client(api_key='あなたのAPIキー')

# チャットセッションを作成
chat = client.chats.create(model='gemini-2.0-flash')

# ストリーミングを使った会話
for chunk in chat.send_message_stream('宇宙について教えてください'):
    print(chunk.text, end='')
```

**出力例（徐々に表示されます）:**
```
宇宙は、私たちが知る限り最大の空間であり、すべての物質、エネルギー、時間、そして空間を含む広大な領域です。現在の科学的理解によれば、宇宙は約138億年前のビッグバンから始まったとされています。

宇宙は絶えず膨張しており、その大きさは想像を超えています。観測可能な宇宙の直径は約930億光年と推定されていますが、実際の宇宙はそれよりもはるかに大きいかもしれません。

宇宙には数千億の銀河があり、それぞれの銀河には数千億の星が存在します。私たちの太陽系は、天の川銀河という渦巻銀河の一部です。

宇宙の大部分はダークエネルギー（約68%）とダークマター（約27%）で構成されており、私たちが通常目にする物質は宇宙全体のわずか5%程度にすぎません。

宇宙は常に変化しており、星の誕生と死、銀河の衝突、ブラックホールの形成など、壮大なスケールのイベントが絶えず起こっています。

宇宙についてさらに詳しく知りたい特定のトピックはありますか？例えば、太陽系、ブラックホール、宇宙の起源などについてお話しすることができます。
```

ストリーミングは、特に長い説明や物語を生成する場合に便利です。ユーザーはAIが考えている途中経過を見ることができるので、より自然な対話感が生まれます。

## 8. 次のステップ

この記事では、Google Gen AI SDKの基本的な使い方を学びました。次回の記事では、以下のような発展的なトピックについて詳しく解説する予定です：

- **画像の説明** - AIに画像を見せて内容を説明してもらう方法
- **構造化出力** - AIの回答をJSON形式などで取得する方法
- **ツールの使用** - AIに特定の関数を呼び出してもらう方法（Function Calling）

これらの機能を使うことで、AIの可能性がさらに広がります。ぜひ次回の記事もお楽しみに！

## 9. まとめ

この記事では、Google Gen AI SDKの基本的な使い方を学びました。

- インストール方法とAPIキーの設定
- シンプルなテキスト生成
- 従来のrequestsライブラリとの比較
- 設定パラメータでAIの応答をカスタマイズする方法
- チャットボットの作成
- ストリーミング応答で即時表示する方法

AIは日々進化しており、できることも増えています。ぜひこの基本をマスターして、自分だけのAIアプリケーションを作ってみてください！

何か質問があれば、ぜひコメントしてくださいね。楽しいAIの旅をお祈りします！

## 参考リンク

- [Google Gen AI SDK 公式ドキュメント](https://googleapis.github.io/python-genai/)
- [Gemini Developer API ドキュメント](https://ai.google.dev/gemini-api/docs)
- [Google AI Studio](https://aistudio.google.com/)