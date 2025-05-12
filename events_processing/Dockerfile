FROM flink:1.20.1-java11
COPY ./requirements.txt .
RUN apt-get update && apt-get upgrade
RUN apt-get install -y maven
RUN apt-get install -y python3 python3-pip python3-dev openjdk-11-jdk-headless && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
RUN pip install -r requirements.txt
COPY . .
RUN mvn clean package dependency:copy-dependencies -DoutputDirectory=jars/
RUN cp -r jars/ /opt/flink/usrlib/
RUN rm -r target/
RUN ln -s /usr/bin/python3 /usr/bin/python
