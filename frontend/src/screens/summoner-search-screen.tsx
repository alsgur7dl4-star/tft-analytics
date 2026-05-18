"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Search } from "lucide-react";
import { searchRiotAccount } from "@/api/tft";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export function SummonerSearchScreen() {
  const router = useRouter();
  const [gameName, setGameName] = useState("");
  const [tagLine, setTagLine] = useState("KR1");
  const [error, setError] = useState("");

  async function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError("");
    try {
      const account = await searchRiotAccount(gameName, tagLine);
      router.push(`/summoner/${account.puuid}`);
    } catch {
      setError("Riot 계정을 찾거나 수집하지 못했습니다.");
    }
  }

  return (
    <ProtectedRoute>
      <Card>
        <h1 className="text-2xl font-semibold">TFT 전적 조회</h1>
        <form className="mt-6 grid gap-3 sm:grid-cols-[1fr_160px_auto]" onSubmit={onSubmit}>
          <Input value={gameName} onChange={(event) => setGameName(event.target.value)} placeholder="Riot ID" />
          <Input value={tagLine} onChange={(event) => setTagLine(event.target.value)} placeholder="TagLine" />
          <Button type="submit">
            <Search size={17} />
            조회
          </Button>
        </form>
        {error ? <p className="mt-3 text-sm text-red-600">{error}</p> : null}
      </Card>
    </ProtectedRoute>
  );
}

