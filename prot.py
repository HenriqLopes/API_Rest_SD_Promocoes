import struct

INI_BYT_SHA = 0
TAM_BYT_SHA = 344
INI_BYT_NOM = INI_BYT_SHA + TAM_BYT_SHA
TAM_BYT_NOM = 100
INI_BYT_IDS = INI_BYT_NOM + TAM_BYT_NOM
TAM_BYT_IDS = 4
INI_BYT_NVT = INI_BYT_IDS + TAM_BYT_IDS
TAM_BYT_NVT = 4
INI_BYT_VOT = INI_BYT_NVT + TAM_BYT_NVT
TAM_BYT_VOT = 1
INI_BYT_EML = INI_BYT_VOT + TAM_BYT_VOT
TAM_BYT_EML = 29 #29 caracteres todo email 
INI_BYT_PRE = INI_BYT_EML + TAM_BYT_EML
TAM_BYT_PRE = 4 #1 double
INI_BYT_NRK = INI_BYT_PRE + TAM_BYT_PRE
TAM_BYT_NRK = 4
INI_BYT_RKN = INI_BYT_NRK + TAM_BYT_NRK
TAM_BYT_RKN = 4

def inic_pacote():
	return list(
		("0" * TAM_BYT_SHA) +
		("0" * TAM_BYT_NOM) +
		("0" * TAM_BYT_IDS) +
		("0" * TAM_BYT_NVT) +
		("z") +
		("a" * TAM_BYT_EML) +
		("0" * TAM_BYT_PRE) +
		("0" * TAM_BYT_NRK) +
		("0" * TAM_BYT_RKN) +
		("0" * TAM_BYT_RKN) +
		("0" * TAM_BYT_RKN) +
		("0" * TAM_BYT_RKN) )

def int_para_chars(valor, tam):
	return list(str(valor).zfill(tam)[:tam])
def chars_para_int(chars):
	return int(''.join(chars) or '0')
def str_para_chars(valor, tam):
	return list(valor.ljust(tam, '\0')[:tam])
def chars_para_str(chars):
	resultado = ""
	for c in chars:
		resultado += str(c)
	return str(resultado)
def pacote_para_string(pacote):
	resultado = ""
	for c in pacote:
		resultado += str(c)
	return str(resultado)

def escreve_sha(msg, SHA):
	msg[INI_BYT_SHA : (INI_BYT_SHA + TAM_BYT_SHA)] = str_para_chars(SHA, TAM_BYT_SHA)
def le_sha(msg):
	return chars_para_str(msg[INI_BYT_SHA : (INI_BYT_SHA + TAM_BYT_SHA)])

def escreve_nome(msg, nome):
	msg[INI_BYT_NOM : (INI_BYT_NOM + TAM_BYT_NOM)] = str_para_chars(nome, TAM_BYT_NOM)
def le_nome(msg):
	ret = chars_para_str(msg[INI_BYT_NOM : (INI_BYT_NOM + TAM_BYT_NOM)])
	return ret.split('\x00', 1)[0]

def escreve_email(msg, email):
	msg[INI_BYT_EML : (INI_BYT_EML + TAM_BYT_EML)] = str_para_chars(email, TAM_BYT_EML)
def le_email(msg):
	ret = chars_para_str(msg[INI_BYT_EML : (INI_BYT_EML + TAM_BYT_EML)])
	return ret.split('\x00', 1)[0]

def escreve_id(msg, id):
	msg[INI_BYT_IDS : (INI_BYT_IDS + TAM_BYT_IDS)] = int_para_chars(id, TAM_BYT_IDS)
def le_id(msg):
	return chars_para_int(msg[INI_BYT_IDS : (INI_BYT_IDS + TAM_BYT_IDS)])

def escreve_voto(msg, voto):
	msg[INI_BYT_VOT : (INI_BYT_VOT + TAM_BYT_VOT)] = str_para_chars(voto, TAM_BYT_VOT)
def le_voto(msg):
	return chars_para_str(msg[INI_BYT_VOT : (INI_BYT_VOT + TAM_BYT_VOT)])

def escreve_n_rk(msg, n_rk):
	msg[INI_BYT_NRK : (INI_BYT_NRK + TAM_BYT_NRK)] = int_para_chars(n_rk, TAM_BYT_NRK)
def le_n_rk(msg):
	return chars_para_int(msg[INI_BYT_NRK : (INI_BYT_NRK + TAM_BYT_NRK)])

def escreve_rk_num_n(msg, rk, n):
	msg[INI_BYT_RKN + (TAM_BYT_RKN * (n - 1)) : (INI_BYT_RKN + (TAM_BYT_RKN * n))] = int_para_chars(rk, TAM_BYT_RKN)
def le_rk_num_n(msg, n):
	return chars_para_int(msg[INI_BYT_RKN +  (TAM_BYT_RKN * (n - 1)) : (INI_BYT_RKN + (TAM_BYT_RKN * n))])

def print_pacote(msg):
	print(f"{le_id(msg)}: {le_nome(msg)}, ({le_preco(msg)} R$) com {le_n_votos(msg)} de {le_email(msg)}")
	#print(le_sha(msg))
	print(f"{le_n_rk(msg)}: {le_rk_num_n(msg, 1)}, {le_rk_num_n(msg, 2)}, {le_rk_num_n(msg, 3)}, {le_rk_num_n(msg, 4)}")

def escreve_preco(msg, preco):
	msg[INI_BYT_PRE : INI_BYT_PRE + TAM_BYT_PRE] = int_para_chars(preco, TAM_BYT_PRE)
def le_preco(msg):
	return chars_para_int(msg[INI_BYT_PRE : (INI_BYT_PRE + TAM_BYT_PRE)])

def escreve_n_votos(msg, n_votos):
	msg[INI_BYT_NVT : (INI_BYT_NVT + TAM_BYT_NVT)] = int_para_chars(id, TAM_BYT_NVT)
def le_n_votos(msg):
	return chars_para_int(msg[INI_BYT_NVT : (INI_BYT_NVT + TAM_BYT_NVT)])


def dicio_p_pacote(dicio):
	
	pacote = inic_pacote()

	nome = dicio.get('nome')
	if nome is not None:
		escreve_nome(pacote, nome)

	# ...

	preco = dicio.get('preco')
	if preco is not None:
		escreve_preco(pacote, preco)

	email = dicio.get('email')
	if email is not None:
		escreve_email(pacote, email)

	id = dicio.get('id')
	if id is not None:
		escreve_id(pacote, id)

	return pacote
def pacote_p_dicio(pacote):

	dicio = {}

	nome =  le_nome(pacote)
	dicio['nome'] = nome

	preco =  le_preco(pacote)
	dicio['preco'] = preco

	email =  le_email(pacote)
	dicio['email'] = email

	categoria =  le_rk_num_n(pacote, 1)
	dicio['categoria'] = categoria

	votos =  le_n_votos(pacote)
	dicio['votos'] = votos

	return dicio

