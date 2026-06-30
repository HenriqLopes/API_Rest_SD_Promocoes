import { useState } from "react";
import { votarPromocao } from "@/lib/api/gateway";

type VoteMap = Record<string, 0 | 1>;

export function useVotes() {
  const [votes, setVotes] = useState<VoteMap>({});

  const toggle = async (id: string) => {
    const wasVoted = votes[id] === 1;
    const voto: 1 | -1 = wasVoted ? -1 : 1;
    
    setVotes({ ...votes, [id]: wasVoted ? 0 : 1 });
    await votarPromocao(id, voto);
  };

  return { votes, toggle };
}
