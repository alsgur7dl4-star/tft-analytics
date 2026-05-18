import { apiClient } from "@/api/client";
import type { CompStats, MatchSummary, RecommendationResult, SummonerSummary } from "@/api/types";

export async function searchRiotAccount(gameName: string, tagLine: string, region = "KR") {
  const { data } = await apiClient.get<{ game_name: string; tag_line: string; puuid: string; region: string }>(
    "/api/tft/accounts/search",
    { params: { game_name: gameName, tag_line: tagLine, region } }
  );
  return data;
}

export async function getSummoner(puuid: string) {
  const { data } = await apiClient.get<SummonerSummary>(`/api/tft/summoners/${puuid}`);
  return data;
}

export async function getSummonerMatches(puuid: string) {
  const { data } = await apiClient.get<MatchSummary[]>(`/api/tft/summoners/${puuid}/matches`);
  return data;
}

export async function getMetaComps() {
  const { data } = await apiClient.get<CompStats[]>("/api/tft/meta/comps");
  return data;
}

export async function getMetaComp(compId: string) {
  const { data } = await apiClient.get<CompStats>(`/api/tft/meta/comps/${compId}`);
  return data;
}

export async function recommendEarlyGame(payload: { units: string[]; items: string[]; augments: string[] }) {
  const { data } = await apiClient.post<RecommendationResult[]>("/api/tft/recommendations/early-game", payload);
  return data;
}

export async function recommendArtifacts(payload: { items: string[] }) {
  const { data } = await apiClient.post<RecommendationResult[]>("/api/tft/recommendations/artifacts", payload);
  return data;
}

export async function getJobRuns() {
  const { data } = await apiClient.get<Array<{ id: number; job_name: string; status: string; started_at: string; message?: string }>>(
    "/api/admin/jobs/runs"
  );
  return data;
}

export async function triggerStatsJob() {
  const { data } = await apiClient.post<{ job_run_id: number; status: string; message: string }>(
    "/api/admin/jobs/recalculate-tft-stats"
  );
  return data;
}

