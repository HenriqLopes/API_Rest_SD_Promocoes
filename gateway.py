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
	if rbt.valida_assinatura(pacote, SHA,defs.PROM):
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
	rbt.envia_msg(ch, dados, defs.R_KEY_PROMOCAO, defs.EXCH)
	return

# envia um pacote ja finalizado para RANK
def envia_voto(ch, dados):
	rbt.envia_msg(ch, dados, defs.R_KEY_RANKING, defs.EXCH)
	return

#TODO pai isso aqui ta adicionando qualquer coisa  que um usuario mandar como promoção, ou seja, paia, já que o MS_PROMO que tinha q validar né 

def criar_promocao():
	new_item = request.get_json() #isso ja converte um JSON pra dict

	pacote = prot.inic_pacote() #esse protocolo vai ser substituido por um JSON.

	prot.escreve_sha(pacote, rbt.gera_assinatura_msg(prot.chars_para_str(pacote)))
	print(f"[] SHA adicionada: {prot.le_sha(pacote)}")
	#envia o pacote montado
	print("[] enviando para promo")
	envia_promo(ch, prot.pacote_para_string(pacote))
	#espera o resposta do pacote
	print("[] iniciando consumo")
	consumir(ch, defs.FILA_GATEWAY)

	#=========================================

	global itens 
	new_id = (len(itens) + 1) #novo id sequencial
	new_item["id"] = new_id
	itens[new_id] = new_item #ja dicionario

	return jsonify(new_item), 201 #isso converte um dict pra um JSON

#Rota para criar uma promoção nova
@app.route("/criar-promocao", methods=["POST"])
def handle_criar_promocao():
    return criar_promocao()

#Busca todas as promoções, sem categoria
@app.route("/promocoes", methods=["GET"])
def lista_promocoes():
	global itens
	return jsonify(itens), 200 #supondo que o email ta como ref de cada promo isso aqui é bem insguro né (ai coitado ele é todo inseguro KSKSKSK perdão).

#Busca as promoções por categoria
@app.route('/promocoes/<int:item_id>', methods=["GET"])
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

		voto = updated_data.get("voto")
		if voto:
			#essa parada aqui tem que ser feita pelo rank tbm n? (RANK TEM QUE CONFIRMAR PRO GATE ATUALIZAR) tudo tem que ter copia atualizada no GATE

			id = int(input("ID: ")) #Isso aqui vai dar ruim, porque vai pedir pelo terminal, não pelo site

			pacote = dict_promo[id]
			prot.escreve_voto(pacote, 's')

			#as veiz ele usa ponteiro as veiz ele n quer, ent esse é pra garantir
			prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))

			prot.escreve_sha(pacote, rbt.gera_assinatura_msg(prot.chars_para_str(pacote)))
			print(f"[] SHA adicionada: {prot.le_sha(pacote)}")

			envia_voto(ch, prot.pacote_para_string(pacote))

			itens[item_id]["voto"] += voto

		return jsonify(item),200  #mesma coisa, acho que n precisa dizer que alterou com sucesso, o 200 ja diz que deu boa n?
	
	return jsonify({"error": "item not found"}), 404

#Rota para definir interesse em categoria
@app.route("/interesse", methods=["POST"])
def registrar_interesse():
    return null

#Apaga interesse em uma categoria
@app.route("/interesse", methods=["DELETE"])
def cancelar_interesse():
	return null

'''#Permite apagar uma promoção (Se pá nem vamos usar)
@app.route('/promocoes/<int:item_id>', methods=["DELETE"])
def apaga_promocao(item_id):

	global itens

	item = itens.get(item_id)

	if item:
		del itens[item_id] #isso funciona em pyto?
		return jsonify({"message": "Item deleted"}), 200
	else:
		return jsonify({"error": "Item not found"}), 404'''

def main():
	global dict_promo
	global itens

	id = 0
	connection, ch = rbt.inic_conec(defs.EXCH)
	print("[] conexão iniciada")
	rbt.inic_fila(ch, defs.FILA_GATEWAY, defs.EXCH)
	print("[] fila iniciada")
	rbt.bind_fila(ch, defs.FILA_GATEWAY, defs.EXCH, defs.R_KEY_VALIDAS)
	escolha_cliente = interface_cliente()

	#TODO tem que starta alguma coisa do rest aqui?
	# some o loop principal pq vai ser tudo por chamada rest.

	connection.close()

if __name__ == '__main__':
	app.run(debug=True)