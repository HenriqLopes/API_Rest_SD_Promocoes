import { Link } from "@tanstack/react-router";
import { Flame, Search } from "lucide-react";

const navItems: { to: "/" | "/minhas-categorias" | "/hot-deals" | "/categorias"; label: string; hot?: boolean }[] = [
  { to: "/", label: "Todas" },
  { to: "/minhas-categorias", label: "Minhas Categorias" },
  { to: "/hot-deals", label: "Hot Deals", hot: true },
  { to: "/categorias", label: "Categorias" },
];

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/90 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3">
        <div className="flex items-center gap-6">
          <Link to="/" className="flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-orange text-white">
              <Flame className="h-5 w-5" />
            </span>
            <span className="font-display text-2xl font-bold tracking-tight text-brand-orange">
              PROMOVALE
            </span>
          </Link>
          <nav className="hidden gap-1 md:flex">
            {navItems.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                className="rounded-full px-4 py-2 text-sm font-medium text-slate-500 hover:bg-slate-50"
                activeProps={{
                  className:
                    "rounded-full px-4 py-2 text-sm font-semibold bg-slate-100 text-slate-900",
                }}
                activeOptions={{ exact: true }}
              >
                {item.hot ? (
                  <span className="flex items-center gap-1.5">
                    <span className="h-2 w-2 rounded-full bg-brand-orange" />
                    {item.label}
                  </span>
                ) : (
                  item.label
                )}
              </Link>
            ))}
          </nav>
        </div>
        <div className="flex items-center gap-3">
          <div className="relative hidden lg:block">
            <Search className="pointer-events-none absolute inset-y-0 left-3 my-auto h-4 w-4 text-slate-400" />
            <input
              type="text"
              placeholder="Buscar ofertas..."
              className="w-64 rounded-xl border border-slate-200 bg-slate-50 py-2 pl-10 pr-4 text-sm focus:border-brand-orange focus:outline-none focus:ring-1 focus:ring-brand-orange"
            />
          </div>
          <Link
            to="/cadastrar"
            className="rounded-xl bg-brand-orange px-5 py-2 text-sm font-bold text-white transition-transform active:scale-95"
          >
            Cadastrar Loja
          </Link>
        </div>
      </div>
    </header>
  );
}
