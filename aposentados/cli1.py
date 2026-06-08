import pika

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import defs
import prot

FILA = 'fl_cli1'
RK_1 = defs.R_KEYS[defs.PROM_COMIDA]
RK_2 = defs.R_KEYS[defs.PROM_QUENTES]

# cria o mago do RABITMQ
def inic_conec(exch):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	ch = connection.channel()

	ch.exchange_declare(exchange=exch, exchange_type='direct')
	ch.confirm_delivery()

	return connection, ch
# cria uma nova fila
def inic_fila(ch, fila, exch):
	ch.queue_declare(queue=fila, durable=True, arguments={'x-queue-type': 'quorum'})
	ch.exchange_declare(exchange=exch, exchange_type='direct')
#inscreve a sua fila em uma determinada chave
def bind_fila(ch, fila, exch, key):
	ch.queue_bind(exchange=exch, queue=fila, routing_key=key)
# bloqueia eternamente pra ficar só consumindo sua fila
def consumir(ch, fila):
	ch.basic_consume(queue=fila, auto_ack=True, on_message_callback=callback)
	ch.start_consuming()
# função chamada sempre que um pacote é lido
def callback(ch, method, properties, pacote):
	pacote = list(chr(b) for b in pacote)
	print("[] pacote recebido")
	print (f"[] nova promo {prot.le_id(pacote)}: {prot.le_nome(pacote)}")
	#prot.print_pacote(pacote)

def main():
	connection, ch = inic_conec(defs.EXCH)
	print("[] conexão iniciada")
	inic_fila(ch, FILA, defs.EXCH)
	print("[] fila iniciada iniciada")
	bind_fila(ch, FILA, defs.EXCH, RK_1)
	print(f"[] interessado em {RK_1}")
	bind_fila(ch, FILA, defs.EXCH, RK_2)
	print(f"[] interessado em {RK_2}")
	print("[] iniciando consumo")
	consumir(ch, FILA)
	connection.close()

if __name__ == '__main__':
	main()
