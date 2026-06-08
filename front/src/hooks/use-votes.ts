import { useCallback, useEffect, useState } from "react";

type VoteMap = Record<string, 0 | 1>;
const KEY = "promovale:votes";

function read(): VoteMap {
  if (typeof window === "undefined") return {};
  try {
    return JSON.parse(localStorage.getItem(KEY) ?? "{}");
  } catch {
    return {};
  }
}

export function useVotes() {
  const [votes, setVotes] = useState<VoteMap>({});

  useEffect(() => {
    setVotes(read());
  }, []);

  const toggle = useCallback((id: string) => {
    setVotes((prev) => {
      const updated = { ...prev, [id]: prev[id] === 1 ? 0 : 1 } as VoteMap;
      try {
        localStorage.setItem(KEY, JSON.stringify(updated));
      } catch {
        // ignore quota errors
      }
      return updated;
    });
  }, []);

  const adjusted = useCallback(
    (id: string, base: number) => base + (votes[id] ?? 0),
    [votes],
  );

  return { votes, toggle, adjusted };
}
