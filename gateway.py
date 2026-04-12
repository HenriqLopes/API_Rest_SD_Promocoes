import pika

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import defs

CHAVE_PRIVADA = "priv_gate.der"

def valida_assinatura(msg, assinatura, quem):
	chave_publica = CHAVE_PUBLICA[quem]

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
	channel = connection.channel()

	channel.exchange_declare(exchange=exch, exchange_type='direct')
	channel.confirm_delivery()

	return connection, channel

def envia_msg(channel, msg, key, exch):
	channel.basic_publish(exchange=exch, routing_key=key, body=msg)

if __name__ == '__main__':
	main()

def inic_fila(channel, fila, exch):
	channel.queue_declare(queue=fila, durable=True, arguments={'x-queue-type': 'quorum'})
	channel.exchange_declare(exchange=exch, exchange_type='direct')

def bind_fila(channel, fila, exch, key):
	channel.queue_bind(exchange=exch, queue=fila, routing_key=key)

def consumir(channel, fila):
	channel.basic_consume(queue=fila, auto_ack=True, on_message_callback=callback)
	channel.start_consuming()

def le_fila(fila, exch):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()

	inic_fila(channel, fila, exch)
	bind_fila(channel, fila, exch, defs.R_KEY_GATEWAY)
	consumir(channel, fila)

def callback(ch, method, properties, body):
	print(f" [x] Received {body}")

def interface_cliente():
	print("[1] Adicionar nova promoção \n [2] Listar promoções \n [3] Votar promoções" )

def main():

	#essa função vai entrar em um loop infinito de leitura
	#le_fila(defs.FILA_GATEWAY, defs.EXCH_GATEWAY)

	#essa parada aqui, vai ter que ser uma parte do callback, leu enviou pq leu sabe, pq ler e mandar sem ser com thread vai dar pau
	connection, channel = inic_conec(defs.EXCH)
	#enviar pra promo
	envia_msg(channel, "TESTE_GATE_PROMO", defs.R_KEY_PROMOCAO, defs.EXCH)

	connection.close()

def comando_cliente():
	return

def mostra_lista_promo(cliente, promocoes):
	print(f"=== PROMOÇÕES DISPONÍVEIS ===")

	encontrou_promo = False

	for promo in promocoes.values():
		#Tem que colocar aqui direito a parte das categorias do cliente, porque não sei como vai ficar
		if promo['n_rk'] in cliente:
			print(f"  Categoria: {promo['categoria']}")
			print(f"  [{promo['id_promo']}] {promo['promo']}")
			encontrou_promo = True

	if encontrou_promo == False:
		print("  Nenhuma promoção disponível para suas categorias.")


def define_promo():
	#Promos que serão hardcoded pré execução
	promos = {
		#R_KEY_PROM_LIVRO = 'rk_livr'
		"id_promo" : {"ini_bits_SHA":0, "tam_bits_SHA":32, "nome_promo":"faz o L", "promo_id":0, "n_rk": 0 , "rk_1":0, "rk_2":0},

		#R_KEY_PROM_ROUPA = 'rk_roup'
		"id_promo" : {"ini_bits_SHA":0, "tam_bits_SHA":32, "nome_promo":"faz o L", "promo_id":0, "n_rk": 0 , "rk_1":0, "rk_2":0},

		#R_KEY_PROM_ESPORTE = 'rk_espo'
		"id_promo" : {"ini_bits_SHA":0, "tam_bits_SHA":32, "nome_promo":"faz o L", "promo_id":0, "n_rk": 0 , "rk_1":0, "rk_2":0},

		#R_KEY_PROM_DOMESTICO = 'rk_dome'
		"id_promo" : {"ini_bits_SHA":0, "tam_bits_SHA":32, "nome_promo":"faz o L", "promo_id":0, "n_rk": 0 , "rk_1":0, "rk_2":0},

		#R_KEY_PROM_COMIDA = 'rk_comi'
		"id_promo" : {"ini_bits_SHA":0, "tam_bits_SHA":32, "nome_promo":"faz o L", "promo_id":0, "n_rk": 0 , "rk_1":0, "rk_2":0}
	}
	return promos

def envia_promo():
	#monta um pacote com as info de uma promo
	#assina e chaveia
	#envia pra valida promo
	return

def envia_voto():
	#monta um pacote com as info de uma promo
	#assina e chaveia
	#envia pro rank
	return