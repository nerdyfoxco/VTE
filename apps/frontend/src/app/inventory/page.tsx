"use client";
export const dynamic = 'force-dynamic';

import { useEffect, useState, Fragment } from 'react';
import axios from 'axios';
import { Dialog, Transition } from '@headlessui/react';
import {
    HomeIcon,
    UserIcon,
    ClipboardDocumentListIcon,
    CheckCircleIcon,
    ExclamationCircleIcon
} from '@heroicons/react/24/outline';

// --- Types ---
interface Unit {
    unit_id: string;
    name: string;
    status: "VACANT" | "OCCUPIED" | "MAINTENANCE";
    tenant_info?: {
        name: string;
        source: string;
    };
}

interface Property {
    property_id: string;
    name: string;
    address: string;
    units: Unit[];
}

// --- Components ---

const StatusBadge = ({ status }: { status: string }) => {
    const styles = {
        OCCUPIED: "bg-green-100 text-green-800",
        VACANT: "bg-gray-100 text-gray-800",
        MAINTENANCE: "bg-yellow-100 text-yellow-800"
    };
    const style = styles[status as keyof typeof styles] || "bg-gray-100 text-gray-800";

    return (
        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${style}`}>
            {status}
        </span>
    );
};

export default function InventoryPage() {
    const [properties, setProperties] = useState<Property[]>([]);
    const [loading, setLoading] = useState(true);
    const [newPropName, setNewPropName] = useState("");

    // Modal State
    const [selectedUnit, setSelectedUnit] = useState<Unit | null>(null);
    const [noteContent, setNoteContent] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    // Add Unit Modal State
    const [isAddUnitOpen, setIsAddUnitOpen] = useState(false);
    const [targetPropertyId, setTargetPropertyId] = useState<string | null>(null);
    const [newUnitName, setNewUnitName] = useState("");

    // Fetch Data
    const fetchInventory = async () => {
        try {
            const token = localStorage.getItem('access_token');
            const res = await axios.get('http://localhost:8000/api/v1/inventory/properties', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setProperties(res.data);
            setLoading(false);
        } catch (e) {
            console.error("Failed to fetch inventory", e);
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchInventory();
    }, []);

    // Action: Register Property
    const handleRegisterProperty = async () => {
        if (!newPropName) return;
        try {
            const token = localStorage.getItem('access_token');
            const payload = {
                actor: { user_id: "ui_user", role: "user" },
                intent: {
                    action: "REGISTER_PROPERTY",
                    target_resource: "auto-gen",
                    parameters: { name: newPropName, address: "TBD Address" }
                },
                evidence_hash: null,
                outcome: "PROPOSED",
                policy_version: "1.0"
            };

            await axios.post('http://localhost:8000/api/v1/decisions', payload, {
                headers: { Authorization: `Bearer ${token}` }
            });

            alert("Property Proposed! Projection running...");
            setNewPropName("");
            setTimeout(fetchInventory, 2000);

        } catch (e: any) {
            alert("Failed: " + (e.response?.data?.detail || e.message));
        }
    };

    // Action: Register Unit
    const handleRegisterUnit = async () => {
        if (!targetPropertyId || !newUnitName) return;
        setIsSubmitting(true);
        try {
            const token = localStorage.getItem('access_token');
            const payload = {
                actor: { user_id: "ui_user", role: "admin" },
                intent: {
                    action: "REGISTER_UNIT", // Matches Contract Trigger
                    target_resource: "auto-gen-unit",
                    parameters: {
                        property_id: targetPropertyId,
                        name: newUnitName,
                        status: "VACANT" // Initial State per Contract
                    }
                },
                evidence_hash: null,
                outcome: "APPROVED",
                policy_version: "1.0"
            };

            await axios.post('http://localhost:8000/api/v1/decisions', payload, {
                headers: { Authorization: `Bearer ${token}` }
            });

            alert("Unit Registered Successfully!");
            setNewUnitName("");
            setIsAddUnitOpen(false);
            setTimeout(fetchInventory, 1000);

        } catch (e: any) {
            alert("Failed to Register Unit: " + (e.response?.data?.detail || e.message));
        } finally {
            setIsSubmitting(false);
        }
    };

    // Action: Write Note
    const handleWriteNote = async () => {
        if (!selectedUnit || !noteContent) return;
        setIsSubmitting(true);
        try {
            const token = localStorage.getItem('access_token');

            // 1. Construct Decision (APPROVED to Trigger Execution)
            const payload = {
                actor: { user_id: "ui_user", role: "admin" }, // Mock Admin Role for auto-execution
                intent: {
                    action: "write_note",
                    target_resource: selectedUnit.unit_id, // In real app, mapper to AppFolio ID
                    parameters: { content: noteContent }
                },
                evidence_hash: null,
                outcome: "APPROVED", // Auto-Approve to trigger 'execute_decision'
                policy_version: "1.0"
            };

            await axios.post('http://localhost:8000/api/v1/decisions', payload, {
                headers: { Authorization: `Bearer ${token}` }
            });

            alert("Action Dispatched: Agent is writing note to AppFolio...");
            setNoteContent("");
            setSelectedUnit(null); // Close Modal

        } catch (e: any) {
            alert("Action Failed: " + (e.response?.data?.detail || e.message));
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 font-sans text-gray-900">
            {/* Header */}
            <header className="bg-white shadow">
                <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
                    <h1 className="text-3xl font-bold text-gray-900 tracking-tight">
                        Portfolio Ledger
                    </h1>
                    <div className="flex space-x-3">
                        <input
                            type="text"
                            placeholder="Property Name"
                            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                            value={newPropName}
                            onChange={(e) => setNewPropName(e.target.value)}
                        />
                        <button
                            onClick={handleRegisterProperty}
                            className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 focus:outline-none"
                        >
                            + Add Asset
                        </button>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                {/* Dashboard Stats (Mock) */}
                <div className="grid grid-cols-1 gap-5 sm:grid-cols-3 mb-8">
                    <div className="bg-white overflow-hidden shadow rounded-lg px-4 py-5 sm:p-6">
                        <dt className="text-sm font-medium text-gray-500 truncate">Total Units</dt>
                        <dd className="mt-1 text-3xl font-semibold text-gray-900">
                            {properties.reduce((acc, p) => acc + p.units.length, 0)}
                        </dd>
                    </div>
                    <div className="bg-white overflow-hidden shadow rounded-lg px-4 py-5 sm:p-6">
                        <dt className="text-sm font-medium text-gray-500 truncate">Occupancy Rate</dt>
                        <dd className="mt-1 text-3xl font-semibold text-green-600">92%</dd>
                    </div>
                    <div className="bg-white overflow-hidden shadow rounded-lg px-4 py-5 sm:p-6">
                        <dt className="text-sm font-medium text-gray-500 truncate">Pending Actions</dt>
                        <dd className="mt-1 text-3xl font-semibold text-blue-600">3</dd>
                    </div>
                </div>

                {/* Properties Grid */}
                {loading ? (
                    <div className="text-center py-20 text-gray-500 animate-pulse">Syncing with Blockchain...</div>
                ) : (
                    <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                        {properties.map(prop => (
                            <div key={prop.property_id} className="bg-white overflow-hidden shadow rounded-lg border border-gray-200">
                                <div className="px-5 py-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
                                    <div>
                                        <h3 className="text-lg leading-6 font-medium text-gray-900">{prop.name}</h3>
                                        <p className="mt-1 text-sm text-gray-500">{prop.address || "123 Main St (Default)"}</p>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                            {prop.units.length} Units
                                        </span>
                                        <button
                                            onClick={() => { setTargetPropertyId(prop.property_id); setIsAddUnitOpen(true); }}
                                            className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 px-2 py-1 rounded border border-gray-300 transform active:scale-95 transition-all"
                                        >
                                            + Add
                                        </button>
                                    </div>
                                </div>
                                <div className="bg-white px-5 py-5">
                                    <ul className="divide-y divide-gray-100">
                                        {prop.units.map(unit => (
                                            <li key={unit.unit_id} className="py-3 flex justify-between items-center hover:bg-gray-50 -mx-5 px-5 transition-colors duration-150">
                                                <div className="flex items-center">
                                                    <div className="flex-shrink-0 h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-500">
                                                        <HomeIcon className="h-6 w-6" />
                                                    </div>
                                                    <div className="ml-4">
                                                        <div className="text-sm font-medium text-gray-900">{unit.name}</div>
                                                        <div className="text-sm text-gray-500">
                                                            {unit.tenant_info ? (
                                                                <span className="flex items-center gap-1">
                                                                    <UserIcon className="h-3 w-3" /> {unit.tenant_info.name}
                                                                </span>
                                                            ) : "No Tenant"}
                                                        </div>
                                                    </div>
                                                </div>
                                                <div className="flex items-center gap-4">
                                                    <StatusBadge status={unit.status} />
                                                    <button
                                                        onClick={() => setSelectedUnit(unit)}
                                                        className="text-indigo-600 hover:text-indigo-900 text-sm font-medium"
                                                    >
                                                        Manage
                                                    </button>
                                                </div>
                                            </li>
                                        ))}
                                        {prop.units.length === 0 && (
                                            <li className="text-sm text-gray-500 italic py-2">No units recorded.</li>
                                        )}
                                    </ul>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>

            {/* Manage Unit Modal */}
            <Transition appear show={!!selectedUnit} as={Fragment}>
                <Dialog as="div" className="relative z-10" onClose={() => setSelectedUnit(null)}>
                    <Transition.Child
                        as={Fragment}
                        enter="ease-out duration-300"
                        enterFrom="opacity-0"
                        enterTo="opacity-100"
                        leave="ease-in duration-200"
                        leaveFrom="opacity-100"
                        leaveTo="opacity-0"
                    >
                        <div className="fixed inset-0 bg-black bg-opacity-25" />
                    </Transition.Child>

                    <div className="fixed inset-0 overflow-y-auto">
                        <div className="flex min-h-full items-center justify-center p-4 text-center">
                            <Transition.Child
                                as={Fragment}
                                enter="ease-out duration-300"
                                enterFrom="opacity-0 scale-95"
                                enterTo="opacity-100 scale-100"
                                leave="ease-in duration-200"
                                leaveFrom="opacity-100 scale-100"
                                leaveTo="opacity-0 scale-95"
                            >
                                <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                                    <Dialog.Title
                                        as="h3"
                                        className="text-lg font-medium leading-6 text-gray-900 flex items-center justify-between"
                                    >
                                        <span>Manage {selectedUnit?.name}</span>
                                        <StatusBadge status={selectedUnit?.status || ""} />
                                    </Dialog.Title>

                                    <div className="mt-4">
                                        <div className="bg-gray-50 p-3 rounded-md mb-4 text-sm text-gray-700">
                                            <p><span className="font-bold">Tenant:</span> {selectedUnit?.tenant_info?.name || "None"}</p>
                                            <p><span className="font-bold">Lease Source:</span> {selectedUnit?.tenant_info?.source || "N/A"}</p>
                                        </div>

                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Execute AppFolio Action
                                        </label>
                                        <div className="space-y-3">
                                            <textarea
                                                className="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500"
                                                rows={3}
                                                placeholder="Write a note to this tenant's AppFolio record..."
                                                value={noteContent}
                                                onChange={(e) => setNoteContent(e.target.value)}
                                            />
                                            <p className="text-xs text-gray-500 italic">
                                                * This will dispatch an AI Agent to AppFolio to post this note securely.
                                            </p>
                                        </div>
                                    </div>

                                    <div className="mt-6 flex justify-end space-x-3">
                                        <button
                                            type="button"
                                            className="inline-flex justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none"
                                            onClick={() => setSelectedUnit(null)}
                                        >
                                            Cancel
                                        </button>
                                        <button
                                            type="button"
                                            className="inline-flex justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none disabled:opacity-50"
                                            onClick={handleWriteNote}
                                            disabled={!noteContent || isSubmitting}
                                        >
                                            {isSubmitting ? "Dispatching..." : "Post Note"}
                                        </button>
                                    </div>
                                </Dialog.Panel>
                            </Transition.Child>
                        </div>
                    </div>
                </Dialog>
            </Transition>

            {/* Add Unit Modal */}
            <Transition appear show={isAddUnitOpen} as={Fragment}>
                <Dialog as="div" className="relative z-10" onClose={() => setIsAddUnitOpen(false)}>
                    <Transition.Child
                        as={Fragment}
                        enter="ease-out duration-300"
                        enterFrom="opacity-0"
                        enterTo="opacity-100"
                        leave="ease-in duration-200"
                        leaveFrom="opacity-100"
                        leaveTo="opacity-0"
                    >
                        <div className="fixed inset-0 bg-black bg-opacity-25" />
                    </Transition.Child>

                    <div className="fixed inset-0 overflow-y-auto">
                        <div className="flex min-h-full items-center justify-center p-4 text-center">
                            <Transition.Child
                                as={Fragment}
                                enter="ease-out duration-300"
                                enterFrom="opacity-0 scale-95"
                                enterTo="opacity-100 scale-100"
                                leave="ease-in duration-200"
                                leaveFrom="opacity-100 scale-100"
                                leaveTo="opacity-0 scale-95"
                            >
                                <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                                    <Dialog.Title as="h3" className="text-lg font-medium leading-6 text-gray-900">
                                        Register New Unit
                                    </Dialog.Title>
                                    <div className="mt-2">
                                        <p className="text-sm text-gray-500">
                                            Add a new unit to this property. It will start as VACANT.
                                        </p>
                                    </div>
                                    <div className="mt-4">
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Unit Name / Number
                                        </label>
                                        <input
                                            type="text"
                                            className="w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500"
                                            placeholder="e.g. Apt 101, Suite B"
                                            value={newUnitName}
                                            onChange={(e) => setNewUnitName(e.target.value)}
                                        />
                                    </div>

                                    <div className="mt-6 flex justify-end space-x-3">
                                        <button
                                            type="button"
                                            className="inline-flex justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none"
                                            onClick={() => setIsAddUnitOpen(false)}
                                        >
                                            Cancel
                                        </button>
                                        <button
                                            type="button"
                                            className="inline-flex justify-center rounded-md border border-transparent bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-700 focus:outline-none disabled:opacity-50"
                                            onClick={handleRegisterUnit}
                                            disabled={!newUnitName || isSubmitting}
                                        >
                                            {isSubmitting ? "Registering..." : "Register Unit"}
                                        </button>
                                    </div>
                                </Dialog.Panel>
                            </Transition.Child>
                        </div>
                    </div>
                </Dialog>
            </Transition>
        </div>
    );
}
