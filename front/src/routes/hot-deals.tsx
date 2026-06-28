import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { PromoGrid } from "@/components/promo-grid";
import { usePromocoes } from "@/hooks/use-promocoes";

export const Route = createFileRoute("/hot-deals")({
  head: () => ({
    meta: [
      { title: "Hot Deals — PROMOVALE" },
      {
        name: "description",
        content: "Promoções em destaque com mais votos da comunidade.",
      },
    ],
  }),
  component: HotDeals,
});

function HotDeals() {
  const { promotions, loading, offline } = usePromocoes();

  const hot = promotions.filter((p) => p.hot === true);

  return (
    <PageShell>
      <header className="mb-8">
        <h1 className="font-display text-3xl font-bold tracking-tight">
          🔥 Hot Deals
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Promoções em destaque com votos suficientes da comunidade.
        </p>
      </header>
      <PromoGrid
        promotions={hot}
        emptyMessage="Ainda nenhuma promoção atingiu o limite de hot deal."
        loading={loading}
        offline={offline}
      />
    </PageShell>
  );
}
