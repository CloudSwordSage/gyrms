FROM python:3.12-slim

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

COPY start.sh /app/start.sh
RUN chmod +777 /app/start.sh

CMD ["/app/start.sh"]

