import pika

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import defs
import prot

#estrutura que armazena as promos ja validas
dict_promo = {}

CHAVE_PRIVADA = "chaves_privadas/priv_gate.der"

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
def callback(ch, method, properties, body):
	global dict_promo
	pacote = list(chr(b) for b in body)
	#pega sha do pacote
	SHA = prot.le_sha(pacote)
	#limpa a sha do pacote
	prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))
	#valida se a sha ta correta, se tiver add a promo na lista
	if valida_assinatura(pacote, SHA,defs.CHAVE_PUBLICA[defs.PROM]):
		dict_promo[prot.le_id(pacote)] = pacote
	ch.stop_consuming()
# recebe escolha do cliente
def interface_cliente():
	return int(input(" [1] Adicionar nova promoção \n [2] Votar promoções \n [3] Listar promoções \n [4] Sair\n >"))

'''def mostra_lista_promo(cliente, promocoes):
	print(f"=== PROMOÇÕES DISPONÍVEIS ===")

	encontrou_promo = False

	for promo in promocoes.values():
		#Tem que colocar aqui direito a parte das categorias do cliente, porque não sei como vai ficar
		if promo['n_rk'] in cliente:
			print(f"  Categoria: {promo['categoria']}")
			print(f"  [{promo['id_promo']}] {promo['promo']}")
			encontrou_promo = True

	if encontrou_promo == False:
		print("  Nenhuma promoção disponível para suas categorias.")'''
'''def define_promo():
	#Promos que serão hardcoded pré execução
	promos = {
		#R_KEY_PROM_LIVRO = 'rk_livr'
		"id_promo1" : {"ini_bits_SHA":0, "tam_bits_SHA":32, "nome_promo":"faz o L", "promo_id":0, "n_rk": 0 , "rk_1":0, "rk_2":0},

		#R_KEY_PROM_ROUPA = 'rk_roup'
		"id_promo2" : {"ini_bits_SHA":0, "tam_bits_SHA":32, "nome_promo":"faz o L", "promo_id":0, "n_rk": 0 , "rk_1":0, "rk_2":0},

		#R_KEY_PROM_ESPORTE = 'rk_espo'
		"id_promo3" : {"ini_bits_SHA":0, "tam_bits_SHA":32, "nome_promo":"faz o L", "promo_id":0, "n_rk": 0 , "rk_1":0, "rk_2":0},

		#R_KEY_PROM_DOMESTICO = 'rk_dome'
		"id_promo4" : {"ini_bits_SHA":0, "tam_bits_SHA":32, "nome_promo":"faz o L", "promo_id":0, "n_rk": 0 , "rk_1":0, "rk_2":0},

		#R_KEY_PROM_COMIDA = 'rk_comi'
		"id_promo5" : {"ini_bits_SHA":0, "tam_bits_SHA":32, "nome_promo":"faz o L", "promo_id":0, "n_rk": 0 , "rk_1":0, "rk_2":0}
	}
	return promos
'''
'''def envia_pacote(pacote, destino):
	# monta o pacote
	connection,ch = inic_conec(defs.EXCH)
	pacote = prot.inic_pacote()

	prot.escreve_nome(pacote, (pacote["id_promo1"])["nome_promo"])
	prot.escreve_id(pacote,(pacote["id_promo1"])["promo_id"])
	prot.escreve_voto(pacote, (pacote["id_promo1"])["voto"])
	prot.escreve_n_rk(pacote, (pacote["id_promo1"])["n_rk"])

	# assinar o pacote e fazer SHA
	prot.escreve_SHA(pacote,gera_assinatura_msg(pacote)) #transformar em string se der BO

	# Defiir pra quem vai mandar 
	envia_msg(ch, pacote, destino, defs.EXCH)


def recebe_pacote(dados, destino): #Microserviço promo.py
	#recebe pacote na fila
	connection,ch = inic_conec(defs.EXCH)
	le_fila(defs.FILA_GATEWAY,defs.EXCH)
	return'''

# envia um pacote ja finalizado para PROMO
def envia_promo(ch, dados):
	envia_msg(ch, dados, defs.R_KEY_PROMOCAO, defs.EXCH)
	return
# envia um pacote ja finalizado para RANK
def envia_voto(ch, dados):
	envia_msg(ch, dados, defs.R_KEY_RANKING, defs.EXCH)
	return

def main():
	id = 0
	connection, ch = inic_conec(defs.EXCH)
	inic_fila(ch, defs.FILA_GATEWAY, defs.EXCH)
	bind_fila(ch, defs.FILA_GATEWAY, defs.EXCH, defs.R_KEY_VALIDAS)
	escolha_cliente = interface_cliente()
	#loop principal
	while (escolha_cliente != 4):
		# escolha add promo
		if (escolha_cliente == 1):

			pacote = prot.inic_pacote()

			nome_promo = str(input("Nome da promoção: "))
			prot.escreve_nome(pacote, nome_promo)

			n_rk = int(input("Quantidade de tags: "))
			for i in range(n_rk): 
				print(f"Quais tags a promoção tem? \n [{defs.PROM_ROUPA}] Roupa \n [{defs.PROM_ESPORTE}] Esporte \n [{defs.PROM_DOMESTICO}] Doméstico \n [{defs.PROM_COMIDA}] Comida \n [{defs.PROM_LIVRO}] Livro")
				tag = int(input("> "))
				prot.escreve_rk_num_n(pacote, tag, i)

			prot.escreve_id(pacote, id)
			id += 1

			prot.escreve_sha(pacote, gera_assinatura_msg(prot.chars_para_str(pacote)))

			#envia o pacote montado
			envia_promo(ch, prot.pacote_para_string(pacote))

			#espera o resposta do pacote
			consumir(ch, defs.FILA_GATEWAY)

		# escolha votar promo
		elif (escolha_cliente == 2):
			id = input("ID: ")
			if(id in dict_promo):
				pacote = dict_promo[id]
				prot.escreve_voto(pacote, 's')
				envia_voto(ch, pacote)

		# escolha listar promocoes
		elif (escolha_cliente == 3):
			for pacote in dict_promo:
				print(f"{prot.le_id(pacote)}: {prot.le_nome(pacote)}")
		
		elif (escolha_cliente == 4):
			break

		escolha_cliente = interface_cliente()

	connection.close()

if __name__ == '__main__':
	main()