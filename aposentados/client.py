import pika
import defs

if __name__ == '__main__':
	main()

def inic_fila(channel, exch):
	channel.queue_declare(durable=True, arguments={'x-queue-type': 'quorum'})
	channel.exchange_declare(exchange=exch, exchange_type='direct')

def bind_fila(channel, exch, key):
	channel.queue_bind(exchange=exch, routing_key=key)

def consumir(channel):
	channel.basic_consume(auto_ack=True, on_message_callback=callback)
	channel.start_consuming()

def le_fila(exch):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()

	inic_fila(channel, exch)
	bind_fila(channel, exch, defs.R_KEY_PROM_COMIDA)
	bind_fila(channel, exch, defs.R_KEY_PROM_QUENTES)
	
	consumir(channel)

def callback(ch, method, properties, body):
	print(f" [x] Received {body}")

def read_name_protocol():
	return

def read_name_protocol():

	return

def main():
	le_fila(defs.EXCH)
	
