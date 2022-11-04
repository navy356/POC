FROM selenium/standalone-chrome-debug
USER root
RUN apt update
RUN wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_99.0.4844.51-1_amd64.deb
RUN dpkg -i google-chrome-stable_99.0.4844.51-1_amd64.deb
RUN wget -qP /tmp/ "https://chromedriver.storage.googleapis.com/99.0.4844.51/chromedriver_linux64.zip"
RUN unzip -o /tmp/chromedriver_linux64.zip -d /usr/bin