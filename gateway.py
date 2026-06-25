#API 

import pika

import defs
import prot
import rbt

from flask import Flask, jsonify, request, Response
import json, time, queue
from flask_cors import CORS

import threading

app = Flask(__name__)
CORS(app) # Permite requisições de outras portas/domínios

#estrutura que armazena as promos ja validas
# dicionario de dicionarios

ch = None

#para Rest, dicionario de dicionarios facilmente convertido em JSON 
itens = {}

CHAVE_PRIVADA = "chaves_privadas/priv_gate.der"

#********* SSE ********
# cada conexão SSE recebe sua própria fila
clientes_sse: list[queue.Queue] = []

def notificar_cliente(evento: dict):
	#Envia um evento para todas as conexões SSE abertas.
	for q in clientes_sse:
		q.put_nowait(evento)

@app.route("/stream")
def stream():
	def gerador():
		q = queue.Queue(maxsize=50)
		clientes_sse.append(q)
		# Envia estado atual imediatamente ao conectar
		yield f"data: {json.dumps(list(itens.values()))}\n\n"
		while True:
			evento = q.get(timeout=20)
			yield f"data: {json.dumps(evento)}\n\n"
	return Response(gerador(), mimetype="text/event-stream",headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

#********** SSE **********

# bloqueia eternamente pra ficar só consumindo sua fila
def consumir(): #Acho que não vai mais ser necessário, porque vai virar a interface web

	global ch	
	connection, ch = rbt.inic_conec(defs.EXCH)
	print("[] conexão iniciada")
	rbt.inic_fila(ch, defs.FILA_GATEWAY, defs.EXCH)
	print("[] fila iniciada")
	rbt.bind_fila(ch, defs.FILA_GATEWAY, defs.EXCH, defs.R_KEY_VALIDAS)
	rbt.bind_fila(ch, defs.FILA_GATEWAY, defs.EXCH, defs.R_KEYS[defs.PROM_QUENTES]) #hots do GATEWAY

	ch.basic_consume(queue=defs.FILA_GATEWAY, auto_ack=True, on_message_callback=callback)
	print("[] iniciando consumo")
	ch.start_consuming()

# função chamada sempre que um pacote é lido
def callback(ch, method, properties, body):
	global itens
	
	print("[] pacote recebido")
	pacote = list(chr(b) for b in body)
	#prot.print_pacote(pacote)

	#pega sha do pacote
	SHA = prot.le_sha(pacote)
	#limpa a sha do pacote
	prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))
	#valida se a sha ta correta, se tiver add a promo na lista
	print("[] validando assinatura")
	
	#retorno do promo
	if rbt.valida_assinatura(pacote, SHA,defs.PROM):
		print("[] assinatura valida promo")

		id = prot.le_id(pacote)
		itens[id] = prot.pacote_p_dicio(pacote) # adicionando o id novo no pacote
		
		#TODO acho que isso aqui n funciona.
		notificar_cliente(list(itens.values())) # Envia o pacote novo para o SSE atualizar

		#prot.print_pacote(itens[id])
	else:
		print("[] assinatura invalida promo")

	#retorno do rank
	if rbt.valida_assinatura(pacote, SHA, defs.RANK):
		print("[] assinatura valida rank")

		id = prot.le_id(pacote)
		n_votos = prot.le_n_votos(pacote)

		promo = itens[id]
		promo['votos'] = n_votos

		#notificar_cliente(list(itens.values()))

		if (n_votos > 5): #HOT DEAL
			promo['hot'] = True
		elif (n_votos < 5): 
			promo['hot'] = False

	else:
		print("[] assinatura invalida rank")

# envia um pacote ja finalizado para PROMO
def envia_promo(dados):

	connection, ch = rbt.inic_conec(defs.EXCH)
	rbt.envia_msg(ch, dados, defs.R_KEY_PROMOCAO, defs.EXCH)
	connection.close()

	return

# envia um pacote ja finalizado para RANK
def envia_voto(dados):

	connection, ch = rbt.inic_conec(defs.EXCH)
	rbt.envia_msg(ch, dados, defs.R_KEY_RANKING, defs.EXCH)
	connection.close()

	return

def criar_promocao(new_item):

	global itens 
	new_id = (len(itens) + 1) #novo id sequencial
	new_item["id"] = new_id

	#=========================================
	pacote = prot.dicio_p_pacote(new_item) # id, nome, preço e email

	sha_loja = new_item['sha']
	prot.escreve_sha(pacote, sha_loja)
	prot.escreve_id(pacote, new_id)
	prot.escreve_n_rk(pacote, 1)
	prot.escreve_rk_num_n(pacote, new_item["categoria"], 1)
	#prot.escreve_sha(pacote, new_item["sha"]) não assina do gate pq ta com a assinatura da loja

	print("[] enviando para promo")
	prot.print_pacote(pacote)

	envia_promo(prot.pacote_para_string(pacote))
	#=========================================
	
	#itens[new_id] = new_item #ja dicionario isso vai acontecer no callback agora?

	return jsonify(new_item), 201 #isso converte um dict pra um JSON

