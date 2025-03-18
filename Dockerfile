# 使用官方 Python 3.9 以上映像
FROM python:3.9

# 設定工作目錄
WORKDIR /app

# 複製需求檔案並安裝相依套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

# 設定環境變數（Cloud Run 需要監聽 0.0.0.0:8080）
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
ENV PYTHONUNBUFFERED=1

# 對外開放 8080 端口
EXPOSE 8080

# 啟動 Flask（使用 Gunicorn 作為 WSGI Server）
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]