"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { login as apiLogin, logout as apiLogout, me, refresh, register as apiRegister } from "@/api/auth";
import { setAccessToken } from "@/api/client";
import type { User } from "@/api/types";

type AuthContextValue = {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, nickname: string) => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    async function boot() {
      try {
        const token = await refresh();
        setAccessToken(token.access_token);
        const current = await me();
        if (mounted) setUser(current);
      } catch {
        setAccessToken(null);
        if (mounted) setUser(null);
      } finally {
        if (mounted) setIsLoading(false);
      }
    }
    boot();
    return () => {
      mounted = false;
    };
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isLoading,
      async login(email, password) {
        const token = await apiLogin({ email, password });
        setAccessToken(token.access_token);
        setUser(await me());
        router.push("/dashboard");
      },
      async register(email, password, nickname) {
        const token = await apiRegister({ email, password, nickname });
        setAccessToken(token.access_token);
        setUser(await me());
        router.push("/dashboard");
      },
      async logout() {
        await apiLogout();
        setAccessToken(null);
        setUser(null);
        router.push("/login");
      }
    }),
    [isLoading, router, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}

