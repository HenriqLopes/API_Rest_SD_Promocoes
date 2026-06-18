#API 

import pika

import defs
import prot
import rbt

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Permite requisições de outras portas/domínios

#estrutura que armazena as promos ja validas
# dicionario de dicionarios
dict_promo = {}

ch = None

#para Rest, dicionario de dicionarios facilmente convertido em JSON 
itens = {}

CHAVE_PRIVADA = "chaves_privadas/priv_gate.der"

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
	
	#retorno do promo
	if rbt.valida_assinatura(pacote, SHA,defs.CHAVE_PUBLICA[defs.PROM]):
		print("[] assinatura valida promo")

		id = prot.le_id(pacote)
		dict_promo[id] = pacote # adicionando o id novo no pacote
		#prot.print_pacote(dict_promo[id])
	else:
		print("[] assinatura invalida promo")

	#retorno do rank
	if rbt.valida_assinatura(pacote, SHA, defs.CHAVE_PUBLICA[defs.RANK]):
		print("[] assinatura valida rank")

		id = prot.le_id(pacote)
		n_votos = prot.le_n_votos(pacote)

		promo = dict_promo[id]
		promo['votos'] = n_votos

		if (n_votos > 5): #HOT DEAL
			promo['hot'] = True
		elif (n_votos < 5): 
			promo['hot'] = False

	else:
		print("[] assinatura invalida rank")

	print("[] encerrando consumo")
	ch.stop_consuming()

# envia um pacote ja finalizado para PROMO
def envia_promo(ch, dados):
	rbt.envia_msg(ch, dados, defs.R_KEY_PROMOCAO, defs.EXCH)
	return

# envia um pacote ja finalizado para RANK
def envia_voto(ch, dados):
	rbt.envia_msg(ch, dados, defs.R_KEY_RANKING, defs.EXCH)
	return

def criar_promocao(new_item):

	global itens 
	new_id = (len(itens) + 1) #novo id sequencial
	new_item["id"] = new_id

	#=========================================
	pacote = prot.dicio_p_pacote(new_item) # id, nome, preço e email

	sha_loja = new_item['sha']
	prot.escreve_sha(pacote, sha_loja)
	#prot.escreve_sha(pacote, new_item["sha"]) não assina do gate pq ta com a assinatura da loja

	global ch
	print("[] enviando para promo")
	envia_promo(ch, prot.pacote_para_string(pacote))
	#espera o resposta do pacote
	print("[] iniciando consumo")
	consumir(ch, defs.FILA_GATEWAY) #bloqueia -> vai para callback
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

#Busca as promoções por categoria
@app.route('promocoes/<int:item_id>', methods=["GET"])
def lista_promocao_id(item_id):
	global itens
	
	item = itens.get(item_id)

	if item: #se é um item
		return jsonify(item), 200 #esse item é o dicionario de promo, que é enviado no registro. se pa nem precisa de resposta o 200 já é funcionou po.
    
	return jsonify({"error": "Item not found"}), 404

#Atualiza os campos individuais das promoções
@app.route('/items/<int:item_id>', methods=['PATCH'])
def atualiza_promo(item_id): #esse atualiza é SÓ PARA VOTOS

	global itens

	item = itens.get(item_id)

	if item:
		updated_data = request.get_json()

		pacote = prot.dicio_p_pacote(updated_data)

		voto = updated_data.get("voto")
		if voto:

			global ch

			if voto > 0:
				prot.escreve_voto(pacote, 's') # +1
			elif voto < 0:
				prot.escreve_voto(pacote, 'n') # -1
			
			prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))
			prot.escreve_sha(pacote, rbt.gera_assinatura_msg(prot.chars_para_str(pacote)))
			#print(f"[] SHA adicionada: {prot.le_sha(pacote)}")
			envia_voto(ch, prot.pacote_para_string(pacote))

			#id = updated_data['id']
			#itens[id]["voto"] += voto isso aqui vai ser feito no callback
			consumir(ch, defs.FILA_GATEWAY)
			
		return jsonify(item),200 # retorna o item com os votos atualizados.
	
	return jsonify({"error": "item not found"}), 404

#Rota para definir interesse em categoria
@app.route("/interesse", methods=["POST"])
def registrar_interesse():
	return null

#Apaga interesse em uma categoria
@app.route("/interesse", methods=["DELETE"])
def cancelar_interesse():
	return null

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
	global dict_promo
	global itens

	id = 0
	global ch
	connection, ch = rbt.inic_conec(defs.EXCH)
	print("[] conexão iniciada")
	rbt.inic_fila(ch, defs.FILA_GATEWAY, defs.EXCH)
	print("[] fila iniciada")
	rbt.bind_fila(ch, defs.FILA_GATEWAY, defs.EXCH, defs.R_KEY_VALIDAS)
	rbt.bind_fila(ch, defs.FILA_GATEWAY, defs.EXCH, defs.R_KEYS[defs.PROM_QUENTES]) #hots do GATEWAY

	#TODO tem que starta alguma coisa do rest aqui?
	# some o loop principal pq vai ser tudo por chamada rest.

	connection.close()

if __name__ == '__main__':
	app.run(debug=True)