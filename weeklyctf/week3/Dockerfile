FROM python:3
RUN apt-get -y update && apt-get install -y build-essential
RUN useradd -m achaar
USER achaar
WORKDIR /home/achaar/app
RUN python3 -m pip install --upgrade pip
COPY app/ ./
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]