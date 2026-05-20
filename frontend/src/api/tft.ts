import { apiClient } from "@/api/client";
import type { BatchJobLog, CommonCodeGroup, CompStats, MatchSummary, RecommendationResult, SummonerSummary } from "@/api/types";

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

export async function getJobLogs(runId: number) {
  const { data } = await apiClient.get<BatchJobLog[]>(`/api/admin/jobs/runs/${runId}/logs`);
  return data;
}

export async function getCodeGroups() {
  const { data } = await apiClient.get<CommonCodeGroup[]>("/api/admin/codes/groups");
  return data;
}

export async function createCodeGroup(body: { group_key: string; group_name: string; description?: string }) {
  const { data } = await apiClient.post<CommonCodeGroup>("/api/admin/codes/groups", body);
  return data;
}

export async function deleteCodeGroup(groupKey: string) {
  await apiClient.delete(`/api/admin/codes/groups/${groupKey}`);
}

export async function addCode(groupKey: string, body: { code: string; label: string; sort_order?: number }) {
  const { data } = await apiClient.post<{ id: number; code: string; label: string; sort_order: number }>(
    `/api/admin/codes/groups/${groupKey}/codes`,
    body
  );
  return data;
}

export async function deleteCode(codeId: number) {
  await apiClient.delete(`/api/admin/codes/${codeId}`);
}

