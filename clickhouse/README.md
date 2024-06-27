### 1. Поднять кликхаус в докере

    ```
    docker run -d -e CLICKHOUSE_USER=admin_ch -e CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT=1 -e CLICKHOUSE_PASSWORD=pwd_ch -p 18123:8123 -p19000:9000 \
    -v ./ch_data:/var/lib/clickhouse/ \
    -v ./ch_logs:/var/log/clickhouse-server/ \
    --name new_ch_server --ulimit nofile=262144:262144 clickhouse/clickhouse-server
    ```
### 2. Настроить пользователя администратора
   [2.sql](https://github.com/IrinaDanilova-dev/WB-Practice-BI-OLAP/blob/main/clickhouse/2.sql)

### 3.  Создать базы для стейджинга, исторических данных, текущих данных и буферных таблиц
   [3.sql](https://github.com/IrinaDanilova-dev/WB-Practice-BI-OLAP/blob/main/clickhouse/3.sql)

### 4.  Создать роль только для чтения и роль с возможность создавать и заполнять данные в БД стейджинга(stg). Создать двух пользователей с такими правами по умолчанию.
   [4.sql](https://github.com/IrinaDanilova-dev/WB-Practice-BI-OLAP/blob/main/clickhouse/4.sql)

