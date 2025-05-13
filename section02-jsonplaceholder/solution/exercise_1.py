import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] %(message)s')

def get_user(user_id) -> dict | None:
    """指定されたIDのユーザー情報を取得する"""
    # TODO: user_idを使って、JSONPlaceholderからユーザー情報を取得するGETリクエストを実装する
    # ヒント: エンドポイントは 'https://jsonplaceholder.typicode.com/users/{user_id}' 形式
    response = requests.get(f'https://jsonplaceholder.typicode.com/users/{user_id}')
    # TODO: ステータスコードが200の場合、JSONレスポンスを返す。それ以外はNoneを返す
    if response.status_code != 200:
        return None

    user_data = response.json()
    return user_data


def get_posts_by_user(user_id) -> list | None:
    """指定されたユーザーIDの投稿を取得する"""
    # TODO: クエリパラメータを使って、特定ユーザーの投稿を取得する
    # ヒント: paramsに適切なキーと値のペアを設定する

    # TODO: GETリクエストを送信し、ステータスコードが200の場合はJSONレスポンスを返す
    # それ以外の場合は空のリストを返す


def display_user_with_posts(user_id) -> None:
    """ユーザー情報とその投稿を表示する"""
    # ユーザー情報の取得
    # TODO: get_user関数を呼び出してユーザー情報を取得する
    user = get_user(user_id)

    # TODO: ユーザーが見つからない場合のエラーメッセージを表示して関数を終了する
    if user is None:
        error_msg = f"User with ID {user_id} not found."
        logging.error(error_msg)
        return

    # ユーザー情報の表示
    logging.info(f"User ID: {user_id}")

    # ユーザーの投稿を取得して表示
    # TODO: get_posts_by_user関数を呼び出してユーザーの投稿を取得する

    # for文を使って、投稿を表示する

if __name__ == "__main__":
    # ユーザーID 3の情報と投稿を表示
    display_user_with_posts(3)