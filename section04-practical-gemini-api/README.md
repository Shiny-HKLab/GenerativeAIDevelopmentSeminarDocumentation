# Google Gen AI SDK発展編：画像処理・構造化出力・ツール連携をマスター 🚀
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shiny-HKLab/GenerativeAIDevelopmentSeminarDocumentation/blob/main/section04-practical-gemini-api/notebook.ipynb)

前回の記事では、Google Gen AI SDKの基本的な使い方を学びました。今回は、AIの可能性をさらに広げる発展的な機能について詳しく解説します！

**今回学ぶこと：**
• 画像を使ったAI対話の実現
• 構造化されたデータ出力の取得
• AIに外部ツールを使わせる方法
• 実践的なアプリケーションの構築例

技術的な複雑さを軽減しながら、より高度なAIアプリケーションを作る方法を身につけていきましょう。

## 1. 前回の振り返り

前回の記事では、以下の基本機能を学びました：

- **テキスト生成** - シンプルなAIとの対話
- **パラメータ調整** - 温度やトークン数での出力制御
- **チャット機能** - 会話の文脈を保持した対話
- **ストリーミング** - リアルタイムな応答表示

これらの基礎知識があることで、今回学ぶ発展的な機能もスムーズに理解できるはずです。

## 2. 画像の説明機能 📸

AIに画像を見せて、その内容を説明してもらう機能は非常に強力です。写真の解析、図表の理解、視覚的なコンテンツの自動説明など、様々な用途に活用できます。

### ローカル画像ファイルの処理

まずは、パソコンに保存されている画像ファイルをAIに見せる方法から始めましょう。

```python
from google import genai
from google.genai import types
import os

# クライアントを作成
client = genai.Client(api_key='あなたのAPIキー')

# 画像ファイルのパスを指定
image_path = 'sample_image.jpg'

# ファイルが存在するかチェック
if not os.path.exists(image_path):
    print(f"エラー: ファイル '{image_path}' が見つかりません")
else:
    # 画像ファイルを読み込む（バイナリモードで開く）
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    # AIに画像について質問
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=[
            'この画像に写っているものを詳しく説明してください',
            types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
        ],
    )
    
    print(response.text)
```

**重要なポイント：**
- ファイルを `'rb'` (read binary) モードで開く必要があります
- `image_path` はファイルパス（文字列）、`image_bytes` は実際のバイナリデータです
- ファイルの存在チェックでエラーを回避できます

### Google Colabでの画像アップロード

Google Colabを使用している場合は、以下の方法で画像をアップロードできます：

```python
from google.colab import files
from google import genai
from google.genai import types

# Google ColabのAPIキー設定
from google.colab import userdata
api_key = userdata.get("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# ファイルをアップロード
uploaded = files.upload()

# アップロードされたファイルを処理
for filename in uploaded.keys():
    print(f'アップロードされたファイル: {filename}')
    
    # ファイルの内容を読み込み
    image_bytes = uploaded[filename]
    
    # 拡張子から MIME タイプを判定
    mime_type = 'image/jpeg'
    if filename.lower().endswith('.png'):
        mime_type = 'image/png'
    elif filename.lower().endswith('.gif'):
        mime_type = 'image/gif'
    
    # AIに画像について質問
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=[
            'この画像に写っているものを詳しく説明してください',
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
        ],
    )
    
    print(f"\n{filename} の分析結果:")
    print(response.text)
```

**出力例（猫の写真の場合）:**
```
この画像には、美しい茶トラ猫が写っています。猫は日当たりの良い窓辺に座っており、
ふわふわした毛並みが印象的です。

詳細な特徴：
• 毛色：茶色とクリーム色の縞模様（タビー）
• 目：大きくて丸い緑色の瞳
• 表情：リラックスした穏やかな表情
• 姿勢：前足を揃えて上品に座っている
• 背景：窓から差し込む自然光が美しく、観葉植物も見える

猫は健康的で幸せそうに見え、とても愛らしい写真です。室内飼いの家猫で、
よく手入れされていることが毛艶の良さからも伺えます。
```

### URL画像の処理

インターネット上の画像も簡単に処理できます。

```python
from google import genai
from google.genai import types

client = genai.Client(api_key='あなたのAPIキー')

# インターネット上の画像のURLを指定
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=[
        'この画像の料理について、作り方を推測して教えてください',
        types.Part.from_uri(
            file_uri='gs://generativeai-downloads/images/scones.jpg',
            mime_type='image/jpeg',
        ),
    ],
)

print(response.text)
```

