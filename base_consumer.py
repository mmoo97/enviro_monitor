#!/usr/bin/env python
import pika  # python client
import sys

credentials = pika.PlainCredentials('reggie', 'reggie')
parameters = pika.ConnectionParameters('ood',
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')  # create exchange to pass messages

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue  # creates a random name for the newly generated queue

nodes = sys.argv[1:]
if not nodes:
    sys.stderr.write("Usage: %s [ood] [ohpc] [manager]\n" % sys.argv[0])
    sys.exit(1)

for node in nodes:
    channel.queue_bind(
        exchange='direct_logs', queue=queue_name, routing_key=node)  # combine exchange, queue, and define routing name

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    print('[%r]  User creation task is done.' % method.routing_key)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)  # ingest messages, and assume delivered via auto_ack

channel.start_consuming()  # initiate message ingestion
