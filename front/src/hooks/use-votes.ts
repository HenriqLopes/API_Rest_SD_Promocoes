/**
 * use-votes.ts
 * Gerencia votos localmente (memória de sessão) e sincroniza com o gateway.
 *
 * Estratégia optimistic update:
 *  1. Atualiza o estado local imediatamente (UX rápida)
 *  2. Dispara o PATCH no gateway em background
 *  3. O SSE traz o total real atualizado — adjusted retorna o base direto
 *
 * Votos NÃO persistem entre sessões — o back não tem memória de quem votou,
 * apenas soma/subtrai no dicionário em memória.
 */

import { useCallback, useState } from "react";
import { votarPromocao } from "@/lib/api/gateway";

type VoteMap = Record<string, 0 | 1>;

export function useVotes() {
  // Estado começa zerado a cada sessão — sem leitura de localStorage
  const [votes, setVotes] = useState<VoteMap>({});

  /**
   * Alterna o voto para uma promoção.
   * Envia +1 ao votar e -1 ao remover o voto para o gateway.
   */
  const toggle = useCallback((id: string) => {
    setVotes((prev) => {
      const wasVoted = prev[id] === 1;
      const updated = { ...prev, [id]: wasVoted ? 0 : 1 } as VoteMap;

      // sincroniza com o gateway em background (optimistic)
      const voto: 1 | -1 = wasVoted ? -1 : 1;
      votarPromocao(id, voto).catch(() => {
        // reverte o estado local em caso de erro de rede
        setVotes((current) => ({
          ...current,
          [id]: wasVoted ? 1 : 0,
        }) as VoteMap);
      });

      return updated;
    });
  }, []);

  /**
   * O total de votos vem direto do back via SSE — não somamos ajuste local.
   * O parâmetro `id` é mantido na assinatura para compatibilidade com PromoGrid.
   */
  const adjusted = useCallback(
    (_id: string, base: number) => base,
    [],
  );

  return { votes, toggle, adjusted };
}
