import pika

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import defs
import prot

import base64

CHAVE_PRIVADA = "chaves_privadas/priv_prom.der"

# faz o hash e RSA e ve se bate com assinatura, se der ret True se não False
def valida_assinatura(msg, assinatura, quem):
	chave_publica = defs.CHAVE_PUBLICA[quem]

	key = RSA.import_key(open(chave_publica, 'rb').read())
	h = SHA256.new("".join(msg).encode())

	try:
		assinatura_bytes = base64.b64decode(assinatura)
		pkcs1_15.new(key).verify(h, assinatura_bytes)
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
	signature_str = base64.b64encode(signature).decode()
	return signature_str

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
	print("[] pacote recebido")
	prot.print_pacote(pacote)

	#pega sha do pacote
	SHA = prot.le_sha(pacote)
	#limpa a sha do pacote
	prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))

	print("[] validando assinatura")
	#valida se a sha ta correta, se tiver add a promo na lista
	if valida_assinatura(pacote, SHA,defs.GATE):
		print("[] assinatura valida")
		prot.escreve_sha(pacote,gera_assinatura_msg(prot.pacote_para_string(pacote))) 
		print("[] postando promo como validada")
		envia_msg(ch, prot.pacote_para_string(pacote),defs.R_KEY_VALIDAS,defs.EXCH)
	else:
		print("[] assinatura invalida")

def main():
	connection, ch = inic_conec(defs.EXCH)
	print("[] conexão iniciada")
	inic_fila(ch, defs.FILA_PROMOCAO, defs.EXCH)
	print("[] fila iniciada iniciada")
	bind_fila(ch, defs.FILA_PROMOCAO, defs.EXCH, defs.R_KEY_PROMOCAO)
	print("[] iniciando consumo")
	consumir(ch, defs.FILA_PROMOCAO)
	connection.close()

if __name__ == '__main__':
	main()
