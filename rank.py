import pika

import defs
import prot
import rbt

dict_promo = {}

CHAVE_PRIVADA = "chaves_privadas/priv_rank.der"

VOTES_HOT_DEAL = 3

# bloqueia eternamente pra ficar só consumindo sua fila
def consumir(ch, fila):
	ch.basic_consume(queue=fila, auto_ack=True, on_message_callback=callback)
	ch.start_consuming()
# função chamada sempre que um pacote é lido
def callback(ch, method, properties, pacote):
	global dict_promo
	
	pacote = list(chr(b) for b in pacote)
	print("[] pacote recebido")
	#prot.print_pacote(pacote)

	#pega sha do pacote
	SHA = prot.le_sha(pacote)
	#limpa a sha do pacote
	prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))

	print("[] validando assinatura")
	#valida se a sha ta correta, se tiver add a promo na lista
	if rbt.valida_assinatura(pacote, SHA, defs.GATE):
		print("[] assinatura valida")
		id = prot.le_id(pacote)

		if id in dict_promo:
			pac, n = dict_promo[id]
			
			voto = prot.le_voto(pacote)
			if voto == 's':
				n += 1
			elif voto == 'n':
				n -= 1
		
			print(f"[] promo de id {id} com {n} votos")
			if n > VOTES_HOT_DEAL:
				prot.escreve_sha(pacote,(rbt.gera_assinatura_msg(prot.chars_para_str(pacote)))) 
				print(f"[] enviando para tag: {defs.R_KEYS[defs.PROM_QUENTES]}")
				#aqui que arruma o bagui do notifica
				rbt.envia_msg(ch, prot.pacote_para_string(pacote), defs.R_KEYS[defs.PROM_QUENTES], defs.EXCH)
			dict_promo[id] = (pac, n)
		else:
			dict_promo[id] = (pacote, 1)
			print(f"[] promo de id {id} com {1} voto")
	else:
		print("[] assinatura invalida")

def main():
	connection, ch = rbt.inic_conec(defs.EXCH)
	print("[] conexão iniciada")
	rbt.inic_fila(ch, defs.FILA_RANKING, defs.EXCH)
	print("[] fila iniciada")
	rbt.bind_fila(ch, defs.FILA_RANKING, defs.EXCH, defs.R_KEY_RANKING)
	print("[] iniciando consumo")
	consumir(ch, defs.FILA_RANKING)
	connection.close()

if __name__ == '__main__':
	main()