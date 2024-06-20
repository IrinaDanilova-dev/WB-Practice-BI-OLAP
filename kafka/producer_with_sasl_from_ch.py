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
        producer.produce('topic_prod_type_parts', data.encode('utf-8'), callback=delivery_report)
        producer.poll(0)  # Поллинг для обработки обратных вызовов
    except BufferError:
        print(f"Local producer queue is full ({len(producer)} messages awaiting delivery): try again")

def get_data_from_ch(database,table):

    client=connect_CH()

    table_data = client.execute(f"""select * from {database}.{table} limit 100""")

    list_of_dicts=[]

    columns_data0= client.execute( f"""select name from system.columns where database='{database}' and  table='{table}'""")
    columns_data=[]
    for col_i in columns_data0:
        columns_data.append(col_i[0])

    print(columns_data)
    for row_i in table_data:
        dict_i=dict(zip(columns_data, row_i))
        list_of_dicts.append(dict_i)

    json_data=json.dumps(list_of_dicts)
    return json_data



if __name__ == '__main__':
    data_from_ch=get_data_from_ch('default', 'dict_ProdType')
    for row in data_from_ch:
        send_message(row)
    producer.flush()


