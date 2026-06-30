import { useEffect, useRef, useState } from "react";
import { abrirStreamPromocoes } from "@/lib/api/gateway";
import type { Promotion } from "@/lib/mock-data";

export function usePromocoes() {
  const [promotions, setPromotions] = useState<Promotion[]>([]);
  const [loading, setLoading] = useState(true);
  const esRef = useRef<EventSource | null>(null);

  function conectar() {
    esRef.current?.close();
    setLoading(true);

    esRef.current = abrirStreamPromocoes((data) => {
      setPromotions(data);
      setLoading(false);
    });
  }

  useEffect(() => {
    conectar();
    return () => esRef.current?.close();
  }, []);

  return { promotions, loading, refetch: conectar };
}
