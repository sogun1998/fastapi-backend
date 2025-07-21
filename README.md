# 書籍管理 API

## 概要

このプロジェクトは、FastAPI を使用した書籍と著者の管理システムです。MySQL データベースを使用し、RESTful API を提供します。

## 機能

### 著者管理

- 著者の作成
- 著者情報の取得

### 書籍管理

- 書籍の作成
- 書籍一覧の取得
- 書籍詳細の取得
- 書籍の削除

## 技術スタック

- **Backend**: FastAPI (Python)
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy
- **Migration**: Alembic
- **Container**: Docker & Docker Compose

## プロジェクト構造

```
fastapi-backend/
├── app/
│   ├── controllers/          # API エンドポイントコントローラー
│   │   ├── authors.py
│   │   └── books.py
│   │   └── test_controller.py
│   ├── models/              # データベースモデル
│   │   ├── authors.py
│   │   └── books.py
│   ├── services/            # ビジネスロジック
│   │   ├── authors.py
│   │   └── books.py
│   ├── database.py          # データベース設定
│   ├── main.py             # FastAPI アプリケーション
│   └── schemas.py          # Pydantic スキーマ
├── alembic/                # データベースマイグレーション
├── docker-compose.yml      # Docker 設定
├── Dockerfile             # Docker イメージ
├── requirements.txt       # Python 依存関係
```

## セットアップ

### 前提条件

- Docker
- Docker Compose

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd fastapi-backend
```

### 2. Docker コンテナの起動

```bash
docker-compose up --build
```

### 3. データベースマイグレーションの実行

```bash
docker-compose exec web bash -c "alembic upgrade head"
```

### 4. ユニットテスト実行

```bash
# コンテナ内でスクリプトを実行
docker-compose exec web bash -c "PYTHONPATH=. pytest app/controllers/test_controller.py"
```

## API エンドポイント

### 著者関連

#### 著者の作成

```http
POST /authors
Content-Type: application/json

{
  "name": "著者名"
}
```

### 書籍関連

#### 書籍の作成

```http
POST /books
Content-Type: application/json

{
  "title": "書籍タイトル",
  "author_id": "著者ID"
}
```

#### 書籍一覧の取得

```http
GET /books
```

#### 書籍詳細の取得

```http
GET /books/{book_id}
```

#### 書籍の削除

```http
DELETE /books/{book_id}
```

## データベーススキーマ

### authors テーブル

| カラム | 型          | 説明           |
| ------ | ----------- | -------------- |
| id     | VARCHAR(36) | 主キー（UUID） |
| name   | VARCHAR(50) | 著者名         |

### books テーブル

| カラム    | 型           | 説明                   |
| --------- | ------------ | ---------------------- |
| id        | VARCHAR(36)  | 主キー（UUID）         |
| title     | VARCHAR(100) | 書籍タイトル           |
| author_id | VARCHAR(36)  | 外部キー（authors.id） |


