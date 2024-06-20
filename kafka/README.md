### 1. поднять в docker-compose, из репозитория + sasl

  docker compose up -d

  ARN[0000] /home/id/docker_dev/docker-compose.yml: `version` is obsolete 
  NAME        IMAGE                          COMMAND                  SERVICE     CREATED         STATUS         PORTS
  kafka       confluentinc/cp-kafka:latest   "/etc/confluent/dock…"   kafka       2 minutes ago   Up 2 minutes   0.0.0.0:9092-9093->9092-9093/tcp, :::9092-9093->9092-9093/tcp
  zookeeper   zookeeper:latest               "/docker-entrypoint.…"   zookeeper   2 minutes ago   Up 2 minutes   2888/tcp, 3888/tcp, 8080/tcp, 0.0.0.0:1560->2181/tcp, :::1560->2181/tcp

### 2.   создать топик
   ![Image alt](https://github.com/IrinaDanilova-dev/WB-Practice-BI-OLAP/raw/main/kafka/images/kafka_with_ssl.jpg)

### 3. python скрипт для заливки данных 
    producer_with_sasl_from_ch.py

### 4. результат в Offset Explorer
   ![Image alt](https://github.com/IrinaDanilova-dev/WB-Practice-BI-OLAP/raw/main/kafka/images/topic_prod_type_parts.jpg)

### 5. чтение из топика питоном
python скрипт:consumer_without_SASL.py 
```
Received message: {"prodtype_id": 1001, "prodtype_code": "assembly_mezo_small_qty", "prodtype_name": "Сборка малой волны", "is_deleted": 1, "is_credit": 0, "is_credit_kpi": 0}            
Received message: {"prodtype_id": 1002, "prodtype_code": "assembly_mezo_big_qty", "prodtype_name": "Сборка по заявке", "is_deleted": 1, "is_credit": 0, "is_credit_kpi": 0}      
Received message: {"prodtype_id": 1003, "prodtype_code": "assembly_byrow_qty", "prodtype_name": "Сборка порядная", "is_deleted": 1, "is_credit": 0, "is_credit_kpi": 0}
Received message: {"prodtype_id": 1004, "prodtype_code": "assembly_by_stream_qty", "prodtype_name": "Сборка", "is_deleted": 0, "is_credit": 0, "is_credit_kpi": 0}
Received message: {"prodtype_id": 1005, "prodtype_code": "assembly_by_stream_size", "prodtype_name": "Сборка Oбъем", "is_deleted": 0, "is_credit": 0, "is_credit_kpi": 0}
Received message: {"prodtype_id": 1006, "prodtype_code": "assembly_by_stream_liter", "prodtype_name": "Сборка в литрах", "is_deleted": 0, "is_credit": 0, "is_credit_kpi": 0}
Received message: {"prodtype_id": 1007, "prodtype_code": "qty_scan_bulky_ship", "prodtype_name": "Сборка с передачей крупногабарит", "is_deleted": 0, "is_credit": 0, "is_credit_kpi": 0}
Received message: {"prodtype_id": 1021, "prodtype_code": "assembly_safe_small_qty", "prodtype_name": "Сборка малой волны сейф", "is_deleted": 1, "is_credit": 0, "is_credit_kpi": 0}
Received message: {"prodtype_id": 1022, "prodtype_code": "assembly_safe_big_qty", "prodtype_name": "Сборка большой волны сейф", "is_deleted": 1, "is_credit": 0, "is_credit_kpi": 0}
Received message: {"prodtype_id": 1031, "prodtype_code": "issue_from_safe", "prodtype_name": "Передача из супер-сейфа", "is_deleted": 0, "is_credit": 0, "is_credit_kpi": 0}
Received message: {"prodtype_id": 1101, "prodtype_code": "assembly_mezo_small_virt_qty", "prodtype_name": "Сборка малой волны баркод", "is_deleted": 1, "is_credit": 0, "is_credit_kpi": 0}
Received message: {"prodtype_id": 1102, "prodtype_code": "assembly_mezo_big_virt_qty", "prodtype_name": "Сборка большой волны баркод", "is_deleted": 1, "is_credit": 0, "is_credit_kpi": 0}
Received message: {"prodtype_id": 1103, "prodtype_code": "assembly_byrow_virt_qty", "prodtype_name": "Сборка порядная баркод", "is_deleted": 1, "is_credit": 0, "is_credit_kpi": 0}
...
```
