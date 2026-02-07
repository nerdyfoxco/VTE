import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

// Request Interceptor: Inject Token
api.interceptors.request.use((config) => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

export interface EvidenceBundleDraft {
    normalization_schema: string;
    items: any[];
}

export interface DecisionDraft {
    actor: {
        user_id: string;
        role: string;
        session_id: string;
    };
    intent: {
        action: string;
        target_resource: string;
        parameters: any;
    };
    evidence_hash: string;
    outcome: "APPROVED" | "DENIED" | "NEEDS_MORE_EVIDENCE";
    policy_version: string;
}

export interface DecisionRead {
    decision_id: string;
    timestamp: string;
    actor_user_id: string;
    actor_role: string;
    actor_session_id?: string;
    intent_action: string;
    intent_target: string;
    intent_params: any;
    evidence_hash?: string;
    outcome: "PROPOSED" | "APPROVED" | "DENIED" | "NEEDS_MORE_EVIDENCE";
    policy_version: string;
    decision_hash: string;
    previous_hash?: string;
}

export const getDecisions = async (status?: string): Promise<DecisionRead[]> => {
    const params = status ? { status } : {};
    const response = await api.get<DecisionRead[]>("/decisions", { params });
    return response.data;
};

export const createDecision = async (draft: DecisionDraft): Promise<DecisionRead> => {
    const response = await api.post<DecisionRead>("/decisions", draft);
    return response.data;
};


export const exchangeGoogleToken = async (idToken: string): Promise<string> => {
    const response = await api.post<{ access_token: string; token_type: string }>("/auth/google-exchange", { id_token: idToken });
    return response.data.access_token;
};

export interface QueueItem {
    id: string;
    priority: number;
    sla_deadline: string;
    assigned_to?: string;
    // Enriched fields for UI
    title: string;
    status: "PENDING" | "IN_PROGRESS" | "DONE";
}

export const getQueueItems = async (): Promise<QueueItem[]> => {
    const response = await api.get<QueueItem[]>("/queue");
    // Ensure dates are parsed back to ISO strings if needed, or handled by UI
    return response.data;
};