**出力例:**
```
この画像には美味しそうなスコーンが写っています。以下のような作り方で作られたと推測されます：

## 材料（8個分）
• 薄力粉：200g
• ベーキングパウダー：小さじ2
• 砂糖：大さじ2
• 塩：小さじ1/4
• 無塩バター：50g（冷やしておく）
• 牛乳：100ml
• 卵：1個

## 作り方
1. オーブンを200℃に予熱
2. 粉類をボウルで混ぜ、冷たいバターを小さく切って加える
3. バターを粉になじませるようにすり混ぜる
4. 牛乳と卵を加えて軽く混ぜ、生地をまとめる
5. 厚さ2cm程度に伸ばし、丸型で抜く
6. 15-20分焼いて完成

画像を見ると、表面が美しいきつね色に焼けており、ふっくらと膨らんでいます。
ジャムやクロテッドクリームと一緒にいただくと最高ですね！
```

### 画像に関する具体的な質問

特定の情報を知りたい場合は、より具体的な質問をすることもできます。

```python
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=[
        'この画像の中に人は何人写っていますか？それぞれの服装の色も教えてください',
        types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
    ],
)

print(response.text)
```

## 3. 構造化出力（JSON形式） 📊

AIからの回答をプログラムで処理しやすい形式（JSON）で取得する方法を学びましょう。これにより、AIの出力をデータベースに保存したり、他のシステムと連携したりすることが簡単になります。

### Pydanticモデルを使った構造化出力

Pydanticを使って、期待するデータ構造を定義できます。`Field`を使って各項目に説明を追加すると、AIがより適切なデータを生成してくれます。

```python
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List

# データ構造を定義（Fieldで詳細な説明を追加）
class BookInfo(BaseModel):
    title: str = Field(description="本のタイトル")
    author: str = Field(description="著者名")
    genre: str = Field(description="ジャンル（小説、ノンフィクション、ビジネス書など）")
    publication_year: int = Field(description="出版年", ge=1900, le=2025)
    pages: int = Field(description="ページ数", gt=0)
    summary: str = Field(description="本の内容を要約した説明（100文字程度）")

client = genai.Client(api_key='あなたのAPIキー')

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='面白いSF小説を1冊おすすめしてください',
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=BookInfo,
    ),
)

print(response.text)
```

**構造化出力のベストプラクティス：**

1. **明確な説明を追加**: `Field(description=...)`でAIに期待値を伝える
2. **バリデーションを活用**: `ge`, `le`, `gt`, `lt`などで値の範囲を制限
3. **Enumで選択肢を限定**: 不正な値の生成を防ぐ
4. **Optionalで柔軟性を保つ**: 必須でない項目は`Optional`を使用
5. **ネストした構造**: 複雑なデータも階層的に定義可能

**出力例:**
```json
{
  "title": "星の航海者",
  "author": "田中雄一",
  "genre": "SF小説",
  "publication_year": 2023,
  "pages": 324,
  "summary": "2150年、人類は初めて太陽系外への航行に成功する。しかし、目的地で発見されたのは古代文明の謎に満ちた遺跡だった。主人公の宇宙飛行士が異星文明の秘密に迫るスペースオペラ。"
}
```

### より複雑な構造化出力の例

複雑なデータ構造にも対応できます：

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class DifficultyLevel(str, Enum):
    BEGINNER = "初級"
    INTERMEDIATE = "中級" 
    ADVANCED = "上級"

class SkillInfo(BaseModel):
    name: str = Field(description="スキル名")
    level: DifficultyLevel = Field(description="習得難易度")
    description: str = Field(description="スキルの説明")

class PersonInfo(BaseModel):
    name: str = Field(description="人物の名前")
    age: int = Field(description="年齢", ge=0, le=120)
    occupation: str = Field(description="職業")
    hobbies: List[str] = Field(description="趣味のリスト（3-5個程度）", max_items=5)
    skills: List[SkillInfo] = Field(description="持っているスキルのリスト")
    bio: str = Field(description="人物の経歴や特徴（150文字程度）")

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='プログラマーの架空の人物プロフィールを作成してください',
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=PersonInfo,
    ),
)

