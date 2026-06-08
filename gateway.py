#API 

import pika

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import defs
import prot

import base64

from flask import Flask, jsonify, request

app = Flask(__name__)

#estrutura que armazena as promos ja validas
dict_promo = {{

	}}

CHAVE_PRIVADA = "chaves_privadas/priv_gate.der"

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

# bloqueia eternamente pra ficar só consumindo sua fila
def consumir(ch, fila): #Acho que não vai mais ser necessário, porque vai virar a interface web
	ch.basic_consume(queue=fila, auto_ack=True, on_message_callback=callback)
	ch.start_consuming()

# função chamada sempre que um pacote é lido
def callback(ch, method, properties, body):
	global dict_promo
	print("[] pacote recebido")
	pacote = list(chr(b) for b in body)
	#prot.print_pacote(pacote)

	#pega sha do pacote
	SHA = prot.le_sha(pacote)
	#limpa a sha do pacote
	prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))
	#valida se a sha ta correta, se tiver add a promo na lista
	print("[] validando assinatura")
	if valida_assinatura(pacote, SHA,defs.PROM):
		print("[] assinatura valida")
		id = prot.le_id(pacote)
		dict_promo[id] = pacote
		#prot.print_pacote(dict_promo[id])
	else:
		print("[] assinatura invalida")
	print("[] encerrando consumo")
	ch.stop_consuming()

# recebe escolha do cliente
def interface_cliente():
	return int(input(" [1] Adicionar nova promoção \n [2] Votar promoções \n [3] Listar promoções \n [4] Sair\n >"))

# envia um pacote ja finalizado para PROMO
def envia_promo(ch, dados):
	envia_msg(ch, dados, defs.R_KEY_PROMOCAO, defs.EXCH)
	return

# envia um pacote ja finalizado para RANK
def envia_voto(ch, dados):
	envia_msg(ch, dados, defs.R_KEY_RANKING, defs.EXCH)
	return

'''
#Cria promoção e aumenta contador
@app.route("/promocoes", methods=["POST"])
def criar_promocao():
	new_item = request.get_json()
    new_id = len(items) + 1
    new_item["id"] = new_id
    items[new_id] = new_item

    return jsonify(new_item), 201
'''

'''
#Busca todas as promoções, sem categoria
@app.route("/promocoes", methods=["GET"])
def lista_promocoes():
	return jsonify(items), 200
'''

'''
#Busca as promoções por categoria
@app.route('promocoes/<int:item_id>', methods=["GET"])
def lista_promocao_id():
	item = items.get(item_id)

    if item:
        return jsonify(
			"resposta": "Promoção encontrada",
			"item": item
		), 200
    
    return jsonify({"error": "Item not found"}), 404
'''

'''
#Atualiza os campos individuais das promoções
@app.route('/items/<int:item_id>', methods=['PATCH'])
def atualiza_promo(item_id):

    item = items.get(item_id)

    if  not  item:
        return jsonify({"error": "item not found"}), 404

    updated_data = request.get_json()

    for chave, valor in updated_data.items():
        #Consegue votar na promo por aqui
        if chave == "voto":
                item[chave] += valor

        else:
            item[chave] = valor
        
    return jsonify({
        "mensagem": "Promoção alterada com sucesso",
        "retorno": item,
        }),200  
'''

'''
#Permite apagar uma promoção (Se pá nem vamos usar)
@app.route('/promocoes/<int:item_id>', methods=["DELETE"])
def apaga_promocao(item_id):
	item = items.get(item_id)

    if item:
        del item[item_id]
        return jsonify({"message": "Item deleted"}), 200
    else:
        return jsonify({"error": "Item not found"}), 404
'''

def main():
	global dict_promo
	id = 0
	connection, ch = inic_conec(defs.EXCH)
	print("[] conexão iniciada")
	inic_fila(ch, defs.FILA_GATEWAY, defs.EXCH)
	print("[] fila iniciada")
	bind_fila(ch, defs.FILA_GATEWAY, defs.EXCH, defs.R_KEY_VALIDAS)
	escolha_cliente = interface_cliente()
	#loop principal
	while (escolha_cliente != 4):
		# escolha add promo	
		if (escolha_cliente == 1):

			pacote = prot.inic_pacote()

			nome_promo = str(input("Nome da promoção: "))
			prot.escreve_nome(pacote, nome_promo)
			print(f"[] nome adicionado: {prot.le_nome(pacote)}")

			n_rk = int(input("Quantidade de tags: "))
			prot.escreve_n_rk(pacote, n_rk)
			for i in range(n_rk): 
				print(f"Quais tags a promoção tem? \n [1] Comida \n [2] Livro \n [3] Roupa \n [4] Esporte \n [5] Doméstico")
				tag = int(input("> "))
				prot.escreve_rk_num_n(pacote, tag, i + 1)
			print(f"[] {prot.le_n_rk(pacote)} rk adicionada(s): {prot.le_rk_num_n(pacote,1)}, {prot.le_rk_num_n(pacote,2)},{prot.le_rk_num_n(pacote,3)},{prot.le_rk_num_n(pacote,4)}")

			prot.escreve_id(pacote, id)
			id += 1
			print(f"[] id adicionado: {prot.le_id(pacote)}")

			prot.escreve_sha(pacote, gera_assinatura_msg(prot.chars_para_str(pacote)))
			print(f"[] SHA adicionada: {prot.le_sha(pacote)}")

			print("[] pacote completo")
			#prot.print_pacote(pacote)
			
			#envia o pacote montado
			print("[] enviando para promo")
			envia_promo(ch, prot.pacote_para_string(pacote))

			#espera o resposta do pacote
			print("[] iniciando consumo")
			consumir(ch, defs.FILA_GATEWAY)

		# escolha votar promo
		elif (escolha_cliente == 2):
			id = int(input("ID: "))

			pacote = dict_promo[id]
			prot.escreve_voto(pacote, 's')

			#as veiz ele usa ponteiro as veiz ele n quer, ent esse é pra garantir
			prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))

			prot.escreve_sha(pacote, gera_assinatura_msg(prot.chars_para_str(pacote)))
			print(f"[] SHA adicionada: {prot.le_sha(pacote)}")

			envia_voto(ch, prot.pacote_para_string(pacote))

		# escolha listar promocoes
		elif (escolha_cliente == 3):
			
			for i in range(len(dict_promo)):
				pacote = dict_promo[i]
				print(f"{prot.le_id(pacote)}: {prot.le_nome(pacote)}")
		
		elif (escolha_cliente == 4):
			break

		escolha_cliente = interface_cliente()

	connection.close()

if __name__ == '__main__':
	main()