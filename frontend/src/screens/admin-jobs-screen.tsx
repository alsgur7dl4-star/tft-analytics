"use client";

import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ChevronDown, ChevronRight, Play } from "lucide-react";
import { getJobLogs, getJobRuns, triggerStatsJob } from "@/api/tft";
import type { BatchJobLog } from "@/api/types";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

const LOG_LEVEL_COLOR: Record<string, string> = {
  INFO: "text-slate-600",
  WARN: "text-amber-600",
  ERROR: "text-red-600",
};

function JobLogPanel({ runId }: { runId: number }) {
  const { data: logs = [], isLoading } = useQuery({
    queryKey: ["job-logs", runId],
    queryFn: () => getJobLogs(runId),
  });

  if (isLoading) return <p className="mt-2 text-sm text-slate-400">로그 불러오는 중...</p>;
  if (!logs.length) return <p className="mt-2 text-sm text-slate-400">로그가 없습니다.</p>;

  return (
    <div className="mt-3 grid gap-1 rounded border border-slate-200 bg-slate-50 p-3">
      {logs.map((log: BatchJobLog) => (
        <div key={log.id} className="grid grid-cols-[60px_100px_1fr] gap-2 text-sm">
          <span className={`font-mono font-semibold ${LOG_LEVEL_COLOR[log.log_level] ?? "text-slate-600"}`}>
            {log.log_level}
          </span>
          <span className="text-slate-500">{log.step ?? "-"}</span>
          <span className="text-slate-700">{log.message}</span>
        </div>
      ))}
    </div>
  );
}

export function AdminJobsScreen() {
  const queryClient = useQueryClient();
  const { data = [] } = useQuery({ queryKey: ["job-runs"], queryFn: getJobRuns });
  const [expandedRunId, setExpandedRunId] = useState<number | null>(null);

  const mutation = useMutation({
    mutationFn: triggerStatsJob,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["job-runs"] }),
  });

  function toggleLog(runId: number) {
    setExpandedRunId((prev) => (prev === runId ? null : runId));
  }

  return (
    <ProtectedRoute>
      <div className="grid gap-5">
        <Card className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-2xl font-semibold">관리자 작업</h1>
            <p className="mt-1 text-sm text-slate-600">수집/집계 작업 실행 이력을 확인합니다.</p>
          </div>
          <Button onClick={() => mutation.mutate()} disabled={mutation.isPending}>
            <Play size={17} />
            통계 재계산
          </Button>
        </Card>
        <div className="grid gap-3">
          {data.map((run) => (
            <Card key={run.id} className="grid gap-2">
              <button
                type="button"
                className="grid cursor-pointer grid-cols-[24px_80px_1fr_120px_1fr] items-center gap-2 text-left"
                onClick={() => toggleLog(run.id)}
              >
                {expandedRunId === run.id ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                <p className="text-sm text-slate-400">#{run.id}</p>
                <p className="font-medium">{run.job_name}</p>
                <StatusBadge status={run.status} />
                <p className="truncate text-sm text-slate-500">{run.message ?? "-"}</p>
              </button>
              {expandedRunId === run.id && <JobLogPanel runId={run.id} />}
            </Card>
          ))}
        </div>
      </div>
    </ProtectedRoute>
  );
}

function StatusBadge({ status }: { status: string }) {
  const color =
    status === "SUCCESS"
      ? "text-teal-700"
      : status === "FAILED"
        ? "text-red-600"
        : status === "RUNNING"
          ? "text-blue-600"
          : "text-slate-500";
  return <p className={`text-sm font-semibold ${color}`}>{status}</p>;
}