print(response.text)
```

**出力例:**
```json
{
  "name": "佐藤健太",
  "age": 28,
  "occupation": "ソフトウェアエンジニア",
  "hobbies": ["読書", "ボードゲーム", "カメラ撮影", "料理"],
  "skills": [
    {
      "name": "Python",
      "level": "上級",
      "description": "Webアプリケーション開発とデータ分析"
    },
    {
      "name": "React",
      "level": "中級",
      "description": "フロントエンド開発"
    }
  ],
  "bio": "大学でコンピュータサイエンスを学んだ後、スタートアップ企業でフルスタック開発者として3年間勤務。現在は大手IT企業でAI関連のプロダクト開発に携わっている。"
}
```

### 辞書形式での構造化出力

Pydanticを使わずに、辞書形式でスキーマを定義することも可能です。

```python
from google import genai
from google.genai import types

client = genai.Client(api_key='あなたのAPIキー')

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='今日の東京の天気予報を教えてください',
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema={
            'type': 'OBJECT',
            'required': ['date', 'temperature', 'condition', 'humidity', 'wind'],
            'properties': {
                'date': {'type': 'STRING'},
                'temperature': {
                    'type': 'OBJECT',
                    'properties': {
                        'high': {'type': 'INTEGER'},
                        'low': {'type': 'INTEGER'}
                    }
                },
                'condition': {'type': 'STRING'},
                'humidity': {'type': 'INTEGER'},
                'wind': {'type': 'STRING'}
            }
        },
    ),
)

print(response.text)
```

**出力例:**
```json
{
  "date": "2025-06-23",
  "temperature": {
    "high": 28,
    "low": 22
  },
  "condition": "晴れ時々曇り",
  "humidity": 65,
  "wind": "北東の風2メートル"
}
```

### 列挙型（Enum）での制限された回答

特定の選択肢から回答を選んでもらいたい場合は、列挙型を使用できます。

```python
from enum import Enum
from google import genai
from google.genai import types

class MoodEnum(Enum):
    HAPPY = 'happy'
    SAD = 'sad'
    EXCITED = 'excited'
    CALM = 'calm'
    CONFUSED = 'confused'

client = genai.Client(api_key='あなたのAPIキー')

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='明日が休日だと知った時の気持ちを表現してください',
    config=types.GenerateContentConfig(
        response_mime_type='text/x.enum',
        response_schema=MoodEnum,
    ),
)

print(response.text)
```

**出力例:**
```
excited
```

## 4. ツールの使用（Function Calling） 🔧

AIに外部の関数やツールを呼び出してもらう機能は、非常に強力です。天気情報の取得、データベースの検索、計算処理など、AIが自動的に適切なツールを選んで実行してくれます。

### Function Callingの仕組みを理解しよう

**Function Calling（関数呼び出し）とは何でしょうか？**

想像してみてください。あなたが秘書に「今日の会議室の予約状況を調べて、空いている時間があれば会議を予約してください」とお願いしたとします。優秀な秘書なら以下のように行動するでしょう：

1. 予約システムにアクセスして空き状況を確認
2. 空きがあれば予約システムで実際に予約を取る
3. 結果をあなたに報告

Function Callingは、AIがこの「優秀な秘書」のような役割を果たす仕組みです：

```
あなた → 「東京の天気を調べて、気温も華氏で教えて」
   ↓
 AI → 「天気を調べる関数を呼び出そう」
   ↓
システム → get_weather_info('Tokyo') を実行
   ↓
 AI → 「気温を変換する関数も呼び出そう」
   ↓
システム → convert_temperature(25, 'fahrenheit') を実行
   ↓
 AI → 「東京は晴れで25度です。華氏では77度ですね」
```

**従来の方法との違い**

```python
# ❌ 従来の方法：すべて手動で処理
user_message = "東京の天気と華氏温度を教えて"
weather = get_weather_info('Tokyo')  # 手動で関数を呼び出し
temp_in_f = convert_temperature(25, 'fahrenheit')  # 手動で変換
response = f"東京の天気：{weather}、華氏：{temp_in_f}"

# ✅ Function Calling：AIが自動で判断・実行
response = client.models.generate_content(
    contents="東京の天気を調べて、気温も華氏で教えて",
    config=types.GenerateContentConfig(
        tools=[get_weather_info, convert_temperature],  # 使える道具を渡すだけ
    ),
)
```

**AIはどのように関数を理解するのか？**

AIは関数の「説明書」（docstring）を読んで、その関数が何をするものなのかを理解します：

```python
def calculate_area(length: float, width: float) -> float:
    """長方形の面積を計算します。  ← AIはこの説明を読む
    
    Args:
        length: 長さ（メートル）    ← 引数の意味も理解
        width: 幅（メートル）      ← 引数の意味も理解
    """
    return length * width
