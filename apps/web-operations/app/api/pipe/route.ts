import { NextResponse } from 'next/server';

// In a full environment, this imports from the central `spine/registry`
function enforceTenantIsolationMock(envelope: any, expectedWorkspace: string) {
    if (!envelope.workspace_id) throw new Error("Missing Workspace ID");
    if (envelope.workspace_id !== expectedWorkspace) {
        throw new Error(`[TenantGuard] SEVERE SECURITY VIOLATION: Pipe crossing detected. Expected [${expectedWorkspace}], received [${envelope.workspace_id}]`);
    }
}

export async function POST(req: Request) {
    try {
        const envelope = await req.json();

        // Contextually, the API gateway would inject the caller's bound workspace context.
        // For this operational prototype, we assume execution within 'VTE-001'.
        const ACTIVE_CONTEXT = 'VTE-001';

        console.log(`[DataPlane Ingress] Received PipeEnvelope from [${envelope.organ_source}]`);

        // Mandatory Spine Authorization Gate
        try {
            enforceTenantIsolationMock(envelope, ACTIVE_CONTEXT);
        } catch (guardError: any) {
            console.error(guardError.message);
            return NextResponse.json({ error: 'Tenant Violation Blocked' }, { status: 403 });
        }

        // --- Data Plane Memory Queue Ingestion occurs here natively ---
        // Pushing to local operational state machine for Brain execution...

        console.log(`[DataPlane Ingress] Envelope [${envelope.correlation_id}] successfully queued for Brain execution.`);

        return NextResponse.json({
            success: true,
            status: 'ACCEPTED_INTO_SPINE',
            correlation_id: envelope.correlation_id
        }, { status: 202 });

    } catch (error: any) {
        console.error('[DataPlane API] Ingress failure:', error.message);
        return NextResponse.json({ error: 'Invalid Payload' }, { status: 400 });
    }
}
