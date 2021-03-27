# Elasticsearch

```bash
$ docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" maguowei/elasticsearch
```

## Plugins

- [elasticsearch-analysis-ik](https://github.com/medcl/elasticsearch-analysis-ik)
- [elasticsearch-analysis-pinyin](https://github.com/medcl/elasticsearch-analysis-pinyin)
