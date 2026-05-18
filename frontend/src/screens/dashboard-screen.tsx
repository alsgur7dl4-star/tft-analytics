"use client";

import { useQuery } from "@tanstack/react-query";
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Card } from "@/components/ui/card";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { getMetaComps } from "@/api/tft";
import { percent } from "@/lib/utils";

export function DashboardScreen() {
  const { data = [] } = useQuery({ queryKey: ["meta-comps"], queryFn: getMetaComps });
  const chartData = data.slice(0, 8).map((comp) => ({ name: comp.comp_name, top4: Math.round(comp.top4_rate * 100) }));

  return (
    <ProtectedRoute>
      <div className="grid gap-6">
        <div>
          <h1 className="text-2xl font-semibold">Dashboard</h1>
          <p className="mt-1 text-sm text-slate-600">수집된 데이터를 바탕으로 전적과 메타 흐름을 확인합니다.</p>
        </div>
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <p className="text-sm text-slate-500">Tracked Comps</p>
            <p className="mt-2 text-3xl font-semibold">{data.length}</p>
          </Card>
          <Card>
            <p className="text-sm text-slate-500">Best TOP4</p>
            <p className="mt-2 text-3xl font-semibold">{percent(data[0]?.top4_rate)}</p>
          </Card>
          <Card>
            <p className="text-sm text-slate-500">Best Tier</p>
            <p className="mt-2 text-3xl font-semibold">{data[0]?.tier_label ?? "-"}</p>
          </Card>
        </div>
        <Card className="h-[320px]">
          <h2 className="mb-4 text-lg font-semibold">Top Comps TOP4 Rate</h2>
          <ResponsiveContainer width="100%" height="85%">
            <BarChart data={chartData}>
              <XAxis dataKey="name" hide />
              <YAxis />
              <Tooltip />
              <Bar dataKey="top4" fill="#0f766e" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>
    </ProtectedRoute>
  );
}

