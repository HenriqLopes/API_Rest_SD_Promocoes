import requests
import time
import random

import rbt


nomes = ['Garrafa de água', 'Caneta', 'Lápis', 'Borracha', 'Caderno', 'Mochila', 'Agenda', 'Livro', 'Revista', 'Jornal', 'Calculadora', 'Régua', 'Tesoura', 'Cola', 'Estojo', 'Marcador de texto', 'Papel sulfite', 'Pasta organizadora', 'Post-it', 'Grampeador', 'Smartphone', 'Notebook', 'Tablet', 'Monitor', 'Teclado', 'Mouse', 'Webcam', 'Impressora', 'Fone de ouvido', 'Caixa de som', 'Carregador portátil', 'Pendrive', 'HD externo', 'SSD', 'Roteador Wi-Fi', 'Cabo USB', 'Adaptador HDMI', 'Smartwatch', 'Controle de videogame', 'Videogame', 'Camiseta', 'Calça jeans', 'Bermuda', 'Jaqueta', 'Casaco', 'Moletom', 'Vestido', 'Saia', 'Camisa social', 'Terno', 'Gravata', 'Meias', 'Cueca', 'Sutiã', 'Pijama', 'Chinelo', 'Tênis', 'Sapato social', 'Bota', 'Sandália', 'Boné', 'Chapéu', 'Cachecol', 'Luvas', 'Cinto', 'Escova de dentes', 'Creme dental', 'Fio dental', 'Enxaguante bucal', 'Shampoo', 'Condicionador', 'Sabonete', 'Desodorante', 'Perfume', 'Protetor solar', 'Hidratante corporal', 'Escova de cabelo', 'Secador de cabelo', 'Aparelho de barbear', 'Toalha de banho', 'Sofá', 'Mesa de jantar', 'Cadeira', 'Poltrona', 'Estante', 'Guarda-roupa', 'Cômoda', 'Escrivaninha', 'Cama', 'Colchão', 'Travesseiro', 'Lençol', 'Cobertor', 'Edredom', 'Cortina', 'Tapete', 'Luminária', 'Espelho', 'Cabide', 'Sapateira', 'Geladeira', 'Fogão', 'Micro-ondas', 'Forno elétrico', 'Liquidificador', 'Batedeira', 'Cafeteira', 'Torradeira', 'Air fryer', 'Panela de pressão', 'Frigideira', 'Conjunto de panelas', 'Prato', 'Copo', 'Xícara', 'Talheres', 'Faca de cozinha', 'Tábua de corte', 'Pote hermético', 'Garrafa térmica', 'Arroz', 'Feijão', 'Macarrão', 'Farinha de trigo', 'Açúcar', 'Sal', 'Café', 'Chá', 'Leite', 'Queijo', 'Iogurte', 'Manteiga', 'Ovos', 'Pão', 'Biscoito', 'Chocolate', 'Sorvete', 'Refrigerante', 'Suco', 'Água mineral', 'Bicicleta', 'Capacete', 'Patins', 'Skate', 'Bola de futebol', 'Bola de basquete', 'Raquete de tênis', 'Corda de pular', 'Colchonete', 'Halteres', 'Elástico de resistência', 'Luva de boxe', 'Rede de vôlei', 'Óculos de natação', 'Prancha de surf', 'Barraca de camping', 'Saco de dormir', 'Lanterna', 'Mochila de trilha', 'Cantil', 'Mala de viagem', 'Trava de bicicleta', 'Guarda-chuva', 'Capa de chuva', 'Binóculo', 'Relógio', 'Pulseira', 'Colar', 'Anel', 'Brincos', 'Óculos de sol', 'Bolsa', 'Carteira', 'Mala executiva', 'Necessaire', 'Mala de bordo', 'Broche', 'Pingente', 'Presilha de cabelo', 'Faixa de cabelo', 'Tinta para parede', 'Pincel de pintura', 'Rolo de pintura', 'Furadeira', 'Martelo', 'Chave de fenda', 'Alicate', 'Trena', 'Parafusos', 'Pregos', 'Fita isolante', 'Extensão elétrica', 'Lâmpada LED', 'Tomada inteligente', 'Fechadura eletrônica', 'Detector de fumaça', 'Aspirador de pó', 'Vassoura', 'Rodo', 'Balde', 'Sabão em pó', 'Amaciante', 'Detergente', 'Desinfetante', 'Esponja de limpeza', 'Pano de chão', 'Papel higiênico', 'Papel toalha', 'Sacos de lixo', 'Organizador de gaveta', 'Quadro decorativo', 'Vaso de planta', 'Planta ornamental', 'Almofada', 'Vela aromática', 'Difusor de aromas', 'Porta-retratos', 'Relógio de parede', 'Escultura decorativa', 'Adesivo de parede', 'Violão', 'Guitarra', 'Teclado musical', 'Bateria eletrônica', 'Microfone', 'Suporte para microfone', 'Estante para partituras', 'Ukulele', 'Harmônica', 'Pandeiro', 'Filme em Blu-ray', 'Jogo de tabuleiro', 'Quebra-cabeça', 'Baralho', 'Livro de colorir', 'Álbum de fotos', 'Drone', 'Câmera fotográfica', 'Filmadora', 'Tripé', 'Cartão de memória', 'Impressora 3D', 'Filamento para impressora 3D', 'Action figure', 'Pelúcia', 'Boneca', 'Carrinho de brinquedo', 'Blocos de montar', 'Trenzinho elétrico', 'Patinete', 'Berço', 'Cadeirinha infantil para carro', 'Mamadeira', 'Chupeta', 'Fraldas', 'Babador', 'Carrinho de bebê', 'Banheira infantil', 'Tapete de atividades para bebê', 'Brinquedo educativo', 'Ração para cachorro', 'Ração para gato', 'Coleira', 'Guia para passeio', 'Caminha para pet', 'Arranhador para gatos', 'Caixa de transporte para pet', 'Brinquedo para cachorro', 'Aquário', 'Comedouro para pet', 'Sementes para jardim', 'Adubo', 'Mangueira de jardim', 'Pá de jardinagem', 'Tesoura de poda', 'Regador', 'Vaso grande', 'Terra vegetal', 'Grama em placas', 'Composteira', 'Carro', 'Moto', 'Capacete para moto', 'Capa para carro', 'Tapete automotivo', 'GPS automotivo', 'Suporte para celular veicular', 'Compressor de ar portátil', 'Cera automotiva', 'Limpador de para-brisa', 'Seguro residencial', 'Seguro automotivo', 'Curso online', 'Assinatura de streaming', 'Ingresso para cinema', 'Ingresso para show', 'Passagem aérea', 'Hospedagem em hotel', 'Vale-presente', 'Assinatura de academia']
PRECO_MIN = 0.00
PRECO_MAX = 10000000.00
emails = ['gustavobuenodacosta@gmail.com', 'buenogustavodacosta@gmail.com']

while True:

	time.sleep(5) #registra uma promo aleatória a cada 5 seg

	nome = random.choice(nomes)
	preco = random.uniform(PRECO_MIN, PRECO_MAX)
	email = random.choice(emails)
	chave = None
	if (email == 'gustavobuenodacosta@gmail.com'):
		chave = 'tools/priv_loj1.der'
	else:
		chave = 'tools/priv_loj2.der'	

	promo = {
		"nome": nome,
		"email": email,
		"preco": preco
	}

	sha = rbt.gera_assinatura_msg(promo, chave)

	promo['sha'] = sha

	resp = requests.post(
		"http://localhost:5000/criar-promocao",
		json=promo
	)

	print(resp.status_code)
	print(resp.json())