import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { PromoGrid } from "@/components/promo-grid";
import { CategoryPicker } from "@/components/category-picker";
import { usePromocoes } from "@/hooks/use-promocoes";

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
  const { promotions, loading, error, isMock, refetch } = usePromocoes();

  return (
    <PageShell>
      <CategoryPicker />
      <header className="mb-8 flex items-start justify-between gap-4">
        <div>
          <h1 className="font-display text-3xl font-bold tracking-tight">
            Todas as promoções
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Vote nas ofertas que valem a pena. Promoções com {">"} 100 votos viram{" "}
            <span className="font-semibold text-brand-orange">Hot Deals</span>.
          </p>
        </div>
        <button
          type="button"
          onClick={refetch}
          disabled={loading}
          className="mt-1 rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-600 transition hover:border-slate-300 disabled:opacity-50"
        >
          {loading ? "Carregando..." : "↺ Atualizar"}
        </button>
      </header>
      <PromoGrid
        promotions={promotions}
        highlightInterests
        loading={loading}
        isMock={isMock}
      />
    </PageShell>
  );
}
