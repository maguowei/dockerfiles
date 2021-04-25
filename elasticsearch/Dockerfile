FROM docker.elastic.co/elasticsearch/elasticsearch:7.11.2
LABEL version="0.1.0"


RUN elasticsearch-plugin install --batch https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.11.2/elasticsearch-analysis-ik-7.11.2.zip
RUN elasticsearch-plugin install --batch https://github.com/medcl/elasticsearch-analysis-pinyin/releases/download/v7.11.2/elasticsearch-analysis-pinyin-7.11.2.zip
