import type { Promotion } from "@/lib/mock-data";
import { useVotes } from "@/hooks/use-votes";
import { PromoCard } from "./promo-card";

type Props = {
  promotions: Promotion[];
  emptyMessage?: string;
  loading?: boolean;
  offline?: boolean;
};

function PromoCardSkeleton() {
  return (
    <div className="flex flex-col rounded-3xl border border-slate-200 bg-card p-4 animate-pulse">
      <div className="mb-4 aspect-square w-full rounded-2xl bg-slate-100" />
      <div className="space-y-2">
        <div className="h-3 w-1/2 rounded bg-slate-100" />
        <div className="h-4 w-full rounded bg-slate-100" />
        <div className="h-4 w-3/4 rounded bg-slate-100" />
        <div className="mt-4 h-6 w-1/3 rounded bg-slate-100" />
      </div>
    </div>
  );
}

export function PromoGrid({
  promotions,
  emptyMessage,
  loading = false,
  offline = false,
}: Props) {
  const { votes, toggle, adjusted } = useVotes();

  if (loading) {
    return (
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 8 }).map((_, i) => (
          <PromoCardSkeleton key={i} />
        ))}
      </div>
    );
  }

  if (offline) {
    return (
      <div className="rounded-3xl border border-dashed border-slate-300 bg-card p-12 text-center">
        <p className="text-sm text-muted-foreground">
          Gateway indisponível — inicie o{" "}
          <code className="rounded bg-slate-100 px-1">gateway.py</code> para ver as promoções.
        </p>
      </div>
    );
  }

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
