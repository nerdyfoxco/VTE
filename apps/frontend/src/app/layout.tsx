import "./globals.css";
import React from "react";
import { AppLayout } from "@/components/layout/app-layout";
import AnalyticsProvider from "@/components/AnalyticsProvider";
import { ErrorBoundary } from "@/components/ErrorBoundary";

export const metadata = {
    title: "VTE Control Plane",
    description: "Verified Transaction Execution",
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en" suppressHydrationWarning>
            <body className="min-h-screen font-sans antialiased" suppressHydrationWarning>
                <ErrorBoundary>
                    <AnalyticsProvider>
                        <AppLayout>
                            {children}
                        </AppLayout>
                    </AnalyticsProvider>
                </ErrorBoundary>
            </body>
        </html>
    );
}
