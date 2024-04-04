FROM python:3.11-slim

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade -r /app/requirements.txt
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "localhost", "--port", "8080"]
  