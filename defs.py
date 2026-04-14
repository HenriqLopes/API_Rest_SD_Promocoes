EXCH = 'exc'

#filas e keys especificas
R_KEY_GATEWAY = 'rk_gate'
FILA_GATEWAY = 'fl_gate'

R_KEY_NOTIFICA = 'rk_noti'
FILA_NOTIFICA = 'fl_noti'

R_KEY_RANKING = 'rk_rank'
FILA_RANKING = 'fl_rank'

R_KEY_PROMOCAO = 'rk_prom'
FILA_PROMOCAO = 'fl_prom'

#key de promos validadas já
R_KEY_VALIDAS = 'rk_vali'

#definicoes do dicionario de tags
PROM_LIVRO = 2
PROM_ROUPA = 3
PROM_ESPORTE = 4
PROM_DOMESTICO = 5
PROM_COMIDA = 1
PROM_QUENTES = 6

R_KEYS = {
	PROM_LIVRO: 'rk_livr',
	PROM_ROUPA: 'rk_roup',
	PROM_ESPORTE: 'rk_espo',
	PROM_DOMESTICO: 'rk_dome',
	PROM_COMIDA: 'rk_comi',
	PROM_QUENTES: 'rk_quen'
}

#definicoes do dicionario de chaves publicas

GATE = 1
RANK = 2
PROM = 3
NOTI = 4

CHAVE_PUBLICA = {
	GATE: 'chaves_publicas/pub_gate.der',
	RANK: 'chaves_publicas/pub_rank.der',
	PROM: 'chaves_publicas/pub_prom.der',
	NOTI: 'chaves_publicas/pub_noti.der',
}
