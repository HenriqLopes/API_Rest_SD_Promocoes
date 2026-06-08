import { createFileRoute } from "@tanstack/react-router";
import { Check } from "lucide-react";
import { PageShell } from "@/components/page-shell";
import { CATEGORIES } from "@/lib/mock-data";
import { useInterests } from "@/hooks/use-interests";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/categorias")({
  head: () => ({
    meta: [
      { title: "Categorias — PROMOVALE" },
      {
        name: "description",
        content: "Escolha as categorias que você quer acompanhar.",
      },
    ],
  }),
  component: CategoriasPage,
});

function CategoriasPage() {
  const { has, toggle, interests } = useInterests();

  return (
    <PageShell>
      <header className="mb-8">
        <h1 className="font-display text-3xl font-bold tracking-tight">
          Suas categorias
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Toque para acompanhar ou parar de acompanhar. Você receberá
          notificações em tempo real ({interests.length} selecionada
          {interests.length === 1 ? "" : "s"}).
        </p>
      </header>

      <div className="flex flex-wrap gap-3">
        {CATEGORIES.map((c) => {
          const active = has(c.name);
          return (
            <button
              key={c.name}
              type="button"
              onClick={() => toggle(c.name)}
              className={cn(
                "flex items-center gap-2 rounded-2xl border px-5 py-3 text-sm font-semibold transition-all",
                active
                  ? "border-2 border-brand-orange bg-brand-orange/5 text-slate-900"
                  : "border-slate-200 bg-card text-slate-700 hover:border-slate-300",
              )}
            >
              <span className="text-lg">{c.emoji}</span>
              {c.name}
              {active && (
                <span className="ml-1 flex h-5 w-5 items-center justify-center rounded-full bg-brand-orange text-white">
                  <Check className="h-3 w-3" strokeWidth={3} />
                </span>
              )}
            </button>
          );
        })}
      </div>
    </PageShell>
  );
}
