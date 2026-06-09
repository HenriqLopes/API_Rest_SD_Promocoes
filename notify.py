import pika

import defs
import prot

<<<<<<< HEAD
import base64
=======
import rbt
>>>>>>> f7890056d7cf3a5d0c365b4a0674334836fd3486

#bibliotecas necessárias para envio do e-mail
import os
from dotenv import load_dotenv
import resend 

CHAVE_PRIVADA = "chaves_privadas/priv_noti.der"

<<<<<<< HEAD
# Pega a chave da API_RESEND do .env
load_dotenv()

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
=======
>>>>>>> f7890056d7cf3a5d0c365b4a0674334836fd3486
# bloqueia eternamente pra ficar só consumindo sua fila
def consumir(ch, fila):
	ch.basic_consume(queue=fila, auto_ack=True, on_message_callback=callback)
	ch.start_consuming()
# função chamada sempre que um pacote é lido
def callback(ch, method, properties, pacote):
	pacote = list(chr(b) for b in pacote)
	print("[] pacote recebido")
	#prot.print_pacote(pacote)

	#pega sha do pacote
	SHA = prot.le_sha(pacote)
	#limpa a sha do pacote
	prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))

	print("[] validando assinatura")
	if rbt.valida_assinatura(pacote, SHA,defs.PROM):
		print("[] assinatura valida")
		n_keys = prot.le_n_rk(pacote)
		print(f"[] publicando em {n_keys} tags")
		#envia para todas as chaves da promo
		for i in range(n_keys): 
			key = prot.le_rk_num_n(pacote, i + 1)
			print(f"[] enviando para tag: {defs.R_KEYS[key]}")
			rbt.envia_msg(ch, prot.pacote_para_string(pacote), defs.R_KEYS[key], defs.EXCH)
	else:
		print("[] assinatura invalida")

def main():
	connection, ch = rbt.inic_conec(defs.EXCH)
	print("[] conexão iniciada")
	rbt.inic_fila(ch, defs.FILA_NOTIFICA, defs.EXCH)
	print("[] fila iniciada")
	rbt.bind_fila(ch, defs.FILA_NOTIFICA, defs.EXCH, defs.R_KEY_VALIDAS)
	print("[] iniciando consumo")
	consumir(ch, defs.FILA_NOTIFICA)
	connection.close()

# Envia e-mail avisando que a promoção é uma hotdeal
def envia_email(id_promo, nome_promo, email_loja):
	#Pega a API do resend do .env
	resend.api_key = os.getenv("API_RESEND")

	r = resend.Emails.send({
		"from": "onboarding@resend.dev",
		"to": "henriquelopesdebarros12345@gmail.com",
		"subject": "${id_promo}: ${nome_promo} ",
		"html": "<p>Parabéns, sua promooção <strong>ID: ${id_promo} ${nome_promo}</strong> virou um <strong>HOT-DEAL</strong>!</p>"
	})

if __name__ == '__main__':
	main()