```

ユーザーが「6メートル×4メートルの部屋の面積は？」と聞くと、AIは：
- 「面積」「長方形」というキーワードから適切な関数を特定
- 6と4という数値を length と width に割り当て
- 関数を呼び出して結果を取得
- 自然な文章で回答を生成

### 自動関数呼び出し

Pythonの関数をそのまま渡すだけで、AIが自動的に呼び出してくれます。

```python
from google import genai
from google.genai import types
import datetime

def get_current_time() -> str:
    """現在の時刻を取得します。"""
    now = datetime.datetime.now()
    return now.strftime("%Y年%m月%d日 %H時%M分")

def calculate_area(length: float, width: float) -> float:
    """長方形の面積を計算します。
    
    Args:
        length: 長さ（メートル）
        width: 幅（メートル）
    """
    return length * width

client = genai.Client(api_key='あなたのAPIキー')

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='今の時刻を教えてください。それと、長さ5メートル、幅3メートルの部屋の面積も計算してください。',
    config=types.GenerateContentConfig(
        tools=[get_current_time, calculate_area],
    ),
)

print(response.text)
```

**出力例:**
```
現在の時刻は2025年06月23日 14時30分です。

また、長さ5メートル、幅3メートルの部屋の面積は15.0平方メートルです。

このサイズの部屋でしたら、一人暮らしの寝室やワークスペースとして
ちょうど良い広さですね。家具の配置を考える際の参考にしてください。
```

### 自動関数呼び出しが行われないパターン

以下のような場合、自動的に関数が呼び出されないことがあります：

#### 1. AIが関数を呼び出す必要がないと判断した場合

```python
def get_current_time() -> str:
    """現在の時刻を取得します。"""
    return datetime.datetime.now().strftime("%Y年%m月%d日 %H時%M分")

# 時刻に関係ない質問の場合、関数は呼び出されない
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='プログラミングを学ぶメリットを教えてください',
    config=types.GenerateContentConfig(
        tools=[get_current_time],
    ),
)
```

#### 2. 関数の説明が不適切な場合

```python
# ❌ 悪い例：説明が不十分
def bad_function(x, y):
    return x * y

# ✅ 良い例：詳細な説明
def calculate_area(length: float, width: float) -> float:
    """長方形の面積を計算します。
    
    Args:
        length: 長さ（メートル）
        width: 幅（メートル）
    
    Returns:
        面積（平方メートル）
    """
    return length * width
```

#### 3. 自動関数呼び出しを無効にした場合

```python
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='今の時刻を教えてください',
    config=types.GenerateContentConfig(
        tools=[get_current_time],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True  # 自動呼び出しを無効化
        ),
    ),
)

# この場合、function_callsで手動で処理する必要がある
if response.function_calls:
    print("関数呼び出しが提案されました:", response.function_calls[0])
```

#### 4. 複雑すぎる処理や曖昧な要求の場合

```python
# 曖昧な要求では関数が呼び出されない可能性
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='何か計算してください',  # 具体性に欠ける
    config=types.GenerateContentConfig(
        tools=[calculate_area],
    ),
)
```

### 自動関数呼び出しを確実にするコツ

1. **明確で詳細な関数の説明文を書く**
2. **引数の型や説明を詳しく記述する**
3. **具体的で明確な指示を出す**
4. **関数名は目的が分かりやすいものにする**

### 天気情報取得の実用例

実際のAPIを呼び出す関数も使用できます。

```python
import requests
from google import genai
from google.genai import types

def get_weather_info(city: str) -> str:
    """指定された都市の天気情報を取得します。
    
    Args:
        city: 都市名（例：Tokyo, Osaka）
    """
    # 実際にはOpenWeatherMap APIなどを使用
    # ここではサンプルデータを返します
    weather_data = {
        'Tokyo': '晴れ、気温25度、湿度60%',
        'Osaka': '曇り、気温23度、湿度70%',
        'Kyoto': '小雨、気温20度、湿度85%'
    }
    
    return weather_data.get(city, f'{city}の天気情報は現在取得できません')

