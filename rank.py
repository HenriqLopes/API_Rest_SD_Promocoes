import pika

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import defs
import prot

import base64

dict_promo = {}

CHAVE_PRIVADA = "chaves_privadas/priv_rank.der"

VOTES_HOT_DEAL = 5

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
	global dict_promo
	
	pacote = list(chr(b) for b in pacote)
	print("[] pacote recebido")
	prot.print_pacote(pacote)

	#pega sha do pacote
	SHA = prot.le_sha(pacote)
	#limpa a sha do pacote
	prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))

	print("[] validando assinatura")
	#valida se a sha ta correta, se tiver add a promo na lista
	if valida_assinatura(pacote, SHA, defs.GATE):
		print("[] assinatura valida")
		id = prot.le_id(pacote)

		if id in dict_promo:
			pac, n = dict_promo[id]
			n += 1
			print(f"[] promo de id {id} com {n} votos")
			if n > VOTES_HOT_DEAL:
				prot.escreve_sha(pacote,(gera_assinatura_msg(prot.chars_para_str(pacote)))) 
				print(f"[] enviando para tag: {defs.R_KEYS[defs.PROM_QUENTES]}")
				envia_msg(ch, prot.pacote_para_string(pacote), defs.R_KEYS[defs.PROM_QUENTES], defs.EXCH)
			dict_promo[id] = (pac, n)
		else:
			dict_promo[id] = (pacote, 1)
			print(f"[] promo de id {id} com {1} voto")
	else:
		print("[] assinatura invalida")

def main():
	connection, ch = inic_conec(defs.EXCH)
	print("[] conexão iniciada")
	inic_fila(ch, defs.FILA_RANKING, defs.EXCH)
	print("[] fila iniciada")
	bind_fila(ch, defs.FILA_RANKING, defs.EXCH, defs.R_KEY_RANKING)
	print("[] iniciando consumo")
	consumir(ch, defs.FILA_RANKING)
	connection.close()

if __name__ == '__main__':
	main()