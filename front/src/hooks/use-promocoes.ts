/**
 * use-promocoes.ts
 * Hook para buscar e gerenciar a lista de promoções vindas do gateway via SSE.
 *
 * - Abre uma conexão SSE ao montar e recebe atualizações em tempo real
 * - Fecha a conexão SSE ao desmontar o componente
 */

import { useEffect, useRef, useState } from "react";
import { abrirStreamPromocoes } from "@/lib/api/gateway";
import type { Promotion } from "@/lib/mock-data";

type State = {
  promotions: Promotion[];
  loading: boolean;
  offline: boolean;
};

export function usePromocoes() {
  const [state, setState] = useState<State>({
    promotions: [],
    loading: true,
    offline: false,
  });

  const esRef = useRef<EventSource | null>(null);

  function conectar() {
    esRef.current?.close();
    setState((s) => ({ ...s, loading: true, offline: false }));

    esRef.current = abrirStreamPromocoes(
      (data) => {
        console.log('[usePromocoes] Recebeu dados via SSE:', data.length, 'promoções');
        console.log('[usePromocoes] Primeira promoção (amostra):', data[0]);
        setState({ promotions: data, loading: false, offline: false });
      },
      () => {
        console.log('[usePromocoes] SSE erro - gateway offline');
        setState({ promotions: [], loading: false, offline: true });
        esRef.current?.close();
      },
    );
  }

  useEffect(() => {
    conectar();
    return () => esRef.current?.close();
  }, []);

  return { ...state, refetch: conectar };
}
