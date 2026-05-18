"use client";

import Link from "next/link";
import { useState } from "react";
import { UserPlus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/stores/auth-store";

export function RegisterScreen() {
  const { register } = useAuth();
  const [email, setEmail] = useState("");
  const [nickname, setNickname] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError("");
    try {
      await register(email, password, nickname);
    } catch {
      setError("회원가입에 실패했습니다.");
    }
  }

  return (
    <main className="grid min-h-screen place-items-center px-4">
      <Card className="w-full max-w-md">
        <h1 className="text-2xl font-semibold">회원가입</h1>
        <form className="mt-6 grid gap-4" onSubmit={onSubmit}>
          <Input value={email} onChange={(event) => setEmail(event.target.value)} placeholder="email@example.com" type="email" />
          <Input value={nickname} onChange={(event) => setNickname(event.target.value)} placeholder="nickname" />
          <Input value={password} onChange={(event) => setPassword(event.target.value)} placeholder="8자 이상 password" type="password" />
          {error ? <p className="text-sm text-red-600">{error}</p> : null}
          <Button type="submit">
            <UserPlus size={17} />
            계정 만들기
          </Button>
        </form>
        <p className="mt-4 text-sm text-slate-600">
          이미 계정이 있나요? <Link className="font-medium text-teal-700" href="/login">로그인</Link>
        </p>
      </Card>
    </main>
  );
}

