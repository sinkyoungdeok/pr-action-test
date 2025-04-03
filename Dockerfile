FROM python:3.9-slim

WORKDIR /app

COPY main.py .

RUN chmod +x main.py
RUN pip install requests

ENTRYPOINT ["python", "main.py"]