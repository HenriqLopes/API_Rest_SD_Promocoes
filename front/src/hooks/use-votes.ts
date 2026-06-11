/**
 * use-votes.ts
 * Gerencia votos localmente (localStorage) e sincroniza com o gateway.
 *
 * Estratégia optimistic update:
 *  1. Atualiza o estado local imediatamente (UX rápida)
 *  2. Dispara o PATCH no gateway em background
 *  3. Em caso de erro, reverte o estado local
 */

import { useCallback, useEffect, useState } from "react";
import { votarPromocao } from "@/lib/api/gateway";

type VoteMap = Record<string, 0 | 1>;
const KEY = "promovale:votes";

function read(): VoteMap {
  if (typeof window === "undefined") return {};
  try {
    return JSON.parse(localStorage.getItem(KEY) ?? "{}");
  } catch {
    return {};
  }
}

export function useVotes() {
  const [votes, setVotes] = useState<VoteMap>({});

  useEffect(() => {
    setVotes(read());
  }, []);

  /**
   * Alterna o voto para uma promoção.
   * Envia +1 ao votar e -1 ao remover o voto para o gateway.
   */
  const toggle = useCallback((id: string) => {
    setVotes((prev) => {
      const wasVoted = prev[id] === 1;
      const updated = { ...prev, [id]: wasVoted ? 0 : 1 } as VoteMap;

      try {
        localStorage.setItem(KEY, JSON.stringify(updated));
      } catch {
        // ignora erros de quota
      }

      // sincroniza com o gateway em background (optimistic)
      const voto: 1 | -1 = wasVoted ? -1 : 1;
      votarPromocao(id, voto).catch(() => {
        // reverte em caso de erro de rede
        setVotes((current) => {
          const reverted = { ...current, [id]: wasVoted ? 1 : 0 } as VoteMap;
          try {
            localStorage.setItem(KEY, JSON.stringify(reverted));
          } catch {
            // ignora
          }
          return reverted;
        });
      });

      return updated;
    });
  }, []);

  /**
   * Retorna a contagem de votos ajustada pelo voto local do usuário.
   * Útil enquanto o backend não retorna o total atualizado.
   */
  const adjusted = useCallback(
    (id: string, base: number) => base + (votes[id] ?? 0),
    [votes],
  );

  return { votes, toggle, adjusted };
}
