import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { PromoGrid } from "@/components/promo-grid";
import { CategoryPicker } from "@/components/category-picker";
import { PROMOTIONS } from "@/lib/mock-data";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "PROMOVALE — Promoções em destaque" },
      {
        name: "description",
        content:
          "Veja as promoções ativas da comunidade, vote nas melhores e descubra hot deals em tempo real.",
      },
    ],
  }),
  component: Index,
});

function Index() {
  return (
    <PageShell>
      <CategoryPicker />
      <header className="mb-8">
        <h1 className="font-display text-3xl font-bold tracking-tight">
          Todas as promoções
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Vote nas ofertas que valem a pena. Promoções com {">"} 100 votos viram{" "}
          <span className="font-semibold text-brand-orange">Hot Deals</span>.
        </p>
      </header>
      <PromoGrid promotions={PROMOTIONS} highlightInterests />
    </PageShell>
  );
}
