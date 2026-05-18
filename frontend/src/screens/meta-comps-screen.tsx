"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { getMetaComps } from "@/api/tft";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { Card } from "@/components/ui/card";
import { percent } from "@/lib/utils";

export function MetaCompsScreen() {
  const { data = [] } = useQuery({ queryKey: ["meta-comps"], queryFn: getMetaComps });

  return (
    <ProtectedRoute>
      <div className="grid gap-4">
        <h1 className="text-2xl font-semibold">메타 조합 티어</h1>
        {data.map((comp) => (
          <Link key={comp.comp_id} href={`/meta/comps/${comp.comp_id}`}>
            <Card className="grid gap-3 hover:border-teal-700 md:grid-cols-[80px_1fr_repeat(4,110px)]">
              <p className="text-xl font-semibold text-teal-700">{comp.tier_label}</p>
              <div>
                <p className="font-semibold">{comp.comp_name}</p>
                <p className="mt-1 text-sm text-slate-500">{comp.core_units.join(", ") || "Core units pending"}</p>
              </div>
              <p className="text-sm">평균 {comp.avg_placement.toFixed(2)}</p>
              <p className="text-sm">TOP4 {percent(comp.top4_rate)}</p>
              <p className="text-sm">1등 {percent(comp.first_rate)}</p>
              <p className="text-sm">픽률 {percent(comp.pick_rate)}</p>
            </Card>
          </Link>
        ))}
      </div>
    </ProtectedRoute>
  );
}

