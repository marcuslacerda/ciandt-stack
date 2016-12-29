FROM kibana:4.6.3
MAINTAINER mlacerda@ciandt.com

# install open or custom plugins
RUN kibana plugin --install heatmap -u https://github.com/stormpython/heatmap/archive/master.zip
RUN kibana plugin --install tagcloud -u https://github.com/stormpython/tagcloud/archive/master.zip
RUN kibana plugin --install oauth2 -u https://github.com/marcuslacerda/kibana-oauth2-plugin/releases/download/0.2.1/kibana-oauth2-plugin-0.2.1.zip

# fix kibana 4.5 and sense plugin
RUN chmod o+w /opt/kibana/optimize/.babelcache.json

#ENTRYPOINT ["/docker-entrypoint.sh"]
#CMD ["kibana"]
