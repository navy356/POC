FROM python:3.8-alpine

RUN mkdir /app 
COPY app.py /app/
COPY test.db /app/
COPY static/ /app/static/
COPY templates/ /app/templates/
RUN chmod +x /app/*

RUN pip install requests flask waitress
WORKDIR /app

CMD ["python3","/app/app.py"]
