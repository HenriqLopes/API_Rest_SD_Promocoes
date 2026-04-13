import pika

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import defs
import prot

dict_promo = {}

CHAVE_PRIVADA = "priv_gate.der"

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
	bind_fila(ch, fila, exch, defs.R_KEY_GATEWAY)
	consumir(ch, fila)

def callback(ch, method, properties, pacote):
	#pega sha do pacote
	SHA = prot.le_sha(pacote)
	#valida a chave com a função valida()
	prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))
	if valida_assinatura(pacote, SHA,defs.CHAVE_PUBLICA[defs.PROM]):
		dict_promo[pacote['id']] = pacote
	ch.stop_consuming()

def interface_cliente():
	return input("[1] Adicionar nova promoção \n [2] Listar promoções \n [3] Votar promoções")

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


def envia_pacote(dados, destino):
	# monta o pacote
	connection,ch = inic_conec(defs.EXCH)
	pacote = prot.inic_pacote()

	prot.escreve_nome(pacote, (dados["id_promo1"])["nome_promo"])
	prot.escreve_id(pacote,(dados["id_promo1"])["promo_id"])
	prot.escreve_voto(pacote, (dados["id_promo1"])["voto"])
	prot.escreve_n_rk(pacote, (dados["id_promo1"])["n_rk"])

	# assinar o pacote e fazer SHA
	prot.escreve_SHA(pacote,gera_assinatura_msg(pacote)) #transformar em string se der BO

	# Defiir pra quem vai mandar 
	envia_msg(ch, pacote, destino, defs.EXCH)


def recebe_pacote(dados, destino): #Microserviço promo.py
	#recebe pacote na fila
	connection,ch = inic_conec(defs.EXCH)
	le_fila(defs.FILA_GATEWAY,defs.EXCH)
	return

def envia_promo(dados):
	envia_pacote(dados, "valida_prom")
	return

def envia_voto(dados):
	envia_pacote(dados, "rk_rank")
	return

def main():
	id = 0
	connection, ch = inic_conec(defs.EXCH)

	escolha_cliente = interface_cliente()
	if (escolha_cliente == 1):
		tags = []
		nome_promo = input("Nome da promoção: ")
		pacote = prot.inic_pacote()
		prot.escreve_nome(pacote, nome_promo)
		n_rk = input("Quantidade de tags: ")
		for i in range(n_rk): 
			tag = input("Quais tags a promoção tem? \n [1] Roupa \n [2] Esporte \n [3] Doméstico \n [4] Comida \n > ")
			prot.escreve_rk_num_n(pacote,tag,i)
		prot.escreve_id(pacote,id)
		id += 1
		prot.escreve_sha(pacote,gera_assinatura_msg(pacote))
		envia_promo(pacote)
		le_fila(defs.FILA_GATEWAY, defs.EXCH_GATEWAY)

	elif (escolha_cliente == 2):
		id = input("ID: ")
		if(id in dict_promo):
			pacote = dict_promo['id']
			prot.escreve_voto(pacote, 's')
			envia_voto(pacote)

	elif (escolha_cliente == 3):
		for pacote in dict_promo["id"]:
			print(f"\n {prot.le_id(pacote)}")
			print(prot.le_nome(pacote))

	connection.close()