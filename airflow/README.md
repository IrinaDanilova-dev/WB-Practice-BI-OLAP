### Домашнее задание по Airflow:
Установить локально Airflow, ClickHouse, Postgres. Не забыть про то, что им нужно общаться, решайте сами, кому как удобно - через ip хоста или через добавления ClickHouse и Postgres в сеть Airflow.
Сделать даг, берущий данные из вашего локального ClickHouse, как-то их трансформирующий (не обязательно, но желательно), а затем кладущий в витрину на том же клике (сделать схему reports). После этого даг должен взять данные из только что созданной витрины, преобразовать в датафрейм пандас, и заинсертить их в Postgres по методологии, рассказанной Львом на лекции по Postgres (процедура импорта).
В репозиторий гит выложить:
Даг.
Скрин, что даг успешно отработал
Скрин с данными из витрины Postgres



### 1. Даг в  Airflow
   [report_tarifiсator_by_prod_type_parts.py](https://github.com/IrinaDanilova-dev/WB-Practice-BI-OLAP/tree/main/airflow/report_tarifiсator_by_prod_type_parts.py)    

### 2. Скрин, что даг успешно отработал
   ![dag_airflow.png](https://github.com/IrinaDanilova-dev/WB-Practice-BI-OLAP/blob/main/airflow/dag_airflow.png)  
    
### 3. Скрин с данными из витрины Postgres    
   ![pg_data.png](https://github.com/IrinaDanilova-dev/WB-Practice-BI-OLAP/blob/main/airflow/pg_data.png)  

  скрипт для создания таблицы , процедуры вставки, функции для чтения
   [pg_airflow.sql](https://github.com/IrinaDanilova-dev/WB-Practice-BI-OLAP/blob/main/airflow/pg_airflow.sql)  

  данные из витрины в формате json
   ![pg_data_json.png](https://github.com/IrinaDanilova-dev/WB-Practice-BI-OLAP/blob/main/airflow/pg_data_json.png)  



