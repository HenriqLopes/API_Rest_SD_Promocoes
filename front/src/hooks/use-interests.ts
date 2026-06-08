import { useCallback, useSyncExternalStore } from "react";
import type { Category } from "@/lib/mock-data";

const KEY = "promovale:interests";
const EVENT = "promovale:interests:change";

function read(): Category[] {
  if (typeof window === "undefined") return [];
  try {
    return JSON.parse(localStorage.getItem(KEY) ?? "[]");
  } catch {
    return [];
  }
}

let cache: Category[] = typeof window === "undefined" ? [] : read();

function emit(next: Category[]) {
  cache = next;
  try {
    localStorage.setItem(KEY, JSON.stringify(next));
  } catch {
    // ignore
  }
  window.dispatchEvent(new Event(EVENT));
}

function subscribe(cb: () => void) {
  window.addEventListener(EVENT, cb);
  window.addEventListener("storage", cb);
  return () => {
    window.removeEventListener(EVENT, cb);
    window.removeEventListener("storage", cb);
  };
}

const EMPTY: Category[] = [];

export function useInterests() {
  const interests = useSyncExternalStore(
    subscribe,
    () => cache,
    () => EMPTY,
  );

  const toggle = useCallback((c: Category) => {
    const current = read();
    const next = current.includes(c)
      ? current.filter((x) => x !== c)
      : [...current, c];
    emit(next);
  }, []);

  const has = useCallback((c: Category) => interests.includes(c), [interests]);

  return { interests, toggle, has };
}
