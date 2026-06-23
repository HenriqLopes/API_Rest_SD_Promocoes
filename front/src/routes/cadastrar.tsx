import { createFileRoute } from "@tanstack/react-router";
import { useState, type FormEvent } from "react";
import { PageShell } from "@/components/page-shell";
import { criarPromocao } from "@/lib/api/gateway";
import { toast } from "sonner";

export const Route = createFileRoute("/cadastrar")({
  head: () => ({
    meta: [
      { title: "Cadastrar promoção — PROMOVALE" },
      {
        name: "description",
        content: "Lojas podem publicar uma nova promoção para a comunidade.",
      },
    ],
  }),
  component: CadastrarPage,
});

function CadastrarPage() {
  const [submitting, setSubmitting] = useState(false);

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const formData = new FormData(e.currentTarget);

      await criarPromocao({
        nome: formData.get("nome") as string,
        email: formData.get("email") as string,
        preco: parseFloat(formData.get("preco") as string),
        sha: "",
      });

      toast.success("Promoção enviada para validação!", {
        description:
          "Após validação da assinatura digital, será publicada na home.",
      });

      (e.currentTarget as HTMLFormElement).reset();
    } catch (error) {
      toast.error("Erro ao enviar promoção", {
        description: error instanceof Error ? error.message : "Tente novamente",
      });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <PageShell>
      <section className="mx-auto max-w-2xl rounded-3xl border border-slate-200 bg-card p-8 lg:p-12">
        <div className="mb-8 text-center">
          <h1 className="font-display text-3xl font-bold">Cadastrar Promoção</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Compartilhe um bom preço com a comunidade.
          </p>
        </div>
        <form onSubmit={onSubmit} className="space-y-6">

          <Field label="Nome da Promoção">
            <input
              required
              type="text"
              name="nome"
              placeholder="Ex: Smart TV Samsung 55 polegadas 4K"
              className={inputCls}
            />
          </Field>

          <Field label="E-mail da loja">
            <input
              required
              type="email"
              name="email"
              placeholder="contato@loja.com"
              className={inputCls}
            />
          </Field>

          <Field label="Preço">
            <div className="relative">
              <span className="absolute inset-y-0 left-4 flex items-center text-sm font-bold text-slate-400">
                R$
              </span>
              <input
                required
                type="number"
                step="0.01"
                min="0"
                name="preco"
                className={`${inputCls} pl-12`}
              />
            </div>
          </Field>

          <button
            type="submit"
            disabled={submitting}
            className="w-full rounded-2xl bg-navy py-4 font-bold text-white transition-all hover:opacity-90 active:scale-[0.98] disabled:opacity-60"
          >
            {submitting ? "Enviando..." : "Enviar Promoção"}
          </button>
          <p className="text-center text-xs text-muted-foreground">
            As mensagens são assinadas digitalmente. Apenas assinaturas válidas
            são publicadas pelo MS Promoção.
          </p>
        </form>
      </section>
    </PageShell>
  );
}

const inputCls =
  "w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm focus:border-brand-orange focus:outline-none focus:ring-1 focus:ring-brand-orange";

function Field({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-semibold text-slate-700">{label}</label>
      {children}
    </div>
  );
}
