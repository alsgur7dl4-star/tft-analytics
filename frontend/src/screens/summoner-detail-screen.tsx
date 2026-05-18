"use client";

import { useQuery } from "@tanstack/react-query";
import { getSummoner, getSummonerMatches } from "@/api/tft";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { Card } from "@/components/ui/card";
import { percent } from "@/lib/utils";

export function SummonerDetailScreen({ puuid }: { puuid: string }) {
  const { data: summary } = useQuery({ queryKey: ["summoner", puuid], queryFn: () => getSummoner(puuid) });
  const { data: matches = [] } = useQuery({ queryKey: ["summoner-matches", puuid], queryFn: () => getSummonerMatches(puuid), enabled: Boolean(summary) });

  return (
    <ProtectedRoute>
      <div className="grid gap-5">
        <Card>
          <h1 className="text-2xl font-semibold">
            {summary ? `${summary.game_name}#${summary.tag_line}` : "Summoner"}
          </h1>
          <div className="mt-4 grid gap-3 sm:grid-cols-4">
            <p className="text-sm text-slate-600">게임 {summary?.recent_matches ?? 0}</p>
            <p className="text-sm text-slate-600">평균 등수 {summary?.avg_placement?.toFixed(2) ?? "-"}</p>
            <p className="text-sm text-slate-600">TOP4 {percent(summary?.top4_rate)}</p>
            <p className="text-sm text-slate-600">1등 {percent(summary?.first_rate)}</p>
          </div>
        </Card>
        <div className="grid gap-3">
          {matches.map((match) => (
            <Card key={match.match_id}>
              <div className="flex flex-wrap items-center justify-between gap-3">
                <p className="font-medium">{match.match_id}</p>
                <p className="text-sm text-slate-500">{match.game_version ?? "-"}</p>
              </div>
              <div className="mt-3 grid gap-2 md:grid-cols-4">
                {match.participants.map((participant) => (
                  <div key={`${match.match_id}-${participant.puuid}`} className="rounded-md border border-slate-200 p-3 text-sm">
                    <p className="font-medium">{participant.placement}등</p>
                    <p className="mt-1 truncate text-slate-500">{participant.puuid}</p>
                  </div>
                ))}
              </div>
            </Card>
          ))}
        </div>
      </div>
    </ProtectedRoute>
  );
}

