INI_BYT_SHA = 0
TAM_BYT_SHA = 344
INI_BYT_NOM = INI_BYT_SHA + TAM_BYT_SHA
TAM_BYT_NOM = 23
INI_BYT_IDS = INI_BYT_NOM + TAM_BYT_NOM
TAM_BYT_IDS = 4
INI_BYT_VOT = INI_BYT_IDS + TAM_BYT_IDS
TAM_BYT_VOT = 1
INI_BYT_NRK = INI_BYT_VOT + TAM_BYT_VOT
TAM_BYT_NRK = 4
INI_BYT_RKN = INI_BYT_NRK + TAM_BYT_NRK
TAM_BYT_RKN = 4

def inic_pacote():
	return list(
		("0" * TAM_BYT_SHA) +
		("a" * TAM_BYT_NOM) +
		("0" * TAM_BYT_IDS) +
		("n") +
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
	return list(valor.ljust(tam)[:tam])
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
	return chars_para_str(msg[INI_BYT_NOM : (INI_BYT_NOM + TAM_BYT_NOM)])

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
	print(f"{le_id(msg)}: {le_nome(msg)} {le_voto(msg)}")
	print(le_sha(msg))
	print(f"{le_n_rk(msg)}: {le_rk_num_n(msg, 1)}, {le_rk_num_n(msg, 2)}, {le_rk_num_n(msg, 3)}, {le_rk_num_n(msg, 4)}")