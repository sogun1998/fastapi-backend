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

| エンドポイント   | メソッド | 説明           |
| :--------------- | :------: | :------------- |
| /authors         |   POST   | 著者の作成     |
| /books           |   POST   | 書籍の作成     |
| /books           |   GET    | 書籍一覧の取得 |
| /books/{book_id} |   GET    | 書籍詳細の取得 |
| /books/{book_id} |  DELETE  | 書籍の削除     |

### curl 実行例

#### 著者の作成

```bash
curl -X POST http://localhost:8000/authors \
  -H "Content-Type: application/json" \
  -d '{"name": "夏目漱石"}'
```

#### 書籍の作成

```bash
curl -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "吾輩は猫である", "author_id": "<著者ID>"}'
```

#### 書籍一覧の取得

```bash
curl http://localhost:8000/books
```

#### 書籍詳細の取得

```bash
curl http://localhost:8000/books/<book_id>
```

#### 書籍の削除

```bash
curl -X DELETE http://localhost:8000/books/<book_id>
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

## アーキテクチャ等で意識した点

- **レイヤードアーキテクチャ**
  - コントローラー層（app/controllers）：API エンドポイントの定義とリクエスト/レスポンスの管理。
  - サービス層（app/services）：ビジネスロジックの実装。コントローラーから呼び出され、モデル操作やバリデーションを担当。
  - モデル層（app/models）：DB テーブルに対応する ORM モデル。
  - スキーマ層（app/schemas）：リクエスト/レスポンスの型定義（Pydantic）。
- **テスト容易性**
  - DB セッションのオーバーライドやトランザクションロールバックにより、テストごとにデータをクリーンに保つ設計。
  - TestClient と pytest で API の自動テストを実装。
- **バリデーション**
  - Pydantic の型・制約（必須/最大長など）を活用し、入力値の検証を徹底。
- **保守性・拡張性**
  - 各層を分離し、将来的な機能追加や修正が容易な構成。
  - Docker による環境統一で、開発・本番の差異を最小化。
  - **データベース管理**
    - アプリケーションのバージョンアップに伴うデータベースのテーブル構造の変更（スキーママイグレーション）を、Alembic などのツールを用いてコードで管理し、履歴を追跡・再現可能な形で運用しています。
