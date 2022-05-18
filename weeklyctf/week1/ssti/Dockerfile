FROM python:3.8-alpine

RUN mkdir /app
COPY main.py /app/
COPY templates/ /app/templates/
COPY static/ /app/static/
RUN chmod +x /app/*

RUN pip3 install flask requests
WORKDIR /app

CMD ["python3","/app/main.py"]
