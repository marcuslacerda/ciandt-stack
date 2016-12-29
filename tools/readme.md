# Docker Compose
Existe um docker componse que configura a inicialização dos serviços elasticsearch e kibana. O elasticsearch é utilizado como banco de dados para o Stack, enquando o Kibana pode ser utilizando para visualização de gráficos mais avançados.

```yaml
version: '2'
services:
    stack-elasticsearch:
        image: elasticsearch:2.4.3
        # volumes:
        #   - /home/mlacerda/data:/usr/share/elasticsearch/data
    stack-kibana:
        build: kibana/
        depends_on:
            - stack-elasticsearch
        environment:
            - ELASTICSEARCH_URL=http://stack-elasticsearch:9200
        volumes:
            - ./conf/kibana/kibana.yml:/opt/kibana/config/kibana.yml
    stack-nginx:
       image: nginx:1.11.8
       depends_on:
           - stack-elasticsearch
           - stack-kibana
       ports:
           - "80:80"
           - "9200:9200"
       volumes:
           # uncomment if you enable auth_basic on nginx
           # - ./conf/nginx/.htpasswd:/etc/nginx/.htpasswd
           - ./conf/nginx/nginx.conf:/etc/nginx/nginx.conf
```

## Elasticsearch
Alterar a configuração do volume para armazenar os dados em um diretório conhecido.
```
stack-elasticsearch:
    image: elasticsearch:2.4.3
    volumes:
       - /home/mlacerda/data:/usr/share/elasticsearch/data
```

## Kibana
Existe um dockerfile custom do Kibana para instalação de plugins para grãfico e autenticação oauth.

Para habilitar a autenticação oauth, será necessário alterar o arquivo conf/kibana/kibana.yml, informando o GOOGLE_CLIENT_IT e GOOGLE_CLIENT_SECRET

```yaml
oauth2.enabled: true
oauth2.clientId: <set-your-client-id>
oauth2.clientSecret: <set-client-secret>
oauth2.redirectUri
```
Opctionalmente, pode será necessário configurar o oauth2.redirectUri se existe um proxy/redirect para o seu kibana. Exemplo oauth2.redirectUri: https://techanalytics.ciandt.com



## Nginx
Configurado como proxy para Kibana e Elasticsearch. Kibana escuta na porta 80 enquanto o elasticsearch escuta na porta 9200.

```console
$ curl http://localhost:9200
$ curl http://localhost
```

# Google Spreadsheet - Knowledge Map

Knowledge Map Spreadsheet Addon permite elaborar um mapa de conhecimento técnico, recuperando informações de skill a partir de uma integração com [Tech Gallery][techgallery].

Essa [apresentação](https://docs.google.com/presentation/d/19kGlJn8RV-K60-jgcjh57NVSo5O838T98VfsrXe-Hh4/edit#slide=id.g16d5cef21f_0_262) explica mais detalhes sobre o funcionamento da planilha e como se dá a integração com o [Tech Gallery](https://github.com/ciandt-dev/tech-gallery).

Abaixo o link do webinar (video) e também o template da planilha.
* Link do Webinar (https://plus.google.com/u/0/events/c2evghng5fvhab0p1gn4vt7jqkg)
* Link do template (https://goo.gl/4VV4PU)

[techgallery]: https://github.com/ciandt-dev/tech-gallery
