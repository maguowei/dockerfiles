# Elasticsearch

预装 IK 分词和拼音插件的 Elasticsearch 镜像。

```bash
docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" -e "xpack.security.enabled=false" \
  maguowei/elasticsearch
```

## 插件

- [elasticsearch-analysis-ik](https://github.com/medcl/elasticsearch-analysis-ik)
- [elasticsearch-analysis-pinyin](https://github.com/medcl/elasticsearch-analysis-pinyin)
