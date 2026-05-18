"use client";

import { useQuery } from "@tanstack/react-query";
import { getMetaComp } from "@/api/tft";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { Card } from "@/components/ui/card";
import { percent } from "@/lib/utils";

export function CompDetailScreen({ compId }: { compId: string }) {
  const { data } = useQuery({ queryKey: ["meta-comp", compId], queryFn: () => getMetaComp(compId) });

  return (
    <ProtectedRoute>
      <Card>
        <p className="text-sm font-semibold text-teal-700">{data?.tier_label ?? "-"}</p>
        <h1 className="mt-2 text-2xl font-semibold">{data?.comp_name ?? "Composition"}</h1>
        <div className="mt-5 grid gap-3 md:grid-cols-4">
          <p>평균 등수 {data?.avg_placement.toFixed(2) ?? "-"}</p>
          <p>TOP4 {percent(data?.top4_rate)}</p>
          <p>1등 {percent(data?.first_rate)}</p>
          <p>픽률 {percent(data?.pick_rate)}</p>
        </div>
        <div className="mt-6 grid gap-4 md:grid-cols-3">
          <section>
            <h2 className="font-semibold">핵심 기물</h2>
            <p className="mt-2 text-sm text-slate-600">{data?.core_units.join(", ") || "-"}</p>
          </section>
          <section>
            <h2 className="font-semibold">핵심 시너지</h2>
            <p className="mt-2 text-sm text-slate-600">{data?.core_traits.join(", ") || "-"}</p>
          </section>
          <section>
            <h2 className="font-semibold">핵심 아이템</h2>
            <p className="mt-2 text-sm text-slate-600">{data?.core_items.join(", ") || "-"}</p>
          </section>
        </div>
      </Card>
    </ProtectedRoute>
  );
}

