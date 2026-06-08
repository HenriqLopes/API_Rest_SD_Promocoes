import { Check } from "lucide-react";
import { CATEGORIES } from "@/lib/mock-data";
import { useInterests } from "@/hooks/use-interests";
import { cn } from "@/lib/utils";

export function CategoryPicker() {
  const { has, toggle, interests } = useInterests();

  return (
    <section className="mb-8 rounded-3xl border border-slate-200 bg-card p-5">
      <div className="mb-3 flex items-baseline justify-between gap-3">
        <h2 className="font-display text-lg font-bold tracking-tight">
          Suas categorias
        </h2>
        <p className="text-xs text-muted-foreground">
          {interests.length} selecionada{interests.length === 1 ? "" : "s"}
        </p>
      </div>
      <div className="flex flex-wrap gap-2">
        {CATEGORIES.map((c) => {
          const active = has(c.name);
          return (
            <button
              key={c.name}
              type="button"
              onClick={() => toggle(c.name)}
              className={cn(
                "flex items-center gap-2 rounded-full border px-4 py-2 text-sm font-semibold transition-all",
                active
                  ? "border-2 border-brand-orange bg-brand-orange/5 text-slate-900"
                  : "border-slate-200 bg-white text-slate-700 hover:border-slate-300",
              )}
            >
              <span>{c.emoji}</span>
              {c.name}
              {active && (
                <span className="flex h-4 w-4 items-center justify-center rounded-full bg-brand-orange text-white">
                  <Check className="h-2.5 w-2.5" strokeWidth={3} />
                </span>
              )}
            </button>
          );
        })}
      </div>
    </section>
  );
}
