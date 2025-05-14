FROM flink:1.20.1-java11
COPY . .
RUN apt-get update && apt-get upgrade
RUN apt-get install -y python3 python3-pip python3-dev openjdk-11-jdk-headless && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3 /usr/bin/python
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
RUN pip3 install -r requirements.txt
