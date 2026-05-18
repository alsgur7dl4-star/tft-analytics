"use client";

import { useState } from "react";
import { Sparkles } from "lucide-react";
import { recommendEarlyGame } from "@/api/tft";
import type { RecommendationResult } from "@/api/types";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { percent } from "@/lib/utils";

export function EarlyGameRecommenderScreen() {
  const [units, setUnits] = useState("");
  const [items, setItems] = useState("");
  const [augments, setAugments] = useState("");
  const [results, setResults] = useState<RecommendationResult[]>([]);
  const [error, setError] = useState("");

  async function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError("");
    try {
      const data = await recommendEarlyGame({
        units: splitInput(units),
        items: splitInput(items),
        augments: splitInput(augments)
      });
      setResults(data);
    } catch {
      setError("추천 계산에 실패했습니다. 보유 기물은 3~8개를 입력해주세요.");
    }
  }

  return (
    <ProtectedRoute>
      <div className="grid gap-5">
        <Card>
          <h1 className="text-2xl font-semibold">2-1 보유 기물 추천</h1>
          <form className="mt-5 grid gap-3" onSubmit={onSubmit}>
            <Input value={units} onChange={(event) => setUnits(event.target.value)} placeholder="보유 기물 3~8개, 쉼표로 구분" />
            <Input value={items} onChange={(event) => setItems(event.target.value)} placeholder="선택 아이템" />
            <Input value={augments} onChange={(event) => setAugments(event.target.value)} placeholder="선택 증강/유물" />
            {error ? <p className="text-sm text-red-600">{error}</p> : null}
            <Button type="submit" className="w-fit">
              <Sparkles size={17} />
              추천 보기
            </Button>
          </form>
        </Card>
        <RecommendationList results={results} />
      </div>
    </ProtectedRoute>
  );
}

export function ArtifactRecommenderScreen() {
  const [items, setItems] = useState("");
  const [results, setResults] = useState<RecommendationResult[]>([]);
  const [error, setError] = useState("");

  async function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError("");
    try {
      const data = await import("@/api/tft").then((api) => api.recommendArtifacts({ items: splitInput(items) }));
      setResults(data);
    } catch {
      setError("추천 계산에 실패했습니다. 유물/아이템은 최대 4개까지 입력해주세요.");
    }
  }

  return (
    <ProtectedRoute>
      <div className="grid gap-5">
        <Card>
          <h1 className="text-2xl font-semibold">유물/아이템 추천</h1>
          <form className="mt-5 grid gap-3" onSubmit={onSubmit}>
            <Input value={items} onChange={(event) => setItems(event.target.value)} placeholder="유물/아이템 최대 4개, 쉼표로 구분" />
            {error ? <p className="text-sm text-red-600">{error}</p> : null}
            <Button type="submit" className="w-fit">
              <Sparkles size={17} />
              추천 보기
            </Button>
          </form>
        </Card>
        <RecommendationList results={results} />
      </div>
    </ProtectedRoute>
  );
}

function RecommendationList({ results }: { results: RecommendationResult[] }) {
  if (!results.length) return null;
  return (
    <div className="grid gap-3">
      {results.map((result) => (
        <Card key={`${result.rank}-${result.comp_id}`}>
          <div className="grid gap-3 md:grid-cols-[70px_1fr_repeat(4,110px)]">
            <p className="text-xl font-semibold text-teal-700">#{result.rank}</p>
            <div>
              <p className="font-semibold">{result.comp_name}</p>
              <p className="mt-1 text-sm text-slate-500">{result.reason}</p>
            </div>
            <p className="text-sm">점수 {result.score.toFixed(3)}</p>
            <p className="text-sm">TOP4 {percent(result.top4_rate)}</p>
            <p className="text-sm">1등 {percent(result.first_rate)}</p>
            <p className="text-sm">픽률 {percent(result.pick_rate)}</p>
          </div>
        </Card>
      ))}
    </div>
  );
}

function splitInput(value: string) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

