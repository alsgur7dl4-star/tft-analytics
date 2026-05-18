export type User = {
  id: number;
  email: string;
  nickname: string;
  role: "USER" | "ADMIN";
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
};

export type CompStats = {
  comp_id: number;
  comp_name: string;
  tier_label: string;
  score: number;
  games: number;
  avg_placement: number;
  top4_rate: number;
  first_rate: number;
  pick_rate: number;
  core_units: string[];
  core_traits: string[];
  core_items: string[];
};

export type RecommendationResult = {
  rank: number;
  comp_id: number;
  comp_name: string;
  score: number;
  tier_label?: string | null;
  core_units: string[];
  final_comp: string[];
  matching_rate?: number | null;
  synergy_score?: number | null;
  avg_placement?: number | null;
  top4_rate?: number | null;
  first_rate?: number | null;
  pick_rate?: number | null;
  difficulty: string;
  reason: string;
};

export type SummonerSummary = {
  puuid: string;
  game_name: string;
  tag_line: string;
  region: string;
  recent_matches: number;
  avg_placement?: number | null;
  top4_rate?: number | null;
  first_rate?: number | null;
};

export type MatchSummary = {
  match_id: string;
  game_version?: string | null;
  game_datetime?: string | null;
  queue_id?: number | null;
  participants: Array<{
    puuid: string;
    placement: number;
    level?: number | null;
    traits: unknown[];
    units: unknown[];
    augments: unknown[];
  }>;
};

