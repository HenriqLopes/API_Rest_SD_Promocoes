/**
 * use-promocoes.ts
 * Hook para buscar e gerenciar a lista de promoções vindas do gateway via SSE.
 *
 * - Abre uma conexão SSE ao montar e recebe atualizações em tempo real
 * - Enquanto o gateway não estiver rodando, retorna dados de exemplo (mock)
 * - Fecha a conexão SSE ao desmontar o componente
 */

import { useEffect, useRef, useState } from "react";
import { abrirStreamPromocoes } from "@/lib/api/gateway";
import type { Promotion } from "@/lib/mock-data";
import { MOCK_PROMOTIONS } from "@/lib/mock-data";

type State = {
  promotions: Promotion[];
  loading: boolean;
  error: string | null;
  isMock: boolean;
};

export function usePromocoes() {
  const [state, setState] = useState<State>({
    promotions: [],
    loading: true,
    error: null,
    isMock: false,
  });

  // Ref para poder fechar e reabrir o EventSource no refetch
  const esRef = useRef<EventSource | null>(null);

  function conectar() {
    // Fecha conexão anterior se existir
    esRef.current?.close();

    setState((s) => ({ ...s, loading: true, error: null, isMock: false }));

    esRef.current = abrirStreamPromocoes(
      (data) => {
        setState({ promotions: data, loading: false, error: null, isMock: false });
      },
      () => {
        // Gateway indisponível — usa dados de exemplo para visualização
        setState({ promotions: MOCK_PROMOTIONS, loading: false, error: null, isMock: true });
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
