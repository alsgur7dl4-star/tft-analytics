import type { Metadata } from "next";
import { QueryClientProvider } from "@/screens/providers";
import "@/styles/global.css";

export const metadata: Metadata = {
  title: "TFT Analytics",
  description: "TFT match lookup and recommendation analytics"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ko">
      <body>
        <QueryClientProvider>{children}</QueryClientProvider>
      </body>
    </html>
  );
}

