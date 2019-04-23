FROM python:2.1.16-stretch

RUN pip install slackclient
COPY ddb-slack-bot.py /ddb

CMD ["python",'ddb-slack-bot.py']
