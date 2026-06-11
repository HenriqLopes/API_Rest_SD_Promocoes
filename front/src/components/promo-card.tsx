import { Zap, Tag } from "lucide-react";
import type { Promotion } from "@/lib/mock-data";
import { isHotDeal } from "@/lib/mock-data";
import { VoteControl } from "./vote-control";

type Props = {
  promo: Promotion;
  count: number;
  liked: boolean;
  onToggle: () => void;
  highlighted?: boolean;
};

const brl = (n: number) =>
  n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

/** Placeholder visual no lugar da imagem do produto */
function PromoImagePlaceholder({ category }: { category: string }) {
  return (
    <div className="mb-4 flex aspect-square w-full items-center justify-center overflow-hidden rounded-2xl bg-slate-100 outline outline-1 -outline-offset-1 outline-black/5">
      <div className="flex flex-col items-center gap-2 text-slate-400">
        <Tag className="h-12 w-12" strokeWidth={1.2} />
        <span className="text-xs font-medium">{category}</span>
      </div>
    </div>
  );
}

export function PromoCard({ promo, count, liked, onToggle, highlighted }: Props) {
  const hot = isHotDeal(count);
  return (
    <article
      className={
        "group relative flex flex-col rounded-3xl border bg-card p-4 transition-all hover:shadow-xl hover:shadow-brand-orange/5 " +
        (highlighted
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

      <PromoImagePlaceholder category={promo.category} />

      <div className="flex flex-1 flex-col">
        <div className="mb-1 flex items-center justify-between text-[10px] font-bold uppercase tracking-wider text-slate-400">
          <span className="font-mono">ID #{promo.id}</span>
          <span className="text-brand-purple">{promo.store}</span>
        </div>
        <h3 className="mb-3 line-clamp-2 min-h-10 text-sm font-semibold leading-tight text-slate-800">
          {promo.title}
        </h3>
        <div className="mb-3">
          <span className="inline-block rounded-md bg-slate-100 px-2 py-0.5 text-[10px] font-medium text-slate-600">
            {promo.category}
          </span>
        </div>

        {/* Link para a oferta, se disponível */}
        {promo.url && (
          <a
            href={promo.url}
            target="_blank"
            rel="noopener noreferrer"
            className="mb-3 truncate text-xs text-brand-orange underline-offset-2 hover:underline"
          >
            Ver oferta ↗
          </a>
        )}

        <div className="mt-auto flex items-end justify-between gap-2">
          <div className="flex flex-col">
            {promo.originalPrice != null && promo.originalPrice > promo.price && (
              <span className="text-xs font-medium text-slate-400 line-through">
                {brl(promo.originalPrice)}
              </span>
            )}
            <span
              className={
                hot
                  ? "text-lg font-bold text-brand-orange"
                  : "text-lg font-bold text-slate-900"
              }
            >
              {brl(promo.price)}
            </span>
          </div>
          <VoteControl count={count} liked={liked} onToggle={onToggle} />
        </div>
      </div>
    </article>
  );
}
