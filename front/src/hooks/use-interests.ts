import { useCallback, useEffect, useState } from "react";
import type { Category } from "@/lib/mock-data";

const KEY = "promovale:interests";

function read(): Category[] {
  if (typeof window === "undefined") return [];
  try {
    return JSON.parse(localStorage.getItem(KEY) ?? "[]");
  } catch {
    return [];
  }
}

export function useInterests() {
  const [interests, setInterests] = useState<Category[]>([]);

  useEffect(() => {
    setInterests(read());
  }, []);

  const persist = (next: Category[]) => {
    setInterests(next);
    try {
      localStorage.setItem(KEY, JSON.stringify(next));
    } catch {
      // ignore
    }
  };

  const toggle = useCallback((c: Category) => {
    const current = read();
    const next = current.includes(c)
      ? current.filter((x) => x !== c)
      : [...current, c];
    persist(next);
  }, []);

  const has = useCallback((c: Category) => interests.includes(c), [interests]);

  return { interests, toggle, has };
}
