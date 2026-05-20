"use client";

import Link from "next/link";
import { BarChart3, BriefcaseBusiness, LogOut, Search, ShieldCheck, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/stores/auth-store";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: BarChart3 },
  { href: "/summoner/search", label: "Summoner", icon: Search },
  { href: "/meta/comps", label: "Meta", icon: BriefcaseBusiness },
  { href: "/recommender/early-game", label: "Early Game", icon: Sparkles },
  { href: "/recommender/artifacts", label: "Artifacts", icon: ShieldCheck }
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuth();
  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
          <Link href="/dashboard" className="font-semibold tracking-normal text-slate-950">
            TFT Analytics
          </Link>
          <div className="flex items-center gap-3 text-sm text-slate-600">
            <span className="hidden sm:inline">{user?.nickname}</span>
            <Button variant="ghost" size="icon" onClick={logout} title="Logout">
              <LogOut size={18} />
            </Button>
          </div>
        </div>
      </header>
      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-6 px-4 py-6 md:grid-cols-[220px_1fr]">
        <nav className="flex gap-2 overflow-x-auto md:flex-col">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className="inline-flex h-10 shrink-0 items-center gap-2 rounded-md px-3 text-sm text-slate-700 hover:bg-white"
              >
                <Icon size={17} />
                {item.label}
              </Link>
            );
          })}
          {user?.role === "ADMIN" ? (
            <>
              <Link
                href="/admin/jobs"
                className="inline-flex h-10 shrink-0 items-center gap-2 rounded-md px-3 text-sm text-slate-700 hover:bg-white"
              >
                <ShieldCheck size={17} />
                Admin 작업
              </Link>
              <Link
                href="/admin/codes"
                className="inline-flex h-10 shrink-0 items-center gap-2 rounded-md px-3 text-sm text-slate-700 hover:bg-white"
              >
                <ShieldCheck size={17} />
                공통코드
              </Link>
            </>
          ) : null}
        </nav>
        <main>{children}</main>
      </div>
    </div>
  );
}

