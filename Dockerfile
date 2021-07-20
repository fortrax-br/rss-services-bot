FROM python:3.7.11-alpine3.14
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
CMD python -m bot
