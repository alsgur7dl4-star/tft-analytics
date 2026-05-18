"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Play } from "lucide-react";
import { getJobRuns, triggerStatsJob } from "@/api/tft";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export function AdminJobsScreen() {
  const queryClient = useQueryClient();
  const { data = [] } = useQuery({ queryKey: ["job-runs"], queryFn: getJobRuns });
  const mutation = useMutation({
    mutationFn: triggerStatsJob,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["job-runs"] })
  });

  return (
    <ProtectedRoute>
      <div className="grid gap-5">
        <Card className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-2xl font-semibold">관리자 작업</h1>
            <p className="mt-1 text-sm text-slate-600">수집/집계 작업 실행 이력을 확인합니다.</p>
          </div>
          <Button onClick={() => mutation.mutate()}>
            <Play size={17} />
            통계 재계산
          </Button>
        </Card>
        <div className="grid gap-3">
          {data.map((run) => (
            <Card key={run.id} className="grid gap-2 md:grid-cols-[80px_1fr_120px_1fr]">
              <p>#{run.id}</p>
              <p className="font-medium">{run.job_name}</p>
              <p className="text-sm text-slate-600">{run.status}</p>
              <p className="text-sm text-slate-500">{run.message ?? "-"}</p>
            </Card>
          ))}
        </div>
      </div>
    </ProtectedRoute>
  );
}

