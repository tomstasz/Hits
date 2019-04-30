FROM python:3.7-alpine
MAINTAINER tomstasz

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /api
WORKDIR /api
COPY ./api /api

ENV FLASK_APP eska.py

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["eska.py"]