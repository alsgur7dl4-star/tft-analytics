import { apiClient } from "@/api/client";
import type { TokenResponse, User } from "@/api/types";

export async function register(payload: { email: string; password: string; nickname: string }) {
  const { data } = await apiClient.post<TokenResponse>("/api/auth/register", payload);
  return data;
}

export async function login(payload: { email: string; password: string }) {
  const { data } = await apiClient.post<TokenResponse>("/api/auth/login", payload);
  return data;
}

export async function refresh() {
  const { data } = await apiClient.post<TokenResponse>("/api/auth/refresh");
  return data;
}

export async function logout() {
  await apiClient.post("/api/auth/logout");
}

export async function me() {
  const { data } = await apiClient.get<User>("/api/auth/me");
  return data;
}

