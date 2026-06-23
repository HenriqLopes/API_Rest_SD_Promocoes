import { useCallback, useSyncExternalStore } from "react";
import type { Category } from "@/lib/mock-data";
import { cancelarInteresse, registrarInteresse } from "@/lib/api/gateway";

const EMAIL_KEY = "promovale:email";
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

function readEmail(): string {
  if(typeof window === "undefined") return "";
  return localStorage.getItem(EMAIL_KEY) ?? "";
}

function saveEmail(email: string) {
  localStorage.setItem(EMAIL_KEY, email);
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

  const toggle = useCallback(async (c: Category) => {
    const email = readEmail();
    const atual = read()
    const removendo = atual.includes(c)
    const prox = removendo ? atual.filter((x) => x !== c) : [...atual, c]
    emit(prox)

    if (email){
      try {
        if(removendo) {
          await cancelarInteresse({email, categoria: c })
        } else {
          await registrarInteresse({email, categoria: c })
        }
      } catch {
        emit(atual);
      }
    }
  }, []);

  const has = useCallback((c: Category) => interests.includes(c), [interests]);

  // para salvar/ler o email
  const setEmail = useCallback((email: string) => { saveEmail(email); }, []);
  const email = readEmail();

  return { interests, toggle, has, email, setEmail };
}
