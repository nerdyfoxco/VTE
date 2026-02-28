import ReactGA from "react-ga4";

// Replace with your actual GA4 Measurement ID
const GA_MEASUREMENT_ID = "G-XXXXXXXXXX";

export const initAnalytics = () => {
    // Only initialize if the user has consented to "all" cookies
    const consent = typeof window !== 'undefined' ? localStorage.getItem('vte_cookie_consent') : null;

    if (consent === 'all') {
        ReactGA.initialize(GA_MEASUREMENT_ID);
        console.log("Analytics Initialized (Privacy Consented)");
    } else {
        console.log("Analytics Disabled (Privacy Opt-Out / Essential Only)");
    }
};

export const trackPageView = (path: string) => {
    const consent = typeof window !== 'undefined' ? localStorage.getItem('vte_cookie_consent') : null;
    if (consent === 'all') {
        ReactGA.send({ hitType: "pageview", page: path });
    }
};

export const trackEvent = (category: string, action: string, label?: string, value?: number) => {
    const consent = typeof window !== 'undefined' ? localStorage.getItem('vte_cookie_consent') : null;
    if (consent === 'all') {
        ReactGA.event({
            category,
            action,
            label,
            value,
        });
    }
};
