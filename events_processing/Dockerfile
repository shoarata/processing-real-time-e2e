FROM flink:1.20.1-java11
COPY ./requirements.txt .
RUN apt-get update && apt-get upgrade
RUN apt-get install -y maven
RUN apt-get install -y python3.10 python3-pip python3.10-venv python3.10-distutils openjdk-11-jdk-headless
RUN rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
RUN pip install -r requirements.txt
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN mvn clean package dependency:copy-dependencies -DoutputDirectory=jars/
RUN rm -r target/
