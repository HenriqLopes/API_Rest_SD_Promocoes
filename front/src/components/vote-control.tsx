import { Heart } from "lucide-react";

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
      className={
        liked
          ? "flex items-center gap-1.5 rounded-full border border-brand-hot/30 bg-brand-hot/10 px-2.5 py-1.5"
          : "flex items-center gap-1.5 rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1.5"
      }
    >
      <Heart
        className={liked ? "h-4 w-4 fill-brand-hot text-brand-hot" : "h-4 w-4 text-slate-400"}
        strokeWidth={2.5}
      />
      <span className={liked ? "text-sm font-bold text-brand-hot" : "text-sm font-bold text-slate-600"}>
        {count}
      </span>
    </button>
  );
}
