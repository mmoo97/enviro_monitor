import pika
import sys

# Begin RabbitMQ process.
credentials = pika.PlainCredentials('reggie', 'reggie')
parameters = pika.ConnectionParameters('ood',
                                       5672,
                                       '/',
                                       credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

node = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(
    exchange='direct_logs', routing_key=node, body=message)
print(" [x] Sent %r:%r" % (node, message))

connection.close()
