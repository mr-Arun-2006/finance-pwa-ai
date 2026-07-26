FROM python:3.9-slim

WORKDIR /app

COPY ml-models/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ml-models .

EXPOSE 5000

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000"]
