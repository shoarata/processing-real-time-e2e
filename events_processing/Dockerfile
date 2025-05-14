FROM flink:1.20.1-java11
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y maven
COPY pom.xml .
RUN mvn clean package dependency:copy-dependencies -DoutputDirectory=jars/
RUN rm -r target/
RUN apt-get install -y python3 python3-pip python3-dev && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3 /usr/bin/python
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .