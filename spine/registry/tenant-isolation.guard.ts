export function enforceTenantIsolation(pipeEnvelope: any, currentContextWorkspaceId: string): void {
    if (!pipeEnvelope || typeof pipeEnvelope !== 'object') {
        throw new Error('[TenantGuard] Null or malformed PipeEnvelope encountered.');
    }

    const envelopeWorkspaceId = pipeEnvelope.workspace_id;

    if (!envelopeWorkspaceId) {
        throw new Error('[TenantGuard] Execution halted: Missing workspace_id in PipeEnvelope.');
    }

    if (envelopeWorkspaceId !== currentContextWorkspaceId) {
        throw new Error(`[TenantGuard] SEVERE SECURITY VIOLATION: Execution blocked. Pipe crossing detected. Expected Workspace [${currentContextWorkspaceId}], but envelope contained [${envelopeWorkspaceId}].`);
    }

    // Pass-through if safe
}
