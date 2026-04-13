import pika

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import defs
import prot

CHAVE_PRIVADA = "priv_noti.der"


def valida_assinatura(msg, assinatura, quem):
	chave_publica = defs.CHAVE_PUBLICA[quem]

	key = RSA.import_key(open(chave_publica, 'rb').read())
	h = SHA256.new(msg)

	try:
		pkcs1_15.new(key).verify(h, assinatura)
		print("The signature is valid.")
		return True
	except (ValueError, TypeError):
		print("The signature is not valid.")
		return False

def gera_assinatura_msg(msg):
	key = RSA.import_key(open(CHAVE_PRIVADA, 'rb').read())
	msg = msg.encode()
	h = SHA256.new(msg)
	signature = pkcs1_15.new(key).sign(h)
	return signature

def inic_conec(exch):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	ch = connection.ch()

	ch.exchange_declare(exchange=exch, exchange_type='direct')
	ch.confirm_delivery()

	return connection, ch

def envia_msg(ch, msg, key, exch):
	ch.basic_publish(exchange=exch, routing_key=key, pacote=msg)

def inic_fila(ch, fila, exch):
	ch.queue_declare(queue=fila, durable=True, arguments={'x-queue-type': 'quorum'})
	ch.exchange_declare(exchange=exch, exchange_type='direct')

def bind_fila(ch, fila, exch, key):
	ch.queue_bind(exchange=exch, queue=fila, routing_key=key)

def consumir(ch, fila):
	ch.basic_consume(queue=fila, auto_ack=True, on_message_callback=callback)
	ch.start_consuming()

def le_fila(fila, exch):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	ch = connection.ch()

	inic_fila(ch, fila, exch)
	bind_fila(ch, fila, exch, defs.R_KEY_VALIDAS)
	consumir(ch, fila)

def callback(ch, method, properties, pacote):
	#pega sha do pacote
	SHA = prot.le_sha(pacote)
	#valida a chave com a função valida()
	prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))
	if valida_assinatura(pacote, SHA,defs.CHAVE_PUBLICA[defs.PROM]):
		n_keys = prot.le_n_rk(pacote)
		for i in range(n_keys): 
			key = prot.le_rk_num_n(i)
			envia_msg(ch,pacote, key,defs.EXCH)

def main():
	connection, ch = inic_conec(defs.EXCH)
	le_fila(defs.FILA_NOTIFICA, defs.EXCH)
	connection.close()

if __name__ == '__main__':
	main()
