import { createFileRoute } from "@tanstack/react-router";
import { useState, type FormEvent } from "react";
import { PageShell } from "@/components/page-shell";
import { criarPromocao } from "@/lib/api/gateway";
import { CATEGORIES, CATEGORY_NAME_TO_ID, type Category } from "@/lib/mock-data";
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

    const formData = new FormData(e.currentTarget);
    const categoriaNome = formData.get("categoria") as Category;

    await criarPromocao({
      nome: formData.get("nome") as string,
      email: formData.get("email") as string,
      preco: parseFloat(formData.get("preco") as string),
      categoria: CATEGORY_NAME_TO_ID[categoriaNome],
      sha: "",
    });

    toast.success("Promoção enviada!");
    (e.currentTarget as HTMLFormElement).reset();
    setSubmitting(false);
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

          <Field label="Categoria">
            <select required name="categoria" className={inputCls}>
              <option value="">Selecione uma categoria</option>
              {CATEGORIES.map((cat) => (
                <option key={cat.id} value={cat.name}>
                  {cat.emoji} {cat.name}
                </option>
              ))}
            </select>
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
            className="w-full rounded-2xl bg-navy py-4 font-bold text-white"
          >
            {submitting ? "Enviando..." : "Enviar Promoção"}
          </button>
        </form>
      </section>
    </PageShell>
  );
}

const inputCls =
  "w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm focus:border-brand-orange focus:outline-none focus:ring-1 focus:ring-brand-orange";

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-semibold text-slate-700">{label}</label>
      {children}
    </div>
  );
}
