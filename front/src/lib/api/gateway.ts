import type { Promotion } from "@/lib/mock-data";

const BASE_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? "http://localhost:5000";

// ── tipos ─────────────────────────────────────────────────────────────────────

/** Payload enviado ao criar uma promoção */
export type CreatePromoPayload = {
  nome: string;
  email: string;
  preco: number;
  sha: string;
};

export type InterestPayload = {
  email: string;
  categoria: string; // nome da categoria, ex: "Livro"
};

/** Resposta genérica de erro do gateway */
type GatewayError = { error: string };

// ── helpers ───────────────────────────────────────────────────────────────────

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let msg = `Erro HTTP ${res.status}`;
    try {
      const body = (await res.json()) as GatewayError;
      if (body.error) msg = body.error;
    } catch {
      // ignora falha no parse
    }
    throw new Error(msg);
  }
  return res.json() as Promise<T>;
}

/**
 * O gateway armazena IDs como int (chave do dict Python).
 * Normaliza para string para consistência com o tipo Promotion do front.
 * O campo 'hot' é setado diretamente pelo back e passado adiante.
 */
function normalizePromotion(raw: Record<string, unknown>): Promotion {
  return {
    ...(raw as Promotion),
    id: String(raw.id),
    preco: Number(raw.preco ?? 0),
    votes: Number(raw.votos ?? raw.votes ?? 0), // back usa 'votos'
    hot: raw.hot === true,
  };
}

// ── funções públicas ──────────────────────────────────────────────────────────

/**
 * GET /promocoes
 * Retorna todas as promoções cadastradas.
 * Gateway devolve { "1": {...}, "2": {...} } — convertemos para array.
 */
export async function listarPromocoes(): Promise<Promotion[]> {
  const res = await fetch(`${BASE_URL}/promocoes`);
  const data = await handleResponse<Record<string, Record<string, unknown>>>(res);
  return Object.values(data).map(normalizePromotion);
}

/**
 * POST /criar-promocao
 * Cadastra uma nova promoção. Retorna 201 com a promoção criada.
 */
export async function criarPromocao(payload: CreatePromoPayload): Promise<Promotion> {
  const res = await fetch(`${BASE_URL}/criar-promocao`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await handleResponse<Record<string, unknown>>(res);
  return normalizePromotion(data);
}

/**
 * PATCH /items/:id
 * Registra voto em uma promoção.
 *   voto: 1  → adiciona voto
 *   voto: -1 → remove voto
 */
export async function votarPromocao(id: string | number, voto: 1 | -1 = 1): Promise<Promotion> {
  const res = await fetch(`${BASE_URL}/items/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ voto }),
  });
  const data = await handleResponse<Record<string, unknown>>(res);
  return normalizePromotion(data);
}

export async function registrarInteresse(payload: InterestPayload): Promise<void> {
  const res = await fetch(`${BASE_URL}/interesse`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  await handleResponse<unknown>(res);
}

export async function cancelarInteresse(payload: InterestPayload): Promise<void> {
  const res = await fetch(`${BASE_URL}/interesse`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  await handleResponse<unknown>(res);
}