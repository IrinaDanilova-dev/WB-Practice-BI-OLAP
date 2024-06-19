1. поднять в docker-compose, из репозитория + sasl

docker compose up -d

ARN[0000] /home/id/docker_dev/docker-compose.yml: `version` is obsolete 
NAME        IMAGE                          COMMAND                  SERVICE     CREATED         STATUS         PORTS
kafka       confluentinc/cp-kafka:latest   "/etc/confluent/dock…"   kafka       2 minutes ago   Up 2 minutes   0.0.0.0:9092-9093->9092-9093/tcp, :::9092-9093->9092-9093/tcp
zookeeper   zookeeper:latest               "/docker-entrypoint.…"   zookeeper   2 minutes ago   Up 2 minutes   2888/tcp, 3888/tcp, 8080/tcp, 0.0.0.0:1560->2181/tcp, :::1560->2181/tcp
