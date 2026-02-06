import React from 'react';
import Link from 'next/link';

interface BreadcrumbItem {
    label: string;
    href?: string;
}

interface BreadcrumbsProps {
    items: BreadcrumbItem[];
}

export default function Breadcrumbs({ items }: BreadcrumbsProps) {
    return (
        <nav className="flex" aria-label="Breadcrumb">
            <ol className="flex items-center space-x-4">
                {items.map((item, index) => (
                    <li key={index}>
                        <div className="flex items-center">
                            {index > 0 && (
                                <svg
                                    className="flex-shrink-0 h-5 w-5 text-gray-300"
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                    aria-hidden="true"
                                >
                                    <path d="M5.555 17.776l8-16 .894.448-8 16-.894-.448z" />
                                </svg>
                            )}
                            {item.href ? (
                                <Link
                                    href={item.href}
                                    className={`ml-4 text-sm font-medium text-gray-500 hover:text-gray-700 ${index === 0 ? 'ml-0' : ''}`}
                                >
                                    {item.label}
                                </Link>
                            ) : (
                                <span
                                    className={`ml-4 text-sm font-medium text-gray-500 ${index === 0 ? 'ml-0' : ''}`}
                                    aria-current="page"
                                >
                                    {item.label}
                                </span>
                            )}
                        </div>
                    </li>
                ))}
            </ol>
        </nav>
    );
}
