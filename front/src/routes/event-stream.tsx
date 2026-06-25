import { createFileRoute } from '@tanstack/react-router'
import { useEffect, useState } from "react";

const BASE_URL =
  (import.meta.env.VITE_API_URL as string | undefined) ?? "http://localhost:5000";

export const Route = createFileRoute("/event-stream")({
  head: () => ({
    meta: [{ title: "SSE Debug — PROMOVALE" }],
  }),
  component: EventStreamPage,
});

function EventStreamPage() {
  const [logs, setLogs] = useState<string[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const es = new EventSource(`${BASE_URL}/stream`);

    es.onopen = () => setConnected(true);

    es.onmessage = (e) => {
      const timestamp = new Date().toLocaleTimeString();
      setLogs((prev) => [`[${timestamp}] ${e.data}`, ...prev.slice(0, 49)]);
    };

    es.onerror = () => {
      setConnected(false);
      setLogs((prev) => [
        `[${new Date().toLocaleTimeString()}] ERRO — conexão perdida`,
        ...prev,
      ]);
    };

    return () => es.close();
  }, []);

  return (
    <div className="p-6 font-mono text-xs">
      <div className="mb-4 flex items-center gap-3">
        <h1 className="text-lg font-bold">SSE Debug</h1>
        <span
          className={`rounded-full px-2 py-0.5 text-[10px] font-semibold ${
            connected
              ? "bg-green-100 text-green-700"
              : "bg-red-100 text-red-600"
          }`}
        >
          {connected ? "conectado" : "desconectado"}
        </span>
      </div>

      {logs.length === 0 ? (
        <p className="text-muted-foreground">Aguardando eventos...</p>
      ) : (
        <ul className="space-y-1">
          {logs.map((l, i) => (
            <li key={i} className="border-b border-slate-100 py-1 break-all">
              {l}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}