FROM python:3.11-slim-bookworm

WORKDIR /app

COPY ./requirements.txt ./README.md ./app.py ./

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl cmake && \
    pip3 install --default-timeout=300 --no-cache-dir -r requirements.txt -i https://pypi.org/simple && \
    apt-get purge -y --auto-remove build-essential cmake && \
    rm -rf /var/lib/apt/lists/* /root/.cache /tmp/*

ENV PYTHONIOENCODING=utf-8
ENV PYTHONUTF8=1
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_PORT=7860

EXPOSE 7860

HEALTHCHECK CMD curl --fail http://localhost:7860/_stcore/health

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]