# Image du site d'études (Streamlit). La progression est stockée dans /data (volume).
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN useradd --create-home app && mkdir -p /data && chown app /data
USER app
ENV PROGRESS_FILE=/data/progress.json
EXPOSE 8501
CMD ["streamlit", "run", "Accueil.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
