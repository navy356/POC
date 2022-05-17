FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD bugbase /code/

WORKDIR /code/bugbase
VOLUME /code
EXPOSE 8000

CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]