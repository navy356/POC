FROM selenium/standalone-chrome as builder
USER root
FROM ubuntu:latest as builder2
RUN apt update
RUN apt-get install -y fonts-liberation
FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt update
RUN apt-get install -y git x11vnc 
RUN apt-get install -y xvfb
COPY --from=builder /usr/bin/chromedriver /usr/bin
COPY --from=builder /usr/bin/google* /usr/bin/
COPY --from=builder /usr/lib/x86_64-linux-gnu/lib* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /opt/* /opt/google/
RUN mkdir -p /usr/share/fonts/truetype/liberation
COPY --from=builder2 /usr/share/fonts/truetype/* /usr/share/fonts/truetype/liberation
WORKDIR /app
COPY requirements.txt /app/
COPY vnc.sh /app/
RUN pip install -r requirements.txt
COPY ./bugbase /app/
WORKDIR /app/bugbase