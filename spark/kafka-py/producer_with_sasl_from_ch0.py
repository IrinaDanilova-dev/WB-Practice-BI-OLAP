from confluent_kafka import Producer
from Connect_DB import connect_CH
import json

config = {
    'bootstrap.servers': 'localhost:9093',  # адрес Kafka сервера
    'client.id': 'simple-producer',
    'sasl.mechanism':'PLAIN',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.username': 'admin',
    'sasl.password': 'admin-secret'
}

producer = Producer(**config)

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def send_message(data):
    try:
        # Асинхронная отправка сообщения
        
        producer.produce('topic_tarificator', data.encode('utf-8'), callback=delivery_report)
        producer.poll(0)  # Поллинг для обработки обратных вызовов
    except BufferError:
        print(f"Local producer queue is full ({len(producer)} messages awaiting delivery): try again")

def get_data_from_ch(database,table):

    client=connect_CH()

    table_data = client.execute(f"""select * from {database}.{table} where oper_dt>=now() +interval 3 hour - interval 3 minute limit 5 by prodtype_id """)

    list_of_json=[]

    columns_data0= client.execute( f"""select name from system.columns where database='{database}' and  table='{table}' """)
    columns_data=[]
    for col_i in columns_data0:
        columns_data.append(col_i[0])

    print(columns_data)
    for row_i in table_data:
        dict_i=json.dumps(dict(zip(columns_data, row_i)),ensure_ascii=False, default=str)
        list_of_json.append(dict_i)
    return (list_of_json)



if __name__ == '__main__':
    data_from_ch=get_data_from_ch('default', 'tarificator')
    for row in data_from_ch:
        send_message(row)
    producer.flush()

