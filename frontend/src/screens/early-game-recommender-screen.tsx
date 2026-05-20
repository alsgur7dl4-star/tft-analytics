"use client";

import { useEffect, useState } from "react";
import { Sparkles } from "lucide-react";
import { getMetaGods, recommendEarlyGame, recommendArtifacts } from "@/api/tft";
import type { God, RecommendationResult } from "@/api/types";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { percent } from "@/lib/utils";

const DIFFICULTY_LABEL: Record<string, string> = {
  EASY: "쉬움",
  MEDIUM: "보통",
  HIGH: "어려움",
};

const DIFFICULTY_COLOR: Record<string, string> = {
  EASY: "text-emerald-600 bg-emerald-50",
  MEDIUM: "text-amber-600 bg-amber-50",
  HIGH: "text-red-600 bg-red-50",
};

const TIER_COLOR: Record<string, string> = {
  S: "text-yellow-700 bg-yellow-50",
  A: "text-orange-600 bg-orange-50",
  B: "text-blue-600 bg-blue-50",
  C: "text-slate-600 bg-slate-100",
  D: "text-slate-400 bg-slate-50",
};

export function EarlyGameRecommenderScreen() {
  const [units, setUnits] = useState("");
  const [items, setItems] = useState("");
  const [augments, setAugments] = useState("");
  const [selectedGods, setSelectedGods] = useState<string[]>([]);
  const [gods, setGods] = useState<God[]>([]);
  const [results, setResults] = useState<RecommendationResult[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getMetaGods().then(setGods).catch(() => setGods([]));
  }, []);

  function toggleGod(godKey: string) {
    setSelectedGods((prev) =>
      prev.includes(godKey) ? prev.filter((g) => g !== godKey) : [...prev, godKey]
    );
  }

  async function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await recommendEarlyGame({
        units: splitInput(units),
        items: splitInput(items),
        augments: splitInput(augments),
        gods: selectedGods,
      });
      setResults(data);
    } catch {
      setError("추천 계산에 실패했습니다. 보유 기물은 3~8개를 입력해주세요.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <ProtectedRoute>
      <div className="grid gap-5">
        <Card>
          <h1 className="text-2xl font-semibold">2-1 보유 기물 추천</h1>
          <form className="mt-5 grid gap-3" onSubmit={onSubmit}>
            <Input value={units} onChange={(e) => setUnits(e.target.value)} placeholder="보유 기물 3~8개, 쉼표로 구분" />
            <Input value={items} onChange={(e) => setItems(e.target.value)} placeholder="아이템 (쉼표로 구분)" />
            <Input value={augments} onChange={(e) => setAugments(e.target.value)} placeholder="증강체 (쉼표로 구분)" />
            {gods.length > 0 && (
              <div>
                <p className="mb-1.5 text-sm text-slate-600">신(God) 선택</p>
                <div className="flex flex-wrap gap-2">
                  {gods.map((god) => {
                    const active = selectedGods.includes(god.god_key);
                    return (
                      <button
                        key={god.god_key}
                        type="button"
                        onClick={() => toggleGod(god.god_key)}
                        className={`rounded-full border px-3 py-1 text-sm transition-colors ${
                          active
                            ? "border-purple-500 bg-purple-100 text-purple-700"
                            : "border-slate-200 bg-white text-slate-600 hover:border-purple-300"
                        }`}
                      >
                        {god.god_name}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
            {error ? <p className="text-sm text-red-600">{error}</p> : null}
            <Button type="submit" className="w-fit" disabled={loading}>
              <Sparkles size={17} />
              {loading ? "계산 중…" : "추천 보기"}
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
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await recommendArtifacts({ items: splitInput(items) });
      setResults(data);
    } catch {
      setError("추천 계산에 실패했습니다. 유물/아이템은 최대 4개까지 입력해주세요.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <ProtectedRoute>
      <div className="grid gap-5">
        <Card>
          <h1 className="text-2xl font-semibold">유물/아이템 추천</h1>
          <form className="mt-5 grid gap-3" onSubmit={onSubmit}>
            <Input value={items} onChange={(e) => setItems(e.target.value)} placeholder="유물/아이템 최대 4개, 쉼표로 구분" />
            {error ? <p className="text-sm text-red-600">{error}</p> : null}
            <Button type="submit" className="w-fit" disabled={loading}>
              <Sparkles size={17} />
              {loading ? "계산 중…" : "추천 보기"}
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
        <ResultCard key={`${result.rank}-${result.comp_id}`} result={result} />
      ))}
    </div>
  );
}

function ResultCard({ result }: { result: RecommendationResult }) {
  const tierColor = result.tier_label ? (TIER_COLOR[result.tier_label] ?? "text-slate-500 bg-slate-50") : null;
  const diffColor = DIFFICULTY_COLOR[result.difficulty] ?? "text-slate-500 bg-slate-50";
  const diffLabel = DIFFICULTY_LABEL[result.difficulty] ?? result.difficulty;

  return (
    <Card>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="flex items-baseline gap-3">
          <span className="text-xl font-semibold text-teal-700">#{result.rank}</span>
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <span className="font-semibold">{result.comp_name}</span>
              {tierColor && (
                <span className={`rounded px-1.5 py-0.5 text-xs font-medium ${tierColor}`}>{result.tier_label}</span>
              )}
              <span className={`rounded px-1.5 py-0.5 text-xs font-medium ${diffColor}`}>{diffLabel}</span>
              {result.god_match && (
                <span className="rounded bg-purple-100 px-1.5 py-0.5 text-xs font-medium text-purple-700">신 일치</span>
              )}
            </div>
            <p className="mt-0.5 text-sm text-slate-500">{result.reason}</p>
          </div>
        </div>
        <span className="text-sm text-slate-500">점수 {result.score.toFixed(3)}</span>
      </div>

      {result.core_units.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1">
          {result.core_units.map((unit) => (
            <span key={unit} className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-700">{unit}</span>
          ))}
        </div>
      )}

      {result.god_match && result.preferred_gods.length > 0 && (
        <p className="mt-2 text-xs text-purple-600">선호 신: {result.preferred_gods.join(" · ")}</p>
      )}

      <div className="mt-3 flex flex-wrap gap-4 text-sm text-slate-600">
        <span>TOP4 {percent(result.top4_rate)}</span>
        <span>1등 {percent(result.first_rate)}</span>
        <span>픽률 {percent(result.pick_rate)}</span>
        {result.matching_rate != null && (
          <span>기물일치 {percent(result.matching_rate)}</span>
        )}
        {result.synergy_score != null && (
          <span>시너지 {percent(result.synergy_score)}</span>
        )}
      </div>
    </Card>
  );
}

function splitInput(value: string) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}
