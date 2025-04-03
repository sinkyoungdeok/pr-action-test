FROM python:3.9-slim

WORKDIR /app

COPY main.py .

RUN chmod +x main.py

ENTRYPOINT ["python", "main.py"]