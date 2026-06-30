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
id_at = 1

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
		global itens
		print(itens)
		
		q = queue.Queue(maxsize=50)
		clientes_sse.append(q)
		# Envia estado atual imediatamente ao conectar
		yield f"data: {json.dumps(list(itens.values()))}\n\n"
		while True:
			evento = q.get(timeout=300)
			yield f"data: {json.dumps(evento)}\n\n"
	return Response(gerador(), mimetype="text/event-stream",headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

#********** SSE **********

# bloqueia eternamente pra ficar só consumindo sua fila
def consumir(): #Acho que não vai mais ser necessário, porque vai virar a interface web
	
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
	
	print("[] pacote recebido")
	pacote = list(chr(b) for b in body)
	prot.print_pacote(pacote)

	#pega sha do pacote
	SHA = prot.le_sha(pacote)
	#limpa a sha do pacote
	prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))
	#valida se a sha ta correta, se tiver add a promo na lista
	print("[] validando assinatura")
	
	global itens

	#retorno do promo
	if rbt.valida_assinatura(pacote, SHA,defs.PROM):
		print("[] assinatura valida promo")


		id = prot.le_id(pacote)
		#print("nova promo adicionada em itens:")
		#print(id)
		dic_n = prot.pacote_p_dicio(pacote)
		#print(dic_n)

		# Inicializa campos obrigatórios para o frontend
		if 'votos' not in dic_n:
			dic_n['votos'] = 0
		if 'hot' not in dic_n:
			dic_n['hot'] = False
		if 'categoria' not in dic_n:
			dic_n['categoria'] = 1  # categoria padrão: Comida
		
		itens[id] = dic_n # adicionando o id novo no pacote
		#print(itens[id])

		notificar_cliente(list(itens.values())) # Envia o pacote novo para o SSE atualizar

		print("dicionario recebendo promo")
		print(itens)
	else:
		print("[] assinatura invalida promo")

	#retorno do rank
	if rbt.valida_assinatura(pacote, SHA, defs.RANK):
		print("[] assinatura valida rank")

		id = prot.le_id(pacote)
		n_votos = prot.le_n_votos(pacote)

		if id in itens:
			promo = itens[id]
			promo['votos'] = n_votos

			if n_votos >= 3:
				promo['hot'] = True
			else:
				promo['hot'] = False

			itens[id] = promo

			# Notifica SSE depois de atualizar todos os campos
			print("[] notificando clientes SSE")
			notificar_cliente(list(itens.values()))
		else:
			print(f"[] AVISO: promoção id {id} não encontrada no gateway")
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
	#global itens 
	global id_at
	id_at += 1
	new_id = (id_at) #novo id sequencial
	new_item["id"] = new_id

	pacote = prot.dicio_p_pacote(new_item) # id, nome, preço e email

	sha_loja = new_item['sha']
	categoria = new_item.get('categoria', 1) # categoria vinda do frontend (default: 1 = Comida)
	
	prot.escreve_sha(pacote, sha_loja)
	prot.escreve_id(pacote, new_id)
	prot.escreve_n_rk(pacote, 1) # número de routing keys = 1
	prot.escreve_rk_num_n(pacote, categoria, 1) # escreve a categoria na posição 1
	#prot.escreve_sha(pacote, new_item["sha"]) não assina do gate pq ta com a assinatura da loja

	print(f"[] enviando para promo (categoria: {categoria})")
	prot.print_pacote(pacote)

	envia_promo(prot.pacote_para_string(pacote))
	
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

# Adiciona interesse de um usuário em uma categoria
@app.route('/interesse', methods=['POST'])
def registrar_interesse():
	data = request.get_json()
	email = data.get('email')
	categoria = data.get('categoria')
	
	if not email or not categoria:
		return jsonify({"error": "Email e categoria são obrigatórios"}), 400
	
	print(f"[] Interesse registrado: {email} -> {categoria}")
	return jsonify({"message": "Interesse registrado com sucesso"}), 201

# Cancela interesse de um usuário em uma categoria
@app.route('/interesse', methods=['DELETE'])
def cancelar_interesse():
	data = request.get_json()
	email = data.get('email')
	categoria = data.get('categoria')
	
	if not email or not categoria:
		return jsonify({"error": "Email e categoria são obrigatórios"}), 400
	
	print(f"[] Interesse cancelado: {email} -> {categoria}")
	return jsonify({"message": "Interesse cancelado com sucesso"}), 200

#Atualiza os votos das promoções
@app.route('/items/<int:item_id>', methods=['PATCH'])
def atualiza_voto_promo(item_id): #esse atualiza é SÓ PARA VOTOS
	global itens

	item = itens.get(item_id)

	if item:
		updated_data = request.get_json()

		pacote = prot.dicio_p_pacote(item)
		prot.escreve_id(pacote, item_id)
		
		voto = updated_data.get("voto")
		if voto:
			if voto > 0:
				prot.escreve_voto(pacote, 's') # +1
			elif voto < 0:
				prot.escreve_voto(pacote, 'n') # -1
			
			prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))
			prot.escreve_sha(pacote, rbt.gera_assinatura_msg(prot.chars_para_str(pacote),CHAVE_PRIVADA))
			#print(f"[] SHA adicionada: {prot.le_sha(pacote)}")
			print("[] Eviando para rank")
			prot.print_pacote(pacote)
		
			envia_voto(prot.pacote_para_string(pacote))
		
		return jsonify(item),200 # retorna o item com os votos atualizados.
	
	return jsonify({"error": "item not found"}), 404

def main():
	global itens

	t = threading.Thread(target=consumir, daemon=True)
	t.start()

	app.run(debug=True,threaded=True)

if __name__ == '__main__':
	main()