ARG ELASTICSEARCH_VERSION=8.15.2
FROM elasticsearch:${ELASTICSEARCH_VERSION}
LABEL version="0.1.0"

ARG ELASTICSEARCH_VERSION
ENV ELASTICSEARCH_VERSION=${ELASTICSEARCH_VERSION}

RUN elasticsearch-plugin install --batch https://get.infini.cloud/elasticsearch/analysis-ik/${ELASTICSEARCH_VERSION}
RUN elasticsearch-plugin install --batch https://get.infini.cloud/elasticsearch/analysis-pinyin/${ELASTICSEARCH_VERSION}
