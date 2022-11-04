FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD sohom /code/

WORKDIR /code/sohom
VOLUME /code
EXPOSE 8000
CMD ["python","app.py"]