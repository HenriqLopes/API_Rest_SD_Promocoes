export const HOT_DEAL_THRESHOLD = 100;

export type Category =
  | "Eletrônicos"
  | "Hardware"
  | "Games"
  | "Smartphones"
  | "Casa e Cozinha"
  | "Áudio"
  | "Moda";

export const CATEGORIES: { name: Category; emoji: string }[] = [
  { name: "Eletrônicos", emoji: "📺" },
  { name: "Hardware", emoji: "💻" },
  { name: "Games", emoji: "🎮" },
  { name: "Smartphones", emoji: "📱" },
  { name: "Casa e Cozinha", emoji: "🏠" },
  { name: "Áudio", emoji: "🔊" },
  { name: "Moda", emoji: "👟" },
];

/** Tipo que reflete o que o gateway retorna */
export type Promotion = {
  id: string;       // gateway retorna int, convertemos para string no gateway.ts
  title: string;
  store: string;
  category: Category;
  url?: string;
  email?: string;
  price: number;
  originalPrice?: number;
  votes: number;
};

export function isHotDeal(votes: number) {
  return votes >= HOT_DEAL_THRESHOLD;
}

/** Dados de exemplo usados quando o gateway não está disponível */
export const MOCK_PROMOTIONS: Promotion[] = [
  { id: "1", title: 'Smart TV 55" 4K Ultra HD',           store: "Amazon",        category: "Eletrônicos",   url: "https://amazon.com.br",         price: 2450,  originalPrice: 3499, votes: 142 },
  { id: "2", title: "Teclado Mecânico RGB Wireless",       store: "Kabum",         category: "Hardware",      url: "https://kabum.com.br",           price: 899,   originalPrice: 1200, votes: 45  },
  { id: "3", title: "Fone Bluetooth Cancelamento de Ruído",store: "Mercado Livre", category: "Áudio",         url: "https://mercadolivre.com.br",    price: 1950,  originalPrice: 2400, votes: 218 },
  { id: "4", title: "Air Fryer 4L Inox",                   store: "Magalu",        category: "Casa e Cozinha",url: "https://magazineluiza.com.br",   price: 329.9, originalPrice: 499,  votes: 210 },
  { id: "5", title: "Smartphone 256GB Azul",               store: "Amazon",        category: "Smartphones",   url: "https://amazon.com.br",         price: 3799,  originalPrice: 4999, votes: 87  },
  { id: "6", title: "Cafeteira Espresso Automática",       store: "Magalu",        category: "Casa e Cozinha",url: "https://magazineluiza.com.br",   price: 499,   originalPrice: 799,  votes: 31  },
  { id: "7", title: "Controle Sem Fio para PC e Console",  store: "Kabum",         category: "Games",         url: "https://kabum.com.br",           price: 379,   originalPrice: 499,  votes: 156 },
  { id: "8", title: "Tênis Running Cushion Pro",           store: "Netshoes",      category: "Moda",          url: "https://netshoes.com.br",        price: 299.9, originalPrice: 549,  votes: 64  },
];
