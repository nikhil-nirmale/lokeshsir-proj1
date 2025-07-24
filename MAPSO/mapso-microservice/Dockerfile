FROM python:3.9-slim

WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/temp_files

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]