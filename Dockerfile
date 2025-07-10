FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn pymysql cryptography

COPY app app
COPY migrations migrations
COPY start.py config.py boot.sh switch.json ./
RUN chmod a+x boot.sh

ENV FLASK_APP start.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
