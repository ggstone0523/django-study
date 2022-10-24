FROM python:3.10
LABEL maintainer="tanks2438@outlook.kr"

COPY ./mysite /django-study
COPY ./requirements.txt /django-study

WORKDIR /django-study

RUN pip install -r requirements.txt
RUN cd ./mysite

EXPOSE 8000

CMD ["bash", "-c", "celery multi start w1 -A mysite -l INFO && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]