

import type { Metadata } from "next";
import { AuthProvider } from "@/contexts/AuthContext";
import { ThemeWrapper } from "@/components/ThemeWrapper";
import "./globals.css";

export const metadata: Metadata = {
  title: "DSPL Asset Pulse - Dashboard",
  description: "Asset management and monitoring system",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <ThemeWrapper>
          <AuthProvider>
            {children}
          </AuthProvider>
        </ThemeWrapper>
      </body>
    </html>
  );
}
