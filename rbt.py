import pika

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import base64

import defs

# faz o hash e RSA e ve se bate com assinatura, se der ret True se não False
def valida_assinatura(msg, assinatura, quem):
	chave_publica = defs.CHAVE_PUBLICA[quem]

	key = RSA.import_key(open(chave_publica, 'rb').read())
	msg_bytes = "".join(msg).encode()
	h = SHA256.new(msg_bytes)

	try:
		assinatura_bytes = base64.b64decode(assinatura)
		pkcs1_15.new(key).verify(h, assinatura_bytes)
		return True
	except (ValueError, TypeError):
		return False
	
# faz o hash e RSA e ve se bate com assinatura, se der ret True se não False
def valida_assinatura_loja(msg, assinatura, chave_publica):

	key = RSA.import_key(open(chave_publica, 'rb').read())
	msg_bytes = "".join(msg).encode()
	h = SHA256.new(msg_bytes)

	try:
		assinatura_bytes = base64.b64decode(assinatura)
		pkcs1_15.new(key).verify(h, assinatura_bytes)
		return True
	except (ValueError, TypeError):
		return False
	
# gera um SHA da msg encodada.
def gera_assinatura_msg(msg, chave_priv):
	key = RSA.import_key(open(chave_priv, 'rb').read())
	h = SHA256.new(msg.encode())
	signature = pkcs1_15.new(key).sign(h)
	return base64.b64encode(signature).decode()

# cria o mago do RABITMQ
def inic_conec(exch):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	ch = connection.channel()
	ch.exchange_declare(exchange=exch, exchange_type='direct')
	ch.confirm_delivery()
	return connection, ch
# envia uma msg para uma chave parametro
def envia_msg(ch, msg, key, exch):
	ch.basic_publish(exchange=exch, routing_key=key, body=msg)
# cria uma nova fila
def inic_fila(ch, fila, exch):
	ch.queue_declare(queue=fila, durable=True, arguments={'x-queue-type': 'quorum'})
	ch.exchange_declare(exchange=exch, exchange_type='direct')
# inscreve a sua fila em uma determinada chave
def bind_fila(ch, fila, exch, key):
	ch.queue_bind(exchange=exch, queue=fila, routing_key=key)