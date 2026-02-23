import * as crypto from 'crypto';

interface LedgerRecord {
    propertyName: string;
    unit: string;
    tenantName: string;
    balance: number;
    tags: string[];
}

// Emulating an external scrape from AppFolio
const mockAppFolioLedger: LedgerRecord[] = [
    {
        propertyName: '3118 N Bambrey St',
        unit: 'Whole House',
        tenantName: 'Tonette Whitehead',
        balance: 1030.00,
        tags: []
    },
    {
        propertyName: '1420 Walnut St',
        unit: '4B',
        tenantName: 'John Doe',
        balance: 450.00,
        tags: ['DNC']
    }
];

// Replicating the physical Pipeline ingestion
async function ingestIntoDataPlane() {
    console.log('[Eyes Adapter] Scraping AppFolio ledgers...');

    for (const record of mockAppFolioLedger) {

        // Constructing the pristine, canonically valid PipeEnvelope
        const envelope = {
            workspace_id: "VTE-001", // Hardcoded strictly mapped workspace
            work_item_id: `wi_${crypto.randomUUID()}`,
            correlation_id: crypto.randomUUID(),
            organ_source: "EYES_APPFOLIO_SCRAPER",
            organ_target: "BRAIN_ROUTER",
            policy_version: "v1.0.4",
            timestamp: new Date().toISOString(),
            payload: {
                ...record
            }
        };

        console.log(`[Eyes Adapter] Dispatching [${envelope.correlation_id}] to Execution Spine`);

        try {
            const res = await fetch('http://localhost:3001/api/pipe', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(envelope)
            });

            if (res.ok) {
                console.log(`[Eyes Adapter] -> SUCCESSFULLY INGESTED into Data Plane Queue`);
            } else {
                console.error(`[Eyes Adapter] -> SPINE REJECTED: HTTP ${res.status}`);
            }
        } catch (e: any) {
            console.error(`[Eyes Adapter] -> FATAL NETWORK ERROR: Could not reach Data Plane Ingress. Is web-operations running?`);
        }
    }
}

ingestIntoDataPlane();
