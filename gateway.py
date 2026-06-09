#API 

import pika

import defs
import prot
import rbt

from flask import Flask, jsonify, request

app = Flask(__name__)

#estrutura que armazena as promos ja validas
<<<<<<< HEAD
dict_promo = {{

	}}
=======
# dicionario de dicionarios
dict_promo = {}
>>>>>>> f7890056d7cf3a5d0c365b4a0674334836fd3486

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

<<<<<<< HEAD
'''
=======

#TODO pai isso aqui ta adicionando qualquer coisa  que um usuario mandar como promoção, ou seja, paia, já que o MS_PROMO que tinha q validar né 

>>>>>>> f7890056d7cf3a5d0c365b4a0674334836fd3486
#Cria promoção e aumenta contador
@app.route("/promocoes", methods=["POST"])
def criar_promocao():
	new_item = request.get_json() #isso ja converte um JSON pra dict

	#aqui entra a validação da Promo. (QUEM VALIDA? o GATE, ou o PROMO, pq agora a gente quer saber se foi a loja que assinou sabe)
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

		voto = updated_data.get("voto")
		if voto:
			#essa parada aqui tem que ser feita pelo rank tbm n? (RANK TEM QUE CONFIRMAR PRO GATE ATUALIZAR) tudo tem que ter copia atualizada no GATE

<<<<<<< HEAD
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
=======
>>>>>>> f7890056d7cf3a5d0c365b4a0674334836fd3486
			id = int(input("ID: "))

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