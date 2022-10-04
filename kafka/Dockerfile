FROM openjdk:18
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/kafka"
LABEL version="0.2.0"

ARG kafka_version=3.3.1
ARG scala_version=2.13

ENV KAFKA_VERSION=$kafka_version \
    SCALA_VERSION=$scala_version \
    KAFKA_HOME=/opt/kafka

ENV PATH=${PATH}:${KAFKA_HOME}/bin

RUN microdnf install wget; \
    microdnf clean all

RUN wget -O /tmp/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz https://mirrors.bfsu.edu.cn/apache/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz \
 && tar xfz /tmp/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz -C /opt \
 && rm /tmp/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz \
 && ln -s /opt/kafka_${SCALA_VERSION}-${KAFKA_VERSION} ${KAFKA_HOME} \
 && rm -rf /tmp/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz

CMD ["sh", "-c", "kafka-storage.sh format -t $(kafka-storage.sh random-uuid) -c /opt/kafka/config/kraft/server.properties; kafka-server-start.sh /opt/kafka/config/kraft/server.properties"]

