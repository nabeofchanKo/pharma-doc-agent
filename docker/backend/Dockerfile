# Base Image: 軽量なSlim版を使用
FROM python:3.10-slim

# 実務Point: バッファリングを無効化し、ログを即時出力させる (デバッグ用)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

WORKDIR /app

# 実務Point: システム依存パッケージのインストール
# (gccなどは一部のPythonライブラリのビルドに必須)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 実務Point: キャッシュ戦略 (Layer Caching)
# ソースコード(COPY . .)よりも先にrequirementsをCOPYしてインストールする。
# これにより、コードを変更しても「ライブラリインストール」の工程はスキップされる。
COPY src/backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 開発時はHost volumeをマウントするので、ここではフォルダ作成のみ
# (本番デプロイ時はここに COPY . . が入る)
RUN mkdir -p /app/src/backend

# ヘルスチェック (コンテナが死んだらECS等が再起動できるようにする)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# 起動コマンド
CMD ["uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]