FROM python:3.6-alpine

WORKDIR /app

ADD ./ /app

ENTRYPOINT ["sh", "./run_both_tests.sh"]
