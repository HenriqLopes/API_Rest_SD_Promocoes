import pika

import defs
import prot
import rbt

CHAVE_PRIVADA = "chaves_privadas/priv_prom.der"

# bloqueia eternamente pra ficar só consumindo sua fila
def consumir(ch, fila):
	ch.basic_consume(queue=fila, auto_ack=True, on_message_callback=callback)
	ch.start_consuming()

# função chamada sempre que um pacote é lido
def callback(ch, method, properties, pacote):
	pacote = list(chr(b) for b in pacote)
	print("[] pacote recebido")
	#prot.print_pacote(pacote)

	nome = prot.le_nome(pacote)
	preco = prot.le_preco(pacote)
	email = prot.le_email(pacote)
	chave = None
	if (email == 'gustavobuenodacosta@gmail.com'):
		chave = 'tools/publ_loj1.der'
	else:
		chave = 'tools/publ_loj2.der'	

	promo = {
		"nome": nome,
		"email": email,
		"preco": preco
	}

	assinatura = prot.le_sha(pacote)

	print(len(prot.le_sha(pacote)))

	print("********************")
	print(assinatura)
	print("********************")

	if (rbt.valida_assinatura_loja(str(promo), assinatura, chave)):
		print("[] assinatura valida")
		
		#limpa a sha do pacote
		prot.escreve_sha(pacote,("0" * prot.TAM_BYT_SHA))
		
		prot.escreve_sha(pacote,rbt.gera_assinatura_msg(prot.pacote_para_string(pacote))) 
		print("[] postando promo como validada")
		rbt.envia_msg(ch, prot.pacote_para_string(pacote),defs.R_KEY_VALIDAS,defs.EXCH)
	else:
		print("[] assinatura invalida")

def main():
	connection, ch = rbt.inic_conec(defs.EXCH)
	print("[] conexão iniciada")
	rbt.inic_fila(ch, defs.FILA_PROMOCAO, defs.EXCH)
	print("[] fila iniciada iniciada")
	rbt.bind_fila(ch, defs.FILA_PROMOCAO, defs.EXCH, defs.R_KEY_PROMOCAO)
	print("[] iniciando consumo")
	consumir(ch, defs.FILA_PROMOCAO)
	connection.close()

if __name__ == '__main__':
	main()
