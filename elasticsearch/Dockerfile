FROM docker.elastic.co/elasticsearch/elasticsearch:7.9.1

RUN elasticsearch-plugin install --batch https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.9.1/elasticsearch-analysis-ik-7.9.1.zip
RUN elasticsearch-plugin install --batch https://github.com/medcl/elasticsearch-analysis-pinyin/releases/download/v7.9.1/elasticsearch-analysis-pinyin-7.9.1.zip
