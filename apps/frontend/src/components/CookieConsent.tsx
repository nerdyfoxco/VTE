"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';

export default function CookieConsent() {
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        // Check if consent is already given
        const consent = localStorage.getItem('vte_cookie_consent');
        if (!consent) {
            setIsVisible(true);
        }
    }, []);

    const handleAcceptAll = () => {
        localStorage.setItem('vte_cookie_consent', 'all');
        setIsVisible(false);
        window.dispatchEvent(new Event('vte_consent_updated'));
    };

    const handleEssentialOnly = () => {
        localStorage.setItem('vte_cookie_consent', 'essential');
        setIsVisible(false);
        window.dispatchEvent(new Event('vte_consent_updated'));
    };

    if (!isVisible) return null;

    return (
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg z-50 p-4 sm:p-6 flex flex-col sm:flex-row items-center justify-between gap-4 animate-fade-in-up">
            <div className="flex-1 text-sm text-gray-600">
                <p className="mb-2 font-semibold text-gray-900">We use cookies to improve your experience.</p>
                <p>
                    VTE uses essential cookies to ensure the site functions properly and analytics cookies to understand how you interact with it.
                    You can choose to accept all cookies or only the essential ones.
                    Read our <Link href="/privacy" className="text-indigo-600 hover:text-indigo-500 underline">Privacy Policy</Link> for more details.
                </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
                <button
                    onClick={handleEssentialOnly}
                    className="whitespace-nowrap px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                    Essential Only
                </button>
                <button
                    onClick={handleAcceptAll}
                    className="whitespace-nowrap px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                    Accept All
                </button>
            </div>
        </div>
    );
}
