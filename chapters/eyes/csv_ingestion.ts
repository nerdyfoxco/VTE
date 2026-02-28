import fs from 'fs';
import path from 'path';
import csv from 'csv-parser';
import * as crypto from 'crypto';

interface AppFolioRow {
    'Tenant Name': string;
    'Property Name': string;
    'Unit': string;
    'Balance': string;
    'Days Late': string;
    'Tags': string;
}

// Replicating the physical Pipeline ingestion from a clean CSV export
async function ingestCSVIntoDataPlane() {
    console.log('[Eyes CSV Pipeline] Initiating secure ingestion sequence...');
    const exportPath = path.resolve(__dirname, '../../storage/exports/appfolio_delinquency.csv');

    if (!fs.existsSync(exportPath)) {
        console.error(`[Eyes CSV Pipeline] ERROR: AppFolio CSV Export not found at ${exportPath}`);
        return;
    }

    const records: AppFolioRow[] = [];

    fs.createReadStream(exportPath)
        .pipe(csv())
        .on('data', (data: AppFolioRow) => records.push(data))
        .on('end', async () => {
            console.log(`[Eyes CSV Pipeline] Parsed ${records.length} records. Routing to Execution Spine...`);

            for (const record of records) {
                const balance = parseFloat(record['Balance']) || 0;
                const daysLate = parseInt(record['Days Late']) || 0;
                const tags = record['Tags'] ? record['Tags'].split(',').map(t => t.trim()) : [];

                // Constructing the pristine, canonically valid PipeEnvelope
                const envelope = {
                    workspace_id: "VTE-001", // Hardcoded strictly mapped workspace
                    work_item_id: `wi_${crypto.randomUUID()}`,
                    correlation_id: crypto.randomUUID(),
                    organ_source: "EYES_APPFOLIO_CSV",
                    organ_target: "BRAIN_ROUTER",
                    policy_version: "v1.0.4",
                    timestamp: new Date().toISOString(),
                    payload: {
                        propertyName: record['Property Name'],
                        unit: record['Unit'],
                        tenantName: record['Tenant Name'],
                        balance: balance,
                        daysLate: daysLate,
                        tags: tags
                    }
                };

                console.log(`[Eyes CSV Pipeline] Dispatching Tenant: ${record['Tenant Name']} [Bal: $${balance}] -> [${envelope.correlation_id}]`);

                try {
                    const res = await fetch('http://127.0.0.1:3001/api/pipe', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(envelope)
                    });

                    if (res.ok) {
                        console.log(`[Eyes CSV Pipeline] ✔ Ingested & Indexed`);
                    } else {
                        console.error(`[Eyes CSV Pipeline] ✖ SPINE REJECTED: HTTP ${res.status}`);
                    }
                } catch (e: any) {
                    console.error(`[Eyes CSV Pipeline] ✖ FATAL NETWORK ERROR: Could not reach Data Plane Ingress. Is web-operations running?`);
                }
            }

            console.log(`[Eyes CSV Pipeline] Ingestion sequence complete.`);
        });
}

ingestCSVIntoDataPlane();
