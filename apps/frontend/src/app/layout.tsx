import "./globals.css";
import React from "react";
import Link from "next/link";
import Navbar from "../components/Navbar";

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
        <html lang="en">
            <body className="min-h-screen bg-gray-100 text-gray-900 font-sans">
                <Navbar />
                <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                    {children}
                </main>
            </body>
        </html>
    );
}
