from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from clickhouse_driver import Client

import os
import pandas as pd
import json
from datetime import datetime
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Нужно указать, чтобы spark подгрузил lib для kafka.
os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars org.apache.spark:spark-sql-kafka-0-10_2.12-3.5.0 --packages org.apache.spark:spark-sql-kafka-0-10_2.12-3.5.0 pyspark-shell'

# Загружаем конекты. Не выкладываем в гит файл с конектами.
with open('/opt/spark/Streams/credentials.json') as json_file:
    сonnect_settings = json.load(json_file)

ch_db_name = "default"
ch_dst_table = "tarificator0"

client = Client(сonnect_settings['ch_local'][0]['host'],
                user=сonnect_settings['ch_local'][0]['user'],
                password=сonnect_settings['ch_local'][0]['password'],
                verify=False,
                database=ch_db_name,
                settings={"numpy_columns": True, 'use_numpy': True},
                compression=True)

# Разные переменные, задаются в params.json
spark_app_name = "tarificator_edu"
spark_ui_port = "8081"

kafka_host = сonnect_settings['kafka'][0]['host']
kafka_port = сonnect_settings['kafka'][0]['port']
kafka_user = сonnect_settings['kafka'][0]['user']
kafka_password = сonnect_settings['kafka'][0]['password']
kafka_topic = "topic_tarificator"
kafka_batch_size = 50000
processing_time = "50 second"

checkpoint_path = f'/opt/kafka_checkpoint_dir/{spark_app_name}/{kafka_topic}/v1'

# Создание сессии спарк.
spark = SparkSession \
    .builder \
    .appName(spark_app_name) \
    .config('spark.ui.port', spark_ui_port)\
    .config("spark.dynamicAllocation.enabled", "false") \
    .config("spark.executor.cores", "1") \
    .config("spark.task.cpus", "1") \
    .config("spark.num.executors", "1") \
    .config("spark.executor.instances", "1") \
    .config("spark.default.parallelism", "1") \
    .config("spark.cores.max", "1") \
    .config('spark.ui.port', spark_ui_port)\
    .getOrCreate()

# убираем разные Warning.
spark.sparkContext.setLogLevel("WARN")
spark.conf.set("spark.sql.adaptive.enabled", "false")
spark.conf.set("spark.sql.debug.maxToStringFields", 500)

# Описание как создается процесс spark structured streaming.
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", f"{kafka_host}:{kafka_port}") \
    .option("subscribe", kafka_topic) \
    .option("maxOffsetsPerTrigger", kafka_batch_size) \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .option("forceDeleteTempCheckpointLocation", "true") \
    .option("kafka.sasl.jaas.config", f'org.apache.kafka.common.security.plain.PlainLoginModule required username="{kafka_user}" password="{kafka_password}";') \
    .option("kafka.sasl.mechanism", "PLAIN") \
    .option("kafka.security.protocol", "SASL_PLAINTEXT") \
    .load()

# Колонки, которые писать в ClickHouse. В kafka много колонок, не все нужны. Этот tuple нужен перед записью в ClickHouse.
columns_to_ch = ("oper_dt", "create_dt", "barcode", "prodtype_id", "prodtype_code", "employee_id", "currency_id", "rate", "amount", "rate_dt", "wh_id", "pay_part")


# Схема сообщений в топике kafka. Используется при формировании batch.
schema = StructType([
    StructField("oper_dt", StringType(), True),
    StructField("create_dt", StringType(), True),
    StructField("barcode", StringType(), True),
    StructField("prodtype_id", LongType(), False),
    StructField("prodtype_code", StringType(), True),
    StructField("employee_id", LongType(), False),
    StructField("currency_id", LongType(), False),
    StructField("rate", StringType(), False),
    StructField("amount", StringType(), False),
    StructField("rate_dt", StringType(), True),
    StructField("wh_id", LongType(), True),
    StructField("pay_part", StringType(), False),
    StructField("ext", StringType(), False),
    StructField("is_credit", BooleanType(), True),
    StructField("office_id", LongType(), True),
    StructField("oper_d", StringType(), True),
    StructField("dt_load", StringType(), True),
    StructField("shk_id", LongType(), False),
    StructField("js_ext",  StringType(), True),
    StructField("mp", StringType(), True),
    StructField("msk_dt", StringType(), True),
    StructField("payment_type", LongType(), False),
    StructField("calc_date_8", StringType(), True),
    StructField("calc_date", StringType(), True),
    StructField("entry", StringType(), True),
    StructField("price_rub", LongType(), False),
])

sql_tmp_create = """
   CREATE TABLE tmp.tmp_tarificator0
        (
            `oper_dt` DateTime ,
            `create_dt` DateTime ,
            `barcode` String ,
            `prodtype_id` UInt64 ,
            `prodtype_code` LowCardinality(String) ,
            `employee_id` UInt32 ,
            `currency_id` UInt16 ,
            `rate` Decimal(15, 2) ,
            `amount` Decimal(15, 2) ,
            `rate_dt` DateTime,
            `wh_id` UInt16,
            `pay_part` Decimal(15, 2)
        )
         engine = Memory
"""

sql_insert = f"""insert into {ch_db_name}.{ch_dst_table}
    select oper_dt, create_dt, barcode, prodtype_id, prodtype_code, employee_id, currency_id, rate, amount, rate_dt, wh_id, pay_part, prod_type_part_id
    from tmp.tmp_tarificator0 t1
    left any join
    (
        select prodtype_id, ProdTypePart_id prod_type_part_id
        from default.dict_ProdTypePartsGuide 
        where prodtype_id in (select prodtype_id from tmp.tmp_tarificator0)
    ) prt
    on t1.prodtype_id = prt.prodtype_id
"""

client.execute("drop table if exists tmp.tmp_tarificator0")

def column_filter(df):
    # select только нужные колонки.
    col_tuple = []
    for col in columns_to_ch:
        col_tuple.append(f"value.{col}")
    return df.selectExpr(col_tuple)


def load_to_ch(df):
    # Преобразуем в dataframe pandas и записываем в ClickHouse.
    df_pd = df.toPandas()
    df_pd.oper_dt = pd.to_datetime(df_pd.oper_dt, format='ISO8601', utc=True, errors='ignore')-pd.Timedelta(hours=3) 

    print('df_pd')
    print(df_pd)
    
    client.insert_dataframe('INSERT INTO tmp.tmp_tarificator0 VALUES', df_pd)

# Функция обработки batch. На вход получает dataframe-spark.
def foreach_batch_function(df2, epoch_id):

    df_rows = df2.count()
    # Если dataframe не пустой, тогда продолжаем.

    if df_rows > 0:
        # df2.printSchema()
        # df2.show(5)

        # Убираем не нужные колонки.
        df2 = column_filter(df2)

        client.execute(sql_tmp_create)      

        # Записываем dataframe в ch.
        load_to_ch(df2)

        # Добавляем объем и записываем в конечную таблицу.
        client.execute(sql_insert)
        client.execute("drop table if exists tmp.tmp_tarificator0")


# Описание как создаются микробатчи. processing_time - задается вначале скрипта
query = df.select(from_json(col("value").cast("string"), schema).alias("value")) \
    .writeStream \
    .trigger(processingTime=processing_time) \
    .option("checkpointLocation", checkpoint_path) \
    .foreachBatch(foreach_batch_function) \
    .start()

query.awaitTermination()
