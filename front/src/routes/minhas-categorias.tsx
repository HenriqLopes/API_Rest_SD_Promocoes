import { createFileRoute, Link } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { PromoGrid } from "@/components/promo-grid";
import { useInterests } from "@/hooks/use-interests";
import { usePromocoes } from "@/hooks/use-promocoes";
import { CATEGORY_NAME_TO_ID, type Category } from "@/lib/mock-data";
import { useMemo } from "react";

export const Route = createFileRoute("/minhas-categorias")({
  head: () => ({
    meta: [
      { title: "Minhas Categorias — PROMOVALE" },
      {
        name: "description",
        content: "Promoções filtradas pelas categorias que você acompanha.",
      },
    ],
  }),
  component: MinhasCategorias,
});

function MinhasCategorias() {
  const { interests } = useInterests();
  const { promotions, loading, offline } = usePromocoes();
  
  // Converte nomes de categoria para IDs do backend
  const categoriaIds = useMemo(() => 
    interests.map((name) => CATEGORY_NAME_TO_ID[name as Category]),
    [interests]
  );
  
  // Filtra promoções no FRONTEND pelas categorias selecionadas
  const filteredPromotions = useMemo(() => {
    if (categoriaIds.length === 0) return [];
    
    console.log('[MinhasCategorias] Total de promoções:', promotions.length);
    console.log('[MinhasCategorias] Categorias selecionadas (IDs):', categoriaIds);
    console.log('[MinhasCategorias] Categorias selecionadas (nomes):', interests);
    
    const filtered = promotions.filter(p => {
      const hasCategoria = p.categoria && categoriaIds.includes(p.categoria);
      if (hasCategoria) {
        console.log(`[MinhasCategorias] ✅ Incluindo promoção #${p.id} (categoria: ${p.categoria})`);
      }
      return hasCategoria;
    });
    
    console.log('[MinhasCategorias] Promoções filtradas:', filtered.length);
    return filtered;
  }, [promotions, categoriaIds, interests]);

  return (
    <PageShell>
      <header className="mb-8">
        <h1 className="font-display text-3xl font-bold tracking-tight">
          Minhas categorias
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          {interests.length === 0
            ? "Você ainda não selecionou categorias de interesse."
            : `Acompanhando: ${interests.join(", ")} (IDs: ${categoriaIds.join(", ")})`}
        </p>
      </header>

      {interests.length === 0 ? (
        <div className="rounded-3xl border border-dashed border-slate-300 bg-card p-12 text-center">
          <p className="text-sm text-muted-foreground">
            Escolha categorias para receber notificações em tempo real.
          </p>
          <Link
            to="/"
            className="mt-4 inline-block rounded-xl bg-brand-orange px-5 py-2 text-sm font-bold text-white"
          >
            Escolher categorias
          </Link>
        </div>
      ) : (
        <PromoGrid
          promotions={filteredPromotions}
          emptyMessage="Sem promoções ativas no momento para as categorias selecionadas."
          loading={loading}
          offline={offline}
        />
      )}
    </PageShell>
  );
}
