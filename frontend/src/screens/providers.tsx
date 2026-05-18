"use client";

import { QueryClient, QueryClientProvider as TanStackQueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";
import { AuthProvider } from "@/stores/auth-store";

export function QueryClientProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  return (
    <TanStackQueryClientProvider client={queryClient}>
      <AuthProvider>{children}</AuthProvider>
    </TanStackQueryClientProvider>
  );
}

