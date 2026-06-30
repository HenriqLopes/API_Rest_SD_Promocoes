import { useState, useEffect } from "react";
import type { Category } from "@/lib/mock-data";
import { cancelarInteresse, registrarInteresse } from "@/lib/api/gateway";

const EMAIL_KEY = "promovale:email";
const KEY = "promovale:interests";

export function useInterests() {
  const [interests, setInterests] = useState<Category[]>(() => {
    const saved = localStorage.getItem(KEY);
    return saved ? JSON.parse(saved) : [];
  });

  const [email, setEmailState] = useState(() => {
    return localStorage.getItem(EMAIL_KEY) ?? "";
  });

  useEffect(() => {
    localStorage.setItem(KEY, JSON.stringify(interests));
  }, [interests]);

  const toggle = async (c: Category) => {
    const removendo = interests.includes(c);
    const prox = removendo ? interests.filter((x) => x !== c) : [...interests, c];
    
    setInterests(prox);

    if (email) {
      if (removendo) {
        await cancelarInteresse({ email, categoria: c });
      } else {
        await registrarInteresse({ email, categoria: c });
      }
    }
  };

  const has = (c: Category) => interests.includes(c);

  const setEmail = (newEmail: string) => {
    setEmailState(newEmail);
    localStorage.setItem(EMAIL_KEY, newEmail);
  };

  return { interests, toggle, has, email, setEmail };
}
