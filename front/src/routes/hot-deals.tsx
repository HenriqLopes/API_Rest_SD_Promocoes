import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { PromoGrid } from "@/components/promo-grid";
import { PROMOTIONS, isHotDeal } from "@/lib/mock-data";
import { useVotes } from "@/hooks/use-votes";

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
  const { adjusted } = useVotes();
  const hot = PROMOTIONS.filter((p) => isHotDeal(adjusted(p.id, p.votes)));

  return (
    <PageShell>
      <header className="mb-8">
        <h1 className="font-display text-3xl font-bold tracking-tight">
          🔥 Hot Deals
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Promoções com mais de 100 votos positivos.
        </p>
      </header>
      <PromoGrid
        promotions={hot}
        emptyMessage="Ainda nenhuma promoção atingiu o limite de hot deal."
      />
    </PageShell>
  );
}
