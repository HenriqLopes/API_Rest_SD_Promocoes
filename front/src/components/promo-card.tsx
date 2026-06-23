import { Zap } from "lucide-react";
import type { Promotion } from "@/lib/mock-data";
import { VoteControl } from "./vote-control";

type Props = {
  promo: Promotion;
  count: number;
  liked: boolean;
  onToggle: () => void;
};

const brl = (n: number) =>
  n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

export function PromoCard({ promo, count, liked, onToggle }: Props) {
  const hot = promo.hot === true;
  return (
    <article
      className={
        "group relative flex flex-col rounded-3xl border bg-card p-4 transition-all hover:shadow-xl hover:shadow-brand-orange/5 " +
        (hot
          ? "border-2 border-brand-orange hover:border-brand-orange"
          : "border-slate-200 hover:border-brand-orange/30")
      }
    >
      {hot && (
        <div className="absolute left-6 top-6 z-10">
          <span className="flex items-center gap-1 rounded-full bg-brand-orange px-3 py-1 text-[10px] font-bold uppercase tracking-wider text-white shadow-md shadow-brand-orange/30">
            <Zap className="h-3 w-3 fill-white" strokeWidth={0} />
            Hot Deal
          </span>
        </div>
      )}

      <div className="flex flex-1 flex-col">
        <div className="mb-1 text-[10px] font-bold uppercase tracking-wider text-slate-400">
          <span className="font-mono">ID #{promo.id}</span>
        </div>
        <h3 className="mb-3 line-clamp-2 min-h-10 text-sm font-semibold leading-tight text-slate-800">
          {promo.nome}
        </h3>

        <div className="mt-auto flex items-end justify-between gap-2">
          <span
            className={
              hot
                ? "text-lg font-bold text-brand-orange"
                : "text-lg font-bold text-slate-900"
            }
          >
            {brl(promo.preco)}
          </span>
          <VoteControl count={count} liked={liked} onToggle={onToggle} />
        </div>
      </div>
    </article>
  );
}
