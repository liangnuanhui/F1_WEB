import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "@/components/providers/Providers";
import { Header } from "@/components/layout/Header";

export const metadata: Metadata = {
  title: "F1 赛事数据",
  description:
    "F1 一级方程式赛车赛事数据网站，提供赛程、车手、车队、赛道和积分榜信息",
  keywords: "F1, 一级方程式, 赛车, 赛程, 车手, 车队, 积分榜",
  authors: [{ name: "F1 Data Team" }],
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN" suppressHydrationWarning>
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Titillium+Web:wght@400;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="font-sans antialiased">
        <Providers>
          <div className="min-h-screen bg-background">
            <Header />
            <main>{children}</main>
          </div>
        </Providers>
      </body>
    </html>
  );
}
