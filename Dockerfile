FROM python:3-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x launch.sh
CMD ['./launch.sh']