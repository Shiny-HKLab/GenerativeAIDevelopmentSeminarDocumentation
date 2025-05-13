import requests
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


# TODO: 投稿（Post）のPydanticモデルを定義する
# 必要なフィールド: id, title, body, userId
# 追加で「created_at」というフィールドを追加し、現在の日時を自動的に設定するようにする
class Post(BaseModel):
    id: int
    title: str
    body: str
    userId: int
    created_at: datetime = Field(default_factory=datetime.now)


# TODO: ユーザー（User）のPydanticモデルを定義する
# 必要なフィールド: id, name, username, email
# email フィールドに対して単純な検証（@が含まれているか）を追加する
class User(BaseModel):
    id: int
    name: str
    username: str
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("メールアドレスには@が含まれている必要があります")
        return v


# JSONPlaceholderからデータを取得して、Pydanticモデルに変換する関数
def get_user_with_posts(user_id: int):
    # ユーザー情報の取得
    # TODO: Pydanticモデルを使ってユーザー情報を取得・変換する処理を実装する
    user_response = requests.get(
        f"https://jsonplaceholder.typicode.com/users/{user_id}"
    )

    if user_response.status_code != 200:
        print(
            f"ユーザー情報の取得に失敗しました。ステータスコード: {user_response.status_code}"
        )
        return

    user_data = user_response.json()

    try:
        user = User.model_validate(user_data)
        print(f"===== ユーザー情報 =====")
        print(f"ID: {user.id}")
        print(f"名前: {user.name}")
        print(f"ユーザー名: {user.username}")
        print(f"メール: {user.email}")
    except Exception as e:
        print(f"ユーザーモデルの変換に失敗しました: {e}")
        return

    # ユーザーの投稿を取得
    # TODO: Pydanticモデルを使ってユーザーの投稿を取得・変換する処理を実装する
    posts_response = requests.get(
        f"https://jsonplaceholder.typicode.com/posts?userId={user_id}"
    )

    if posts_response.status_code != 200:
        print(
            f"投稿データの取得に失敗しました。ステータスコード: {posts_response.status_code}"
        )
        return

    posts_data = posts_response.json()

    try:
        posts = [Post.model_validate(post) for post in posts_data]
    except Exception as e:
        print(f"投稿モデルの変換に失敗しました: {e}")
        return

    # 投稿を表示
    # TODO: Pydanticモデルの属性を使って結果を表示する処理を実装する
    # ヒント: 短縮本文はモデルの外で処理する（ユーティリティ関数を作成）
    def get_short_body(text: str, length: int = 50) -> str:
        """本文の短縮版を返す"""
        if len(text) <= length:
            return text
        return text[:length] + "..."

    print(f"\n===== {user.name}の投稿 ({len(posts)}件) =====")

    for i, post in enumerate(posts, 1):
        print(f"\n投稿 {i}:")
        print(f"ID: {post.id}")
        print(f"タイトル: {post.title}")
        print(f"本文（短縮）: {get_short_body(post.body)}")
        print(f"作成日時: {post.created_at}")
        print("-" * 50)


# メイン処理
if __name__ == "__main__":
    # ユーザーID 2の情報と投稿を表示
    get_user_with_posts(2)