def convert_temperature(celsius: float, unit: str) -> str:
    """摂氏温度を他の単位に変換します。
    
    Args:
        celsius: 摂氏温度
        unit: 変換先の単位（'fahrenheit' または 'kelvin'）
    """
    if unit.lower() == 'fahrenheit':
        fahrenheit = (celsius * 9/5) + 32
        return f'{celsius}℃ は {fahrenheit:.1f}°F です'
    elif unit.lower() == 'kelvin':
        kelvin = celsius + 273.15
        return f'{celsius}℃ は {kelvin:.1f}K です'
    else:
        return '対応していない単位です'

client = genai.Client(api_key='あなたのAPIキー')

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='東京の天気を調べて、気温を華氏でも教えてください',
    config=types.GenerateContentConfig(
        tools=[get_weather_info, convert_temperature],
    ),
)

print(response.text)
```

**出力例:**
```
東京の現在の天気は晴れで、気温は25度、湿度は60%です。

気温25℃を華氏に変換すると77.0°Fになります。

とても過ごしやすい気候ですね！お出かけには最適な天気です。
湿度も適度で、快適に過ごせそうです。
```

### 複数のツールを組み合わせた複雑な処理

```python
from google import genai
from google.genai import types
import json
import random

def search_books(genre: str) -> str:
    """ジャンル別に本を検索します。
    
    Args:
        genre: 本のジャンル（fiction, mystery, science, business等）
    """
    # サンプルデータ
    books = {
        'fiction': ['吾輩は猫である', '坊っちゃん', 'こころ'],
        'mystery': ['そして誰もいなくなった', 'シャーロック・ホームズ', '容疑者Xの献身'],
        'science': ['コスモス', 'ファインマン物理学', 'ブルーバックス シリーズ'],
        'business': ['7つの習慣', 'FACTFULNESS', 'イノベーションのジレンマ']
    }
    
    result = books.get(genre, ['該当する本が見つかりません'])
    return json.dumps(result, ensure_ascii=False)

def generate_quote() -> str:
    """ランダムに名言を生成します。"""
    quotes = [
        "継続は力なり",
        "読書は心の栄養である", 
        "知識は力なり",
        "学ぶことをやめたら、教えることをやめなければならない"
    ]
    return random.choice(quotes)

def calculate_reading_time(pages: int, speed: int = 1) -> str:
    """読書時間を計算します。
    
    Args:
        pages: ページ数
        speed: 読書速度（1=普通、2=速い、0.5=ゆっくり）
    """
    # 1ページあたり平均2分として計算
    minutes = pages * 2 / speed
    hours = minutes / 60
    
    if hours < 1:
        return f"約{int(minutes)}分で読めます"
    else:
        return f"約{hours:.1f}時間で読めます"

client = genai.Client(api_key='あなたのAPIキー')

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='ミステリー小説を探していて、300ページくらいの本の読書時間も知りたいです。あと、読書のモチベーションになる名言も教えてください。',
    config=types.GenerateContentConfig(
        tools=[search_books, calculate_reading_time, generate_quote],
    ),
)

print(response.text)
```

**出力例:**
```
ミステリー小説をお探しですね！以下のような作品がおすすめです：

• そして誰もいなくなった
• シャーロック・ホームズ
• 容疑者Xの献身

300ページの本でしたら、約10.0時間で読めます。1日1時間読書すれば、約10日で完読できる計算ですね。

読書のモチベーションとなる名言をお送りします：
「読書は心の栄養である」

ミステリー小説は一度読み始めると止まらなくなるジャンルです。
特に「そして誰もいなくなった」は、ミステリーの古典的名作として
多くの読者に愛され続けています。楽しい読書時間をお過ごしください！
```

## 5. 実践的なアプリケーション例 💡

これまで学んだ機能を組み合わせて、実用的なアプリケーションを作ってみましょう。

### 画像解析レポート生成システム

```python
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List

class ImageAnalysisReport(BaseModel):
    main_subjects: List[str]
    colors: List[str]
    mood: str
    suggested_tags: List[str]
    description: str
    potential_uses: List[str]

def analyze_image_comprehensively(image_path: str) -> dict:
    """画像を総合的に分析してレポートを生成します。"""
    
    client = genai.Client(api_key='あなたのAPIキー')
    
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=[
            '''この画像を総合的に分析してください。
            - 主要な被写体
            - 使用されている色調
            - 画像の雰囲気・ムード
            - SEOに適したタグ候補
            - 詳細な説明
            - この画像の潜在的な用途''',
            types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
        ],
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=ImageAnalysisReport,
        ),
    )
    
    return response.text

