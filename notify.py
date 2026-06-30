import pika

import defs
import prot

import rbt

# Bibliotecas nativas do Python para envio de e-mail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

CHAVE_PRIVADA = "chaves_privadas/priv_noti.der"

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

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
	# Hot deals vem do MS Ranking
	if rbt.valida_assinatura(pacote, SHA, defs.RANK):
		print("[] assinatura valida - hot deal")

		envia_email(pacote)

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
	rbt.bind_fila(ch, defs.FILA_NOTIFICA, defs.EXCH, defs.R_KEYS[defs.PROM_QUENTES])
	print("[] iniciando consumo")
	consumir(ch, defs.FILA_NOTIFICA)
	connection.close()

# Envia e-mail avisando que a promoção é uma hotdeal
def envia_email(pacote):
	id_promo = prot.le_id(pacote)
	email_loja = prot.le_email(pacote).strip()
	nome_promo = prot.le_nome(pacote)
	
	print(f"[] Enviando e-mail para {email_loja} sobre promoção #{id_promo}: {nome_promo}")
	
	# Configurações do remetente (Gmail SMTP)
	remetente = os.getenv("EMAIL_REMETENTE")
	senha = os.getenv("EMAIL_SENHA")
	
	# Cria a mensagem
	msg = MIMEMultipart()
	msg['From'] = remetente
	msg['To'] = email_loja
	msg['Subject'] = f"Promoção #{id_promo}: {nome_promo} virou HOT DEAL!"
	
	corpo = f"""
	<html>
		<body>
			<p>Sua promoção <strong>#{id_promo} - {nome_promo}</strong> virou um <strong>HOT-DEAL</strong>!</p>
		</body>
	</html>
	"""
	
	msg.attach(MIMEText(corpo, 'html'))
	
	# Envia via SMTP do Gmail
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(remetente, senha)
	server.send_message(msg)
	server.quit()
	
	print(f"[] E-mail enviado com sucesso!")

if __name__ == '__main__':
	main()
