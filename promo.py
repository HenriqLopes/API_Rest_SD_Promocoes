import pika

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import defs
import prot

CHAVE_PRIVADA = "chaves_privadas/priv_prom.der"

# faz o hash e RSA e ve se bate com assinatura, se der ret True se não False
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
# gera um SHA da msg encodada.
def gera_assinatura_msg(msg):
	key = RSA.import_key(open(CHAVE_PRIVADA, 'rb').read())
	msg = msg.encode()
	h = SHA256.new(msg)
	signature = pkcs1_15.new(key).sign(h)
	return signature

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
# bloqueia eternamente pra ficar só consumindo sua fila
def consumir(ch, fila):
	ch.basic_consume(queue=fila, auto_ack=True, on_message_callback=callback)
	ch.start_consuming()
# função chamada sempre que um pacote é lido
def callback(ch, method, properties, pacote):
	pacote = list(chr(b) for b in pacote)
	#pega sha do pacote
	SHA = prot.le_sha(pacote)
	#limpa a sha do pacote
	prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))
	#valida se a sha ta correta, se tiver add a promo na lista
	if valida_assinatura(pacote, SHA,defs.GATE):
		prot.escreve_SHA(pacote,gera_assinatura_msg(prot.pacote_para_string(pacote))) 
		envia_msg(ch,pacote,defs.R_KEY_VALIDAS,defs.EXCH)

def main():
	connection, ch = inic_conec(defs.EXCH)
	inic_fila(ch, defs.FILA_PROMOCAO, defs.EXCH)
	bind_fila(ch, defs.FILA_PROMOCAO, defs.EXCH, defs.R_KEY_PROMOCAO)
	consumir(ch, defs.FILA_PROMOCAO)
	connection.close()

if __name__ == '__main__':
	main()
