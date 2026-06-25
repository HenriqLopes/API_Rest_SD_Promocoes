import requests
import time
import random

import rbt


nomes = ['Garrafa de agua', 'Caneta', 'Lapis', 'Borracha', 'Caderno', 'Mochila', 'Agenda', 'Livro', 'Revista', 'Jornal', 'Calculadora', 'Regua', 'Tesoura', 'Cola', 'Estojo', 'Marcador de texto', 'Papel sulfite', 'Pasta organizadora', 'Post-it', 'Grampeador', 'Smartphone', 'Notebook', 'Tablet', 'Monitor', 'Teclado', 'Mouse', 'Webcam', 'Impressora', 'Fone de ouvido', 'Caixa de som', 'Carregador portatil', 'Pendrive', 'HD externo', 'SSD', 'Roteador Wi-Fi', 'Cabo USB', 'Adaptador HDMI', 'Smartwatch', 'Controle de videogame', 'Videogame', 'Camiseta', 'Calca jeans', 'Bermuda', 'Jaqueta', 'Casaco', 'Moletom', 'Vestido', 'Saia', 'Camisa social', 'Terno', 'Gravata', 'Meias', 'Cueca', 'Sutia', 'Pijama', 'Chinelo', 'Tenis', 'Sapato social', 'Bota', 'Sandalia', 'Bone', 'Chapeu', 'Cachecol', 'Luvas', 'Cinto', 'Escova de dentes', 'Creme dental', 'Fio dental', 'Enxaguante bucal', 'Shampoo', 'Condicionador', 'Sabonete', 'Desodorante', 'Perfume', 'Protetor solar', 'Hidratante corporal', 'Escova de cabelo', 'Secador de cabelo', 'Aparelho de barbear', 'Toalha de banho', 'Sofa', 'Mesa de jantar', 'Cadeira', 'Poltrona', 'Estante', 'Guarda-roupa', 'Comoda', 'Escrivaninha', 'Cama', 'Colchao', 'Travesseiro', 'Lencol', 'Cobertor', 'Edredom', 'Cortina', 'Tapete', 'Luminaria', 'Espelho', 'Cabide', 'Sapateira', 'Geladeira', 'Fogao', 'Micro-ondas', 'Forno eletrico', 'Liquidificador', 'Batedeira', 'Cafeteira', 'Torradeira', 'Air fryer', 'Panela de pressao', 'Frigideira', 'Conjunto de panelas', 'Prato', 'Copo', 'Xicara', 'Talheres', 'Faca de cozinha', 'Tabua de corte', 'Pote hermetico', 'Garrafa termica', 'Arroz', 'Feijao', 'Macarrao', 'Farinha de trigo', 'Acucar', 'Sal', 'Cafe', 'Cha', 'Leite', 'Queijo', 'Iogurte', 'Manteiga', 'Ovos', 'Pao', 'Biscoito', 'Chocolate', 'Sorvete', 'Refrigerante', 'Suco', 'Agua mineral', 'Bicicleta', 'Capacete', 'Patins', 'Skate', 'Bola de futebol', 'Bola de basquete', 'Raquete de tenis', 'Corda de pular', 'Colchonete', 'Halteres', 'Elastico de resistencia', 'Luva de boxe', 'Rede de volei', 'Oculos de natacao', 'Prancha de surf', 'Barraca de camping', 'Saco de dormir', 'Lanterna', 'Mochila de trilha', 'Cantil', 'Mala de viagem', 'Trava de bicicleta', 'Guarda-chuva', 'Capa de chuva', 'Binoculo', 'Relogio', 'Pulseira', 'Colar', 'Anel', 'Brincos', 'oculos de sol', 'Bolsa', 'Carteira', 'Mala executiva', 'Necessaire', 'Mala de bordo', 'Broche', 'Pingente', 'Presilha de cabelo', 'Faixa de cabelo', 'Tinta para parede', 'Pincel de pintura', 'Rolo de pintura', 'Furadeira', 'Martelo', 'Chave de fenda', 'Alicate', 'Trena', 'Parafusos', 'Pregos', 'Fita isolante', 'Extensao eletrica', 'Lampada LED', 'Tomada inteligente', 'Fechadura eletronica', 'Detector de fumaca', 'Aspirador de po', 'Vassoura', 'Rodo', 'Balde', 'Sabao em po', 'Amaciante', 'Detergente', 'Desinfetante', 'Esponja de limpeza', 'Pano de chao', 'Papel higienico', 'Papel toalha', 'Sacos de lixo', 'Organizador de gaveta', 'Quadro decorativo', 'Vaso de planta', 'Planta ornamental', 'Almofada', 'Vela aromatica', 'Difusor de aromas', 'Porta-retratos', 'Relogio de parede', 'Escultura decorativa', 'Adesivo de parede', 'Violao', 'Guitarra', 'Teclado musical', 'Bateria eletronica', 'Microfone', 'Suporte para microfone', 'Estante para partituras', 'Ukulele', 'Harmonica', 'Pandeiro', 'Filme em Blu-ray', 'Jogo de tabuleiro', 'Quebra-cabeca', 'Baralho', 'Livro de colorir', 'album de fotos', 'Drone', 'Camera fotografica', 'Filmadora', 'Tripe', 'Cartao de memoria', 'Impressora 3D', 'Filamento para impressora 3D', 'Action figure', 'Pelucia', 'Boneca', 'Carrinho de brinquedo', 'Blocos de montar', 'Trenzinho eletrico', 'Patinete', 'Berco', 'Cadeirinha infantil para carro', 'Mamadeira', 'Chupeta', 'Fraldas', 'Babador', 'Carrinho de bebe', 'Banheira infantil', 'Tapete de atividades para bebe', 'Brinquedo educativo', 'Racao para cachorro', 'Racao para gato', 'Coleira', 'Guia para passeio', 'Caminha para pet', 'Arranhador para gatos', 'Caixa de transporte para pet', 'Brinquedo para cachorro', 'Aquario', 'Comedouro para pet', 'Sementes para jardim', 'Adubo', 'Mangueira de jardim', 'Pa de jardinagem', 'Tesoura de poda', 'Regador', 'Vaso grande', 'Terra vegetal', 'Grama em placas', 'Composteira', 'Carro', 'Moto', 'Capacete para moto', 'Capa para carro', 'Tapete automotivo', 'GPS automotivo', 'Suporte para celular veicular', 'Compressor de ar portatil', 'Cera automotiva', 'Limpador de para-brisa', 'Seguro residencial', 'Seguro automotivo', 'Curso online', 'Assinatura de streaming', 'Ingresso para cinema', 'Ingresso para show', 'Passagem aerea', 'Hospedagem em hotel', 'Vale-presente', 'Assinatura de academia']
PRECO_MIN = 0
PRECO_MAX = 50
emails = ['gustavobuenodacosta@gmail.com', 'buenogustavodacosta@gmail.com']
#keys = ['livro', 'roupa', 'esporte', 'domestico', 'comida']
keys = [2, 3, 4, 5, 1]

while True:

	time.sleep(5) #registra uma promo aleatoria a cada 5 seg

	nome = random.choice(nomes)
	preco = random.randint(PRECO_MIN, PRECO_MAX)
	email = random.choice(emails)
	categoria = random.choice(keys)

	chave = None
	if (email == 'gustavobuenodacosta@gmail.com'):
		chave = 'tools/priv_loj1.der'
	else:
		chave = 'tools/priv_loj2.der'	

	promo = {
		"nome": nome,
		"email": email,
		"preco": preco,
		"categoria": categoria
	}

	sha = rbt.gera_assinatura_msg(str(promo),chave)

	promo['sha'] = sha

	resp = requests.post(
		"http://localhost:5000/criar-promocao",
		json=promo
	)

	print(f"[] Postando promocao: {nome} ({preco} R$)")
	print(f"[] status do envio: {resp.status_code}")
