FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "./app.py" ]