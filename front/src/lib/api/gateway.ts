/**
 * gateway.ts
 * Camada de integração com o gateway.py (Flask REST API).
 *
 * Contrato das rotas (gateway.py):
 *   GET    /promocoes           → { "1": {promo}, "2": {promo}, ... }
 *   GET    /promocoes/:id       → {promo} | { error }
 *   POST   /criar-promocao      → {promo criada} (201)
 *   PATCH  /items/:id           → body: { voto: 1 | -1 }  → {promo atualizada}
 *   DELETE /promocoes/:id       → { message } | { error }
 *
 * Para adicionar uma nova rota no back:
 *   1. Implemente a rota no gateway.py
 *   2. Adicione a função correspondente aqui seguindo o mesmo padrão
 *   3. O front já está pronto para consumir via hooks ou chamada direta
 */

import type { Promotion } from "@/lib/mock-data";

const BASE_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? "http://localhost:5000";

// ── tipos ─────────────────────────────────────────────────────────────────────

/** Payload enviado ao criar uma promoção */
export type CreatePromoPayload = {
  nome: string;
  store: string;
  email: string;
  url: string;
  preco: number;
  originalpreco?: number;
  category: string;
  sha: string;
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
 */
function normalizePromotion(raw: Record<string, unknown>): Promotion {
  return {
    ...(raw as Promotion),
    id: String(raw.id),
    votes: Number(raw.votes ?? 0),
    preco: Number(raw.preco ?? 0),
    originalpreco: raw.originalpreco != null ? Number(raw.originalpreco) : undefined,
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
 * GET /promocoes/:id
 * Busca uma promoção específica pelo ID.
 */
export async function buscarPromocao(id: string | number): Promise<Promotion> {
  const res = await fetch(`${BASE_URL}/promocoes/${id}`);
  const data = await handleResponse<Record<string, unknown>>(res);
  return normalizePromotion(data);
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

/**
 * DELETE /promocoes/:id
 * Remove uma promoção pelo ID.
 */
export async function apagarPromocao(id: string | number): Promise<{ message: string }> {
  const res = await fetch(`${BASE_URL}/promocoes/${id}`, {
    method: "DELETE",
  });
  return handleResponse<{ message: string }>(res);
}