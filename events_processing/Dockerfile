FROM flink:1.20.1-java11
COPY . .
RUN apt-get update && apt-get upgrade
RUN apt-get install -y maven
RUN mvn clean package dependency:copy-dependencies -DoutputDirectory=jars/
RUN rm -r target/
RUN apt-get install -y python3 python3-pip python3-dev && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN pip3 install -r requirements.txt
