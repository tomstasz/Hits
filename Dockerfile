FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /api
WORKDIR /.
COPY . .

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["main.py"]