import axios from 'axios';

async function verifyNativeGatewayAuth() {
    console.log("=========================================");
    console.log("🔍 [TEST] Initiating Native Gateway Identity Exchange");
    console.log("=========================================");

    try {
        console.log("1. Executing /api/v1/auth/login against Canonical Framework...");

        // Target specifically the Edge Gateway (Port 8000), not the Python Backend (8001)
        const response = await axios.post('http://localhost:8000/api/v1/auth/login', {
            username: 'admin@vintasoftware.com', // To match python form encoded request
            email: 'admin@vintasoftware.com',    // Our Native Schema payload
            password: 'admin'
        });

        console.log("✅ Identity Authenticated Natively!");
        console.log("Token Bound:", response.data.access_token.substring(0, 40) + "...");
        console.log("Canonical Operator Profile:\n", JSON.stringify(response.data.operator, null, 2));

        console.log("\n2. Verifying Native JWT strictly inside the Orchestration Engine...");

        const shadowReq = await axios.post('http://localhost:8000/api/v1/orchestration/shadow', {
            workflowName: 'auth_verification_mock',
            payload: { context: "Security Verification" }
        }, {
            headers: { Authorization: `Bearer ${response.data.access_token}` }
        });

        console.log("✅ Orchestration Authorization Verified!");
        console.log("Engine Trace Result:\n", JSON.stringify(shadowReq.data, null, 2));

        console.log("\n🎉 Native Node.js Identity Strangulation Complete.");

    } catch (e: any) {
        if (e.response) {
            console.error("❌ Gateway Execution Failed HTTP", e.response.status);
            console.error("Payload:", JSON.stringify(e.response.data, null, 2));
        } else {
            console.error("❌ Critical Network or Syntax Error:", e);
        }
        process.exit(1);
    }
}

verifyNativeGatewayAuth();