#Rota para criar uma promoção nova
@app.route("/criar-promocao", methods=["POST"])
def handle_criar_promocao():

	new_item = request.get_json() #isso ja converte um JSON pra dict
	return criar_promocao(new_item)

#Busca todas as promoções, sem categoria
@app.route("/promocoes", methods=["GET"])
def lista_promocoes():
	global itens
	return jsonify(itens), 200 #supondo que o email ta como ref de cada promo isso aqui é bem insguro né (ai coitado ele é todo inseguro KSKSKSK perdão).

# Busca todas as promoções das categorias informadas
@app.route("/promocoes/<string:categorias>", methods=["GET"])
def lista_promocoes_categ(categorias):
	ids_categ = [int(x) for x in categorias.split(",")]

	itens_ret = []

	global itens

	for i in itens.values():
		if i["categoria"] in ids_categ:
			itens_ret.append(i)

	return jsonify(itens_ret), 200

#Busca as promoções por categoria
@app.route('/promocoes/<int:item_id>', methods=["GET"])
def lista_promocao_id(item_id):
	global itens
	
	item = itens.get(item_id)

	if item: #se é um item
		return jsonify(item), 200 #esse item é o dicionario de promo, que é enviado no registro. se pa nem precisa de resposta o 200 já é funcionou po.
    
	return jsonify({"error": "Item not found"}), 404

#Atualiza os campos individugit
@app.route('/items/<int:item_id>', methods=['PATCH'])
def atualiza_promo(item_id): #esse atualiza é SÓ PARA VOTOS

	global itens

	item = itens.get(item_id)

	if item:
		updated_data = request.get_json()

		pacote = prot.dicio_p_pacote(updated_data)
		print("Passei dicio pacote")

		voto = updated_data.get("voto")
		if voto:

			if voto > 0:
				prot.escreve_voto(pacote, 's') # +1
			elif voto < 0:
				prot.escreve_voto(pacote, 'n') # -1
			
			prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))
			prot.escreve_sha(pacote, rbt.gera_assinatura_msg(prot.chars_para_str(pacote)))
			#print(f"[] SHA adicionada: {prot.le_sha(pacote)}")
			envia_voto(prot.pacote_para_string(pacote))

			#id = updated_data['id']
			#itens[id]["voto"] += voto isso aqui vai ser feito no callback
			
		return jsonify(item),200 # retorna o item com os votos atualizados.
	
	return jsonify({"error": "item not found"}), 404

#Dicionário global relacionando {email[interesses]}
'''interesses = {}

@app.route("/interesse", methods=["POST"])
def registrar_interesse():
	updated_interest = request.get_json()

	email = updated_interest.get("email")
	categoria = updated_interest.get("categoria")

	if not email or categoria is None:
		return jsonify({"error" : "email e categoria são obrigatórios"}), 400
	
	if email not in interesses:
		interesses[email] = []
	
	#Relaciona uma categoria ao email do usuário TODO chefia o usuario n bota email não. é só interesse.
	if categoria not in interesses[email]:
		interesses[email].append(categoria)

	return jsonify({"email" : email, "categorias": interesses[email]}), 201

#Apaga interesse em uma categoria
@app.route("/interesse", methods=["DELETE"])
def cancelar_interesse():

	updated_interest = request.get_json()

	email = updated_interest.get("email")
	categoria = updated_interest.get("categoria")

	if not email or categoria is None:
		return jsonify({"error" : "email e categoria são obrigatórios"}), 400
	
	if email not in interesses or categoria not in interesses[email]:
		interesses[email] = []
		return jsonify({"error": "interesse não encontrado"}), 404

	interesses[email].remove(categoria)
	
	return jsonify({"email" : email, "categorias": interesses[email]}), 200'''

#Permite apagar uma promoção (Se pá nem vamos usar)
@app.route('/promocoes/<int:item_id>', methods=["DELETE"])
def apaga_promocao(item_id):

	global itens

	item = itens.get(item_id)

	if item:
		del item[item_id] #isso funciona em pyto?
		return jsonify({"message": "Item deleted"}), 200
	else:
		return jsonify({"error": "Item not found"}), 404

def main():
	global itens

	t = threading.Thread(target=consumir, daemon=True)
	t.start()

	app.run(debug=True)

if __name__ == '__main__':
	main()