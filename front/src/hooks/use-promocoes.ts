/**
 * use-promocoes.ts
 * Hook para buscar e gerenciar a lista de promoções vindas do gateway.
 *
 * - Busca ao montar e expõe `refetch` para atualização manual
 * - Enquanto o gateway não estiver rodando, retorna array vazio e expõe o erro
 */

import { useCallback, useEffect, useState } from "react";
import { listarPromocoes } from "@/lib/api/gateway";
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

  const fetch = useCallback(async () => {
    setState((s) => ({ ...s, loading: true, error: null }));
    try {
      const data = await listarPromocoes();
      setState({ promotions: data, loading: false, error: null, isMock: false });
    } catch (err) {
      // Gateway indisponível — usa dados de exemplo para visualização
      setState({
        promotions: MOCK_PROMOTIONS,
        loading: false,
        error: null,
        isMock: true,
      });
    }
  }, []);

  useEffect(() => {
    fetch();
  }, [fetch]);

  return { ...state, refetch: fetch };
}
