
FROM python:3.12-alpine


WORKDIR /app


RUN apk add --no-cache curl libffi-dev openssl-dev build-base

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8005

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8005"]
