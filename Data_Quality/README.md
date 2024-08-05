### ДЗ Data Quality
собрать метрики качества данных по вашей таблице в локальном клике в таблицу.
поднять DataLens.
    В гит выложить:
sql-запрос на сбор метрик качества данных
скрин дашборда



### 1. sql-запрос на сбор метрик качества данных
```
create database dq;
create table dq.tarificator_by_wh_hour_emp_ptype
    engine = ReplacingMergeTree() order by dt_hour as
select dt_hour
     , count()                                            rows_qty
     , uniq(employee_id)                                  employee_id_uniq
     , uniq(wh_id)                                        wh_id_uniq
     , uniq(prodtype_id)                                  prodtype_id_uniq
     , uniq(prod_type_part_id)                            prod_type_part_id_uniq
     , countIf(wh_id < 1)                                 wh_id_0_qty
     , countIf(prodtype_id < 1)                           prodtype_id_0_qty
     , countIf(prod_type_part_id < 1)                     prod_type_part_id_0_qty
     , countIf(qty < 1)                                   qty_0_qty
     , countIf(amount_sum < 1 and prod_type_part_id != 7) amount_sum_0_qty
from default.tarificator_by_wh_hour_emp_ptype
where dt_hour >= today() - interval 1 day
group by dt_hour;   
```
### 2. скрин дашборда
   ![datalens.png](https://github.com/IrinaDanilova-dev/WB-Practice-BI-OLAP/blob/main/Data_Quality/datalens.PNG)  
    



