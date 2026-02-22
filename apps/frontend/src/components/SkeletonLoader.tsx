import React from 'react';

export default function SkeletonLoader() {
    return (
        <div className="animate-pulse">
            <div className="bg-white shadow overflow-hidden sm:rounded-md mb-6">
                <ul role="list" className="divide-y divide-gray-200">
                    {[1, 2, 3, 4, 5].map((i) => (
                        <li key={i} className="px-4 py-4 sm:px-6">
                            <div className="flex items-center justify-between">
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center justify-between mb-2">
                                        <div className="h-4 bg-gray-200 rounded w-1/3"></div>
                                        <div className="h-4 bg-gray-200 rounded w-16"></div>
                                    </div>
                                    <div className="flex justify-between">
                                        <div className="h-3 bg-gray-200 rounded w-1/4"></div>
                                        <div className="h-3 bg-gray-200 rounded w-1/4"></div>
                                    </div>
                                </div>
                                <div className="ml-5 flex-shrink-0">
                                    <div className="h-8 w-20 bg-gray-200 rounded"></div>
                                </div>
                            </div>
                        </li>
                    ))}
                </ul>
            </div>

            {/* Pagination Skeleton */}
            <div className="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6 shadow sm:rounded-md">
                <div className="flex-1 flex justify-between sm:hidden">
                    <div className="h-8 w-20 bg-gray-200 rounded"></div>
                    <div className="h-8 w-20 bg-gray-200 rounded"></div>
                </div>
                <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
                    <div className="h-4 bg-gray-200 rounded w-32"></div>
                    <div className="flex gap-2">
                        <div className="h-8 w-8 bg-gray-200 rounded"></div>
                        <div className="h-8 w-8 bg-gray-200 rounded"></div>
                    </div>
                </div>
            </div>
        </div>
    );
}
