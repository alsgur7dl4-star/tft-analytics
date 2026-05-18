"use client";

import Link from "next/link";
import { useState } from "react";
import { LogIn } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/stores/auth-store";

export function LoginScreen() {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError("");
    try {
      await login(email, password);
    } catch {
      setError("로그인에 실패했습니다.");
    }
  }

  return (
    <main className="grid min-h-screen place-items-center px-4">
      <Card className="w-full max-w-md">
        <h1 className="text-2xl font-semibold">로그인</h1>
        <form className="mt-6 grid gap-4" onSubmit={onSubmit}>
          <Input value={email} onChange={(event) => setEmail(event.target.value)} placeholder="email@example.com" type="email" />
          <Input value={password} onChange={(event) => setPassword(event.target.value)} placeholder="password" type="password" />
          {error ? <p className="text-sm text-red-600">{error}</p> : null}
          <Button type="submit">
            <LogIn size={17} />
            로그인
          </Button>
        </form>
        <p className="mt-4 text-sm text-slate-600">
          계정이 없나요? <Link className="font-medium text-teal-700" href="/register">회원가입</Link>
        </p>
      </Card>
    </main>
  );
}

