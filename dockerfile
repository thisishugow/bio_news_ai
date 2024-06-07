FROM debian 

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN TZ=Asia/Taipei \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata 

# Install Python 3.11 and PIP
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y wget procps chromium chromium-driver
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3.11 python3.11-distutils

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.bk
RUN python3.11 get-pip.py
RUN pip3 install --upgrade setuptools

RUN mkdir /app
RUN chmod -R 777 /app 

COPY .env /app
WORKDIR /app
COPY ./dist/web_condenser_ai*.whl /app
RUN pip3 install /app/web_condenser_ai*.whl
RUN rm /app/web_condenser_ai*.whl

ENV USE_CHROMIUM yes

ENTRYPOINT [ "python3.11", "-m", "web_condenser_ai" ]

EXPOSE 8501