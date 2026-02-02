FROM python:3.11-slim
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip install --no-cache-dir flask requests
RUN mkdir -p /app/www

COPY app/main.py /app/main.py
COPY www/ /app/www/

CMD ["python", "main.py"]
