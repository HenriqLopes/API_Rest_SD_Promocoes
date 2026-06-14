import pika

import defs
import prot

import rbt

#bibliotecas necessárias para envio do e-mail
import os
import resend 

CHAVE_PRIVADA = "chaves_privadas/priv_noti.der"

# bloqueia eternamente pra ficar só consumindo sua fila
def consumir(ch, fila):
	ch.basic_consume(queue=fila, auto_ack=True, on_message_callback=callback)
	ch.start_consuming()
# função chamada sempre que um pacote é lido
def callback(ch, method, properties, pacote):
	pacote = list(chr(b) for b in pacote)
	print("[] pacote recebido")
	#prot.print_pacote(pacote)
	#pega sha do pacote
	SHA = prot.le_sha(pacote)
	#limpa a sha do pacote
	prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))

	print("[] validando assinatura")
	if rbt.valida_assinatura(pacote, SHA,defs.PROM):
		print("[] assinatura valida")
		
		# TODO colocar pra ler o pacote e enviar n email
		prot.le_email(pacote)
		prot.le_nome(pacote)
		prot.le_id(pacote)
		
		#n_keys = prot.le_n_rk(pacote)
		#print(f"[] publicando em {n_keys} tags")
		#envia para todas as chaves da promo
		#for i in range(n_keys): 
			#key = prot.le_rk_num_n(pacote, i + 1)
			#print(f"[] enviando para tag: {defs.R_KEYS[key]}")
			#rbt.envia_msg(ch, prot.pacote_para_string(pacote), defs.R_KEYS[key], defs.EXCH)
	else:
		print("[] assinatura invalida")

def main():
	connection, ch = rbt.inic_conec(defs.EXCH)
	print("[] conexão iniciada")
	rbt.inic_fila(ch, defs.FILA_NOTIFICA, defs.EXCH)
	print("[] fila iniciada")
	#rbt.bind_fila(ch, defs.FILA_NOTIFICA, defs.EXCH, defs.R_KEY_VALIDAS) # n precisa mais se importar com as promos
	rbt.bind_fila(ch, defs.FILA_NOTIFICA, defs.EXCH, defs.R_KEYS[defs.PROM_QUENTES])
	print("[] iniciando consumo")
	consumir(ch, defs.FILA_NOTIFICA)
	connection.close()

if __name__ == '__main__':
	main()