# 使用例
# report = analyze_image_comprehensively('sample_photo.jpg')
# print(report)
```

### AIパーソナルアシスタント

```python
from google import genai
from google.genai import types
import datetime
import json

class PersonalAssistant:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.tools = [
            self.get_current_time,
            self.calculate_days_until,
            self.convert_currency,
            self.get_weather_advice
        ]
    
    def get_current_time(self) -> str:
        """現在の日時を取得します。"""
        return datetime.datetime.now().strftime("%Y年%m月%d日 %H時%M分")
    
    def calculate_days_until(self, target_date: str) -> str:
        """指定された日付までの日数を計算します。
        
        Args:
            target_date: 目標日（YYYY-MM-DD形式）
        """
        try:
            target = datetime.datetime.strptime(target_date, "%Y-%m-%d")
            today = datetime.datetime.now()
            days = (target - today).days
            return f"{target_date}まであと{days}日です"
        except:
            return "日付の形式が正しくありません"
    
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> str:
        """通貨を変換します（簡易版）。
        
        Args:
            amount: 金額
            from_currency: 変換元通貨（USD, JPY, EUR等）
            to_currency: 変換先通貨
        """
        # 実際にはリアルタイム為替レートAPIを使用
        rates = {'USD': 150, 'EUR': 160, 'JPY': 1}  # 対JPYレート
        
        jpy_amount = amount * rates.get(from_currency, 1)
        result = jpy_amount / rates.get(to_currency, 1)
        
        return f"{amount} {from_currency} = {result:.2f} {to_currency}"
    
    def get_weather_advice(self, condition: str) -> str:
        """天気に応じたアドバイスを提供します。
        
        Args:
            condition: 天気の状況（sunny, rainy, cloudy等）
        """
        advice = {
            'sunny': '日焼け止めを忘れずに！水分補給もこまめに。',
            'rainy': '傘を持参してください。足元にご注意を。',
            'cloudy': '上着を一枚持っていくと安心です。',
            'snowy': '防寒対策をしっかりと。滑りにくい靴がおすすめ。'
        }
        return advice.get(condition, '天気情報をご確認ください。')
    
    def chat(self, message: str) -> str:
        """ユーザーのメッセージに応答します。"""
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=message,
            config=types.GenerateContentConfig(
                tools=self.tools,
                system_instruction='''あなたは親切なパーソナルアシスタントです。
                ユーザーの質問に対して、適切なツールを使って正確で役立つ情報を提供してください。
                回答は丁寧で分かりやすくしてください。'''
            ),
        )
        return response.text

# 使用例
# assistant = PersonalAssistant('あなたのAPIキー')
# print(assistant.chat('クリスマスまであと何日か教えて'))
# print(assistant.chat('100ドルは日本円でいくら？'))
```

## 6. エラーハンドリングとベストプラクティス ⚠️

実際のアプリケーション開発では、エラーハンドリングが重要です。

### よくあるエラーと対処法

#### 1. 画像関連のエラー

**ValidationError: Data should be valid base64**
```python
# ❌ 間違った例：ファイルパスをそのまま渡している
image_path = 'sample.jpg'
types.Part.from_bytes(data=image_path, mime_type='image/jpeg')  # エラー！

# ✅ 正しい例：ファイルを読み込んでバイナリデータを渡す
with open(image_path, 'rb') as f:
    image_bytes = f.read()
types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg')
```

**ファイルが見つからないエラー**
```python
import os
from google import genai
from google.genai import types

def safe_image_analysis(image_path: str, prompt: str):
    """安全な画像分析関数"""
    client = genai.Client(api_key='あなたのAPIキー')
    
    # ファイル存在チェック
    if not os.path.exists(image_path):
        return f"エラー: ファイル '{image_path}' が見つかりません"
    
    # ファイルサイズチェック（20MB制限）
    file_size = os.path.getsize(image_path)
    if file_size > 20 * 1024 * 1024:
        return "エラー: ファイルサイズが20MBを超えています"
    
    try:
        # 拡張子からMIMEタイプを判定
        mime_type = 'image/jpeg'
        if image_path.lower().endswith('.png'):
            mime_type = 'image/png'
        elif image_path.lower().endswith('.gif'):
            mime_type = 'image/gif'
        elif image_path.lower().endswith('.webp'):
            mime_type = 'image/webp'
        
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=[
                prompt,
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            ],
        )
        
        return response.text
        
    except Exception as e:
        return f"分析中にエラーが発生しました: {e}"

