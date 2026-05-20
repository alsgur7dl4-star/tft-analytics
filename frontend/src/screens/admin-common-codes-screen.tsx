"use client";

import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Plus, Trash2 } from "lucide-react";
import { addCode, createCodeGroup, deleteCode, deleteCodeGroup, getCodeGroups } from "@/api/tft";
import type { CommonCodeGroup } from "@/api/types";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export function AdminCommonCodesScreen() {
  const queryClient = useQueryClient();
  const { data: groups = [] } = useQuery({ queryKey: ["code-groups"], queryFn: getCodeGroups });

  const [newGroupKey, setNewGroupKey] = useState("");
  const [newGroupName, setNewGroupName] = useState("");
  const [newGroupDesc, setNewGroupDesc] = useState("");

  const createGroupMutation = useMutation({
    mutationFn: createCodeGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["code-groups"] });
      setNewGroupKey("");
      setNewGroupName("");
      setNewGroupDesc("");
    },
  });

  const deleteGroupMutation = useMutation({
    mutationFn: deleteCodeGroup,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["code-groups"] }),
  });

  function handleCreateGroup(event: React.FormEvent) {
    event.preventDefault();
    if (!newGroupKey.trim() || !newGroupName.trim()) return;
    createGroupMutation.mutate({
      group_key: newGroupKey.trim(),
      group_name: newGroupName.trim(),
      description: newGroupDesc.trim() || undefined,
    });
  }

  return (
    <ProtectedRoute>
      <div className="grid gap-6">
        <Card>
          <h1 className="text-2xl font-semibold">공통코드 관리</h1>
          <p className="mt-1 text-sm text-slate-600">코드 그룹과 코드 항목을 등록하고 관리합니다.</p>
          <form className="mt-5 grid gap-3 md:grid-cols-[1fr_1fr_1fr_auto]" onSubmit={handleCreateGroup}>
            <Input
              value={newGroupKey}
              onChange={(e) => setNewGroupKey(e.target.value)}
              placeholder="그룹 키 (예: TIER_LABEL)"
            />
            <Input
              value={newGroupName}
              onChange={(e) => setNewGroupName(e.target.value)}
              placeholder="그룹 이름 (예: 티어 라벨)"
            />
            <Input
              value={newGroupDesc}
              onChange={(e) => setNewGroupDesc(e.target.value)}
              placeholder="설명 (선택)"
            />
            <Button type="submit" disabled={createGroupMutation.isPending}>
              <Plus size={16} />
              그룹 추가
            </Button>
          </form>
        </Card>

        {groups.map((group) => (
          <CodeGroupCard
            key={group.group_key}
            group={group}
            onDeleteGroup={() => deleteGroupMutation.mutate(group.group_key)}
          />
        ))}
      </div>
    </ProtectedRoute>
  );
}

function CodeGroupCard({
  group,
  onDeleteGroup,
}: {
  group: CommonCodeGroup;
  onDeleteGroup: () => void;
}) {
  const queryClient = useQueryClient();
  const [code, setCode] = useState("");
  const [label, setLabel] = useState("");
  const [sortOrder, setSortOrder] = useState("0");

  const addCodeMutation = useMutation({
    mutationFn: ({ groupKey, body }: { groupKey: string; body: { code: string; label: string; sort_order: number } }) =>
      addCode(groupKey, body),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["code-groups"] });
      setCode("");
      setLabel("");
      setSortOrder("0");
    },
  });

  const deleteCodeMutation = useMutation({
    mutationFn: deleteCode,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["code-groups"] }),
  });

  function handleAddCode(event: React.FormEvent) {
    event.preventDefault();
    if (!code.trim() || !label.trim()) return;
    addCodeMutation.mutate({
      groupKey: group.group_key,
      body: { code: code.trim(), label: label.trim(), sort_order: Number(sortOrder) },
    });
  }

  return (
    <Card className="grid gap-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="font-semibold">{group.group_name}</p>
          <p className="font-mono text-sm text-teal-700">{group.group_key}</p>
          {group.description && <p className="mt-1 text-sm text-slate-500">{group.description}</p>}
        </div>
        <Button
          variant="ghost"
          className="text-red-500 hover:text-red-700"
          onClick={onDeleteGroup}
        >
          <Trash2 size={16} />
          그룹 삭제
        </Button>
      </div>

      <div className="rounded border border-slate-100">
        <div className="grid grid-cols-[80px_1fr_1fr_40px] gap-2 border-b border-slate-100 px-3 py-2 text-xs font-semibold text-slate-500">
          <span>순서</span>
          <span>코드</span>
          <span>라벨</span>
          <span />
        </div>
        {group.codes.length === 0 && (
          <p className="px-3 py-3 text-sm text-slate-400">코드가 없습니다.</p>
        )}
        {group.codes.map((c) => (
          <div
            key={c.id}
            className="grid grid-cols-[80px_1fr_1fr_40px] items-center gap-2 border-b border-slate-50 px-3 py-2 text-sm last:border-b-0"
          >
            <span className="text-slate-400">{c.sort_order}</span>
            <span className="font-mono">{c.code}</span>
            <span>{c.label}</span>
            <button
              type="button"
              className="text-red-400 hover:text-red-600"
              onClick={() => deleteCodeMutation.mutate(c.id)}
            >
              <Trash2 size={14} />
            </button>
          </div>
        ))}
      </div>

      <form className="grid gap-2 md:grid-cols-[60px_1fr_1fr_auto]" onSubmit={handleAddCode}>
        <Input
          value={sortOrder}
          onChange={(e) => setSortOrder(e.target.value)}
          placeholder="순서"
          type="number"
        />
        <Input value={code} onChange={(e) => setCode(e.target.value)} placeholder="코드 값 (예: S)" />
        <Input value={label} onChange={(e) => setLabel(e.target.value)} placeholder="라벨 (예: S티어)" />
        <Button type="submit" disabled={addCodeMutation.isPending}>
          <Plus size={16} />
          추가
        </Button>
      </form>
    </Card>
  );
}
