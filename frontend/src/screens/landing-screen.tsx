import Link from "next/link";
import { ArrowRight, Search, Sparkles, Trophy } from "lucide-react";
import { Button } from "@/components/ui/button";

export function LandingScreen() {
  return (
    <main className="min-h-screen bg-white">
      <section className="mx-auto grid min-h-[82vh] max-w-7xl content-center gap-10 px-4 py-12 lg:grid-cols-[1.05fr_0.95fr]">
        <div className="flex flex-col justify-center">
          <p className="text-sm font-semibold uppercase text-teal-700">TFT Analytics</p>
          <h1 className="mt-4 max-w-3xl text-4xl font-bold leading-tight text-slate-950 sm:text-5xl">
            TFT 전적 조회와 추천 조합 분석
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-7 text-slate-600">
            Riot API로 수집한 전적을 기반으로 최근 성적, 메타 조합 티어, 2-1 보유 기물 및 유물/아이템 기반 추천 덱을 제공합니다.
          </p>
          <div className="mt-7 flex flex-wrap gap-3">
            <Button asChild>
              <Link href="/login">
                로그인 <ArrowRight size={17} />
              </Link>
            </Button>
            <Button asChild variant="secondary">
              <Link href="/register">회원가입</Link>
            </Button>
          </div>
        </div>
        <div className="grid content-center gap-3">
          {[
            { icon: Search, title: "전적 조회", body: "Riot ID와 TagLine으로 최근 매치와 참가자 정보를 확인합니다." },
            { icon: Trophy, title: "메타 티어", body: "평균 등수, TOP4 비율, 1등 비율, 픽률을 함께 반영합니다." },
            { icon: Sparkles, title: "추천 조합", body: "보유 기물과 아이템 방향성에 맞는 덱을 순위로 보여줍니다." }
          ].map((item) => {
            const Icon = item.icon;
            return (
              <div key={item.title} className="rounded-lg border border-slate-200 bg-slate-50 p-5">
                <Icon className="text-teal-700" size={22} />
                <h2 className="mt-3 text-lg font-semibold">{item.title}</h2>
                <p className="mt-2 text-sm leading-6 text-slate-600">{item.body}</p>
              </div>
            );
          })}
        </div>
      </section>
    </main>
  );
}

