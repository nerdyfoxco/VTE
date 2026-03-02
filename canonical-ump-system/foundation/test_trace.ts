import jwt from 'jsonwebtoken';
import { config } from 'dotenv';
config({ path: '../../.env' });

async function testPostgresTraceExtrusion() {
    console.log("[TEST] Minting local Administrative JWT bound to the seeded canonical Tenant.");

    // Exact claims the Security Firewall expects
    const claims = {
        operatorId: '00000000-0000-0000-0000-000000000009', // Mock Operator ID
        email: 'admin@vintasoftware.com',
        role: 'admin',
        tenantId: '00000000-0000-0000-0000-000000000001' // Exact Tenant Seeded in Postgres
    };

    const secret = process.env.VTE_JWT_SECRET || 'super-secret-vte-key-for-local-dev-only-999';
    const token = jwt.sign(claims, secret, { expiresIn: '1h' });

    console.log("[TEST] Dispatching payload directly to the running Canonical Gateway...");

    try {
        const response = await fetch('http://localhost:8000/api/v1/orchestration/live', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                workflowName: 'Test_Postgres_Trace_Sealer',
                payload: { work_item_id: "WI-9999", bypass: true }
            })
        });

        const data = await response.json();

        if (response.ok) {
            console.log("✅ Success! Canonical Orchestration Engine penetrated Postgres perfectly:");
            console.log(JSON.stringify(data, null, 2));
        } else {
            console.error("❌ Failed. Gateway returned:", response.status, data);
        }
    } catch (e) {
        console.error("❌ Network execution crashed:", e);
    }
}

testPostgresTraceExtrusion();
