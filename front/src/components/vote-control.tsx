import { Heart } from "lucide-react";
import { cn } from "@/lib/utils";

type Props = {
  count: number;
  liked: boolean;
  onToggle: () => void;
};

export function VoteControl({ count, liked, onToggle }: Props) {
  return (
    <button
      type="button"
      onClick={onToggle}
      aria-label={liked ? "Remover curtida" : "Curtir promoção"}
      aria-pressed={liked}
      className={cn(
        "group/like flex items-center gap-1.5 rounded-full border px-2.5 py-1.5 transition-all active:scale-95",
        liked
          ? "border-brand-hot/30 bg-brand-hot/10"
          : "border-slate-200 bg-slate-50 hover:border-brand-hot/30 hover:bg-brand-hot/5",
      )}
    >
      <Heart
        className={cn(
          "h-4 w-4 transition-transform group-hover/like:scale-110",
          liked
            ? "fill-brand-hot text-brand-hot animate-in zoom-in-50 duration-200"
            : "text-slate-400 group-hover/like:text-brand-hot",
        )}
        strokeWidth={2.5}
      />
      <span
        className={cn(
          "min-w-4 text-center text-sm font-bold tabular-nums",
          liked ? "text-brand-hot" : "text-slate-600",
        )}
      >
        {count}
      </span>
    </button>
  );
}
