from influxdb import InfluxDBClient
import pika
import json
from dotenv import load_dotenv
import os

load_dotenv('..')

database = InfluxDBClient(host='localhost', port=8086, username=os.getenv('INFLUXDB_USERNAME'), password=os.getenv('INFLUXDB_PASSWORD'), ssl=False, verify_ssl=False, database='db0')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='persistence')

def callback(ch, method, properties, body):
    #print(" [x] Received new status!")
    obj = json.loads(body)
    data = [
    {
        "measurement": "status",
        "tags": {
            "track": obj["track"]
        },
        "time": obj["time"],
        "fields": obj
    }]
    database.write_points(data)


channel.basic_consume(queue='persistence', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

