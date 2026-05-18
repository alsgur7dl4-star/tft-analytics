import { CompDetailScreen } from "@/screens/comp-detail-screen";

export default async function Page({ params }: { params: Promise<{ compId: string }> }) {
  const { compId } = await params;
  return <CompDetailScreen compId={compId} />;
}