# 使用例
result = safe_image_analysis('sample.jpg', 'この画像を説明してください')
print(result)
```

#### 2. 構造化出力のエラー

**スキーマ定義の不備**
```python
from pydantic import BaseModel, Field
from typing import List, Optional

# ❌ 悪い例：説明やバリデーションがない
class BadBookInfo(BaseModel):
    title: str
    author: str
    pages: int

# ✅ 良い例：詳細な説明とバリデーション
class GoodBookInfo(BaseModel):
    title: str = Field(description="本のタイトル")
    author: str = Field(description="著者名")
    pages: int = Field(description="ページ数", gt=0, le=2000)
    genre: str = Field(description="ジャンル（小説、ビジネス書など）")
    
# より柔軟なスキーマ定義の例
try:
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents='おすすめの自己啓発本を1冊教えてください',
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=GoodBookInfo,
        ),
    )
    print(response.text)
except Exception as e:
    print(f"構造化出力エラー: {e}")
```

**重要：Fieldの説明が不十分だと、AIが期待と異なるデータを生成する可能性があります。**

### 基本的なエラーハンドリング

```python
from google import genai
from google.genai import errors

client = genai.Client(api_key='あなたのAPIキー')

try:
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents='こんにちは'
    )
    print(response.text)
    
except errors.APIError as e:
    print(f"APIエラーが発生しました: {e.code} - {e.message}")
    
except Exception as e:
    print(f"予期しないエラーが発生しました: {e}")
```

### 開発時のベストプラクティス

**パフォーマンス最適化：**
• レスポンス時間を短縮するため、不要に長いプロンプトは避ける
• ストリーミングを活用してユーザー体験を向上させる
• 適切なモデルを選択（速度重視なら flash、品質重視なら pro）

**セキュリティ対策：**
• APIキーは環境変数で管理し、コードに直接書かない
• ユーザー入力のサニタイゼーションを実装
• レート制限に注意して適切な間隔でAPIを呼び出す

**コスト管理：**
• 不要なAPI呼び出しを避ける
• トークン数を適切に制限する
• 開発環境と本番環境でAPIキーを分ける

**デバッグのコツ：**
```python
# ログ出力で問題を特定
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_api_call(prompt: str):
    logger.info(f"API呼び出し開始: {prompt[:50]}...")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt
        )
        logger.info(f"API呼び出し成功: {len(response.text)} 文字の応答")
        return response.text
        
    except Exception as e:
        logger.error(f"API呼び出し失敗: {e}")
        return None
```

## 7. まとめと次なる挑戦 🎯

この記事では、Google Gen AI SDKの発展的な機能を学びました：

**習得した技術：**
• 画像処理による視覚的AI対話
• 構造化出力でのプログラマブルなデータ取得
• Function Callingによる外部ツール連携
• 実践的なアプリケーション構築方法

### 継続的な学習のストラテジー

**次のステップとして挑戦してみてください：**
• 複数の画像を同時に処理する機能
• 音声認識・音声合成との連携
• データベースとの統合システム
• Webアプリケーションへの組み込み
• リアルタイム処理システムの構築

技術的な複雑さに負けず、小さなプロジェクトから始めて徐々にスケールアップしていくことが、優れたAI開発者への道です。

**コミュニティとの交流を活用：**
• GitHub上でのオープンソースプロジェクトへの参加
• 技術ブログでの知識共有
• カンファレンスやハッカソンへの参加
• 新しいAI技術トレンドへの継続的な学習

AIテクノロジーは日々進化しています。今回学んだ基礎をしっかりと身につけて、次世代のAIアプリケーション開発にチャレンジしてみてください！

## 参考リンク

- [Google Gen AI SDK 公式ドキュメント](https://googleapis.github.io/python-genai/)
- [Gemini API リファレンス](https://ai.google.dev/gemini-api/docs)
- [Pydantic公式ドキュメント](https://pydantic.readthedocs.io/)
- [Google AI Studio](https://aistudio.google.com/)

継続的な成長が、優れたAI開発者への道です。頑張ってください！ 🚀