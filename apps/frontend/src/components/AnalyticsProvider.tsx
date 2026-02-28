"use client";

import { useEffect, Suspense } from "react";
import { usePathname, useSearchParams } from "next/navigation";
import { useReportWebVitals } from "next/web-vitals";
import { initAnalytics, trackPageView, trackEvent } from "@/lib/analytics";

function AnalyticsTracker() {
    const pathname = usePathname();
    const searchParams = useSearchParams();

    // Initialize on mount
    useEffect(() => {
        initAnalytics();

        // Listen for custom re-init event from the CookieConsent component
        const handleConsentUpdate = () => {
            initAnalytics();
            if (pathname) {
                trackPageView(pathname);
            }
        };

        window.addEventListener('vte_consent_updated', handleConsentUpdate);
        return () => window.removeEventListener('vte_consent_updated', handleConsentUpdate);
    }, [pathname]);

    // Track page views on route change
    useEffect(() => {
        if (pathname) {
            const url = pathname + (searchParams?.toString() ? `?${searchParams.toString()}` : "");
            trackPageView(url);
        }
    }, [pathname, searchParams]);

    // Track Web Vitals
    useReportWebVitals((metric) => {
        trackEvent("Web Vitals", metric.name, metric.id, Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value));
    });

    return null;
}

export default function AnalyticsProvider({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <>
            <Suspense fallback={null}>
                <AnalyticsTracker />
            </Suspense>
            {children}
        </>
    );
}
