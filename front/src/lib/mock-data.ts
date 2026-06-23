export type Category = "Comida" | "Livro" | "Roupa" | "Doméstico" | "Esporte"

export const CATEGORIES = [
  { name: "Comida",     emoji: "🍔" },
  { name: "Livro",      emoji: "📚" },
  { name: "Roupa",      emoji: "👕" },
  { name: "Esporte",    emoji: "⚽" },
  { name: "Doméstico",  emoji: "🏠" },
]

/** Tipo que reflete o que o gateway retorna */
export type Promotion = {
  id: string;
  nome: string;
  email?: string;
  preco: number;
  votes: number;
  hot?: boolean;
};

/** Dados de exemplo usados quando o gateway não está disponível */
export const MOCK_PROMOTIONS: Promotion[] = [
  { id: "1", nome: 'Smart TV 55" 4K Ultra HD',            email: "loja1@exemplo.com", preco: 2450,  votes: 142 },
  { id: "2", nome: "Teclado Mecânico RGB Wireless",        email: "loja2@exemplo.com", preco: 899,   votes: 45  },
  { id: "3", nome: "Fone Bluetooth Cancelamento de Ruído", email: "loja3@exemplo.com", preco: 1950,  votes: 218 },
  { id: "4", nome: "Air Fryer 4L Inox",                    email: "loja4@exemplo.com", preco: 329.9, votes: 210 },
  { id: "5", nome: "Smartphone 256GB Azul",                email: "loja5@exemplo.com", preco: 3799,  votes: 87  },
  { id: "6", nome: "Cafeteira Espresso Automática",        email: "loja6@exemplo.com", preco: 499,   votes: 31  },
  { id: "7", nome: "Controle Sem Fio para PC e Console",   email: "loja7@exemplo.com", preco: 379,   votes: 156 },
  { id: "8", nome: "Tênis Running Cushion Pro",            email: "loja8@exemplo.com", preco: 299.9, votes: 64  },
];
