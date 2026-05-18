import { SummonerDetailScreen } from "@/screens/summoner-detail-screen";

export default async function Page({ params }: { params: Promise<{ puuid: string }> }) {
  const { puuid } = await params;
  return <SummonerDetailScreen puuid={puuid} />;
}

