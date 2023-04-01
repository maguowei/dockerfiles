ARG ELASTICSEARCH_VERSION=8.6.2
FROM elasticsearch:${ELASTICSEARCH_VERSION}
LABEL version="0.1.0"

ARG ELASTICSEARCH_VERSION
ENV ELASTICSEARCH_VERSION=${ELASTICSEARCH_VERSION}

RUN elasticsearch-plugin install --batch https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v${ELASTICSEARCH_VERSION}/elasticsearch-analysis-ik-${ELASTICSEARCH_VERSION}.zip
RUN elasticsearch-plugin install --batch https://github.com/medcl/elasticsearch-analysis-pinyin/releases/download/v${ELASTICSEARCH_VERSION}/elasticsearch-analysis-pinyin-${ELASTICSEARCH_VERSION}.zip
