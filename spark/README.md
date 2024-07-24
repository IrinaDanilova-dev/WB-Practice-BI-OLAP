### 1. Разворачиваем контейнеры 
    Папка  с docker-compose файлами для развертывания контейнеров: 
   [docker-kafka-spark](https://github.com/IrinaDanilova-dev/WB-Practice-BI-OLAP/tree/main/spark/docker-kafka-spark/)

### 2. Заливаем данные в кафку
    Было залито 399 строк из таблицы tarificator на сервере wh-olap-pegashard 
   ![kafka-data](https://github.com/IrinaDanilova-dev/WB-Practice-BI-OLAP/blob/main/spark/images/kafka-data.png)

   скрипты python в папке: 
   [kafka-py](https://github.com/IrinaDanilova-dev/WB-Practice-BI-OLAP/tree/main/spark/kafka-py)
    
### 3. Создаем таблицы на сервере clickhouse
    создали таблицу default.dict_ProdTypePartsGuide, справочник участков работ , аналогичную таблице на сервере wh-olap-pegashard
    CREATE TABLE default.dict_ProdTypePartsGuide
    (
        `prodtype_id` UInt64,
        `ProdTypePart_id` UInt16,
        `is_deleted` UInt8,
        `changing_employee_id` UInt64,
        `dt` UInt32
    )
    ENGINE = ReplacingMergeTree(dt)
    ORDER BY prodtype_id;
    залили туда данные с wh-olap-pegashard , путем импорта из файла .csv

    создали таблицу default.tarificator0 , которая будет принимать часть колонок из tarificator + колонка prod_type_part_id - id участка работ (ProdTypePart_id из dict_ProdTypePartsGuide)
    CREATE TABLE default.tarificator0
    (
        `oper_dt` DateTime COMMENT 'Время операции, отклонение на 3 часа вперед, на 6 для entry = \'LogisticOrhan\'',
        `create_dt` DateTime COMMENT 'Время загрузки операции',
        `barcode` String COMMENT 'Баркод (номер присвоенный от поставщика)',
        `prodtype_id` UInt64 COMMENT 'ID операции (словарь Prodtype)',
        `prodtype_code` LowCardinality(String) COMMENT 'Относится к типу операции (что-то типа расшифровки)',
        `employee_id` UInt32 COMMENT 'Сотрудник, совершивший операцию',
        `currency_id` UInt16 COMMENT 'Валюта',
        `rate` Decimal(15, 2) COMMENT 'Тариф',
        `amount` Decimal(15, 2) COMMENT 'Итоговая сумма начисленного по операции',
        `rate_dt` DateTime COMMENT 'Дата установки тарифа',
        `wh_id` UInt16 COMMENT 'Блок, на котором была совершена операция',
        `pay_part` Decimal(15, 2) COMMENT 'Коефициент, на который умножается тариф для формирования суммы',
        `prod_type_part_id` UInt16
    )
    ENGINE = MergeTree()
    PARTITION BY toStartOfWeek(oper_dt)
    ORDER BY (prodtype_id, oper_dt);
