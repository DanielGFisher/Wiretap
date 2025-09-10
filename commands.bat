docker pull mongo

docker run -d --name my-mongodb -p 27017:27017 mongo

docker network create elastic

docker pull docker.elastic.co/elasticsearch/elasticsearch:9.1.3

docker run --name elasticsearch --net elastic -p 9200:9200 -e discovery.type=single-node -e ES_JAVA_OPTS="-Xms1g -Xmx1g" -e xpack.security.enabled=false -it docker.elastic.co/elasticsearch/elasticsearch:9.1.3

docker pull docker.elastic.co/kibana/kibana:9.1.3

docker run --name kibana --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:9.1.3