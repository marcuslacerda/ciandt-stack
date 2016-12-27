FROM python:2.7
MAINTAINER Marcus Lacerda "marcus.lacerda@gmail.com"

RUN mkdir /app

ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt

ADD app /app

WORKDIR /app

ENTRYPOINT ["python"]
CMD ["run.py"]
