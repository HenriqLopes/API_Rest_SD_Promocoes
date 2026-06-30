export type Category = "Comida" | "Livro" | "Roupa" | "Doméstico" | "Esporte"

export const CATEGORIES = [
  { name: "Comida",     emoji: "🍔", id: 1 },
  { name: "Livro",      emoji: "📚", id: 2 },
  { name: "Roupa",      emoji: "👕", id: 3 },
  { name: "Esporte",    emoji: "⚽", id: 4 },
  { name: "Doméstico",  emoji: "🏠", id: 5 },
]

/** Mapeia nome de categoria para ID do backend */
export const CATEGORY_NAME_TO_ID: Record<Category, number> = {
  "Comida": 1,
  "Livro": 2,
  "Roupa": 3,
  "Esporte": 4,
  "Doméstico": 5,
}

/** Mapeia ID do backend para nome de categoria */
export const CATEGORY_ID_TO_NAME: Record<number, Category> = {
  1: "Comida",
  2: "Livro",
  3: "Roupa",
  4: "Esporte",
  5: "Doméstico",
}

/** Tipo que reflete o que o gateway retorna */
export type Promotion = {
  id: string;
  nome: string;
  email?: string;
  preco: number;
  votos: number;
  hot?: boolean;
  categoria?: number; // ID da categoria (1-5)
};
