### 1. Поднять кликхаус в докере

    ```
    docker run -d -e CLICKHOUSE_USER=admin_ch -e CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT=1 -e CLICKHOUSE_PASSWORD=pwd_ch -p 18123:8123 -p19000:9000 \
    -v ./ch_data:/var/lib/clickhouse/ \
    -v ./ch_logs:/var/log/clickhouse-server/ \
    --name new_ch_server --ulimit nofile=262144:262144 clickhouse/clickhouse-server
    ```
### 2. Настроить пользователя администратора
    [2.sql](https://github.com/IrinaDanilova-dev/WB-Practice-BI-OLAP/blob/main/clickhouse/2.sql)
