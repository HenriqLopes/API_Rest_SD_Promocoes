import type { Promotion } from "@/lib/mock-data";
import { useVotes } from "@/hooks/use-votes";
import { PromoCard } from "./promo-card";

export function PromoGrid({
  promotions,
  emptyMessage,
}: {
  promotions: Promotion[];
  emptyMessage?: string;
}) {
  const { votes, toggle, adjusted } = useVotes();

  if (promotions.length === 0) {
    return (
      <div className="rounded-3xl border border-dashed border-slate-300 bg-card p-12 text-center">
        <p className="text-sm text-muted-foreground">
          {emptyMessage ?? "Nenhuma promoção encontrada."}
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
      {promotions.map((p) => (
        <PromoCard
          key={p.id}
          promo={p}
          count={adjusted(p.id, p.votes)}
          liked={votes[p.id] === 1}
          onToggle={() => toggle(p.id)}
        />
      ))}
    </div>
  );
}
