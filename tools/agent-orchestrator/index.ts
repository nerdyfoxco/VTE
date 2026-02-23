import * as fs from 'fs';
import * as path from 'path';
import { ChangeApplier } from './applier';
import { OpenAIAdapter } from './adapter.openai';

const PROJECT_ROOT = path.resolve(__dirname, '../../');
const SYSTEM_PROMPT_PATH = path.join(PROJECT_ROOT, 'system_prompt', 'SystemPrompt.md');
const UMPS_DIR = path.join(PROJECT_ROOT, 'umps');
const SEALS_DIR = path.join(PROJECT_ROOT, 'repo', 'seals');

async function main() {
    console.log('[Orchestrator] Booting Autonomous UMP Meta-Runner...');

    if (!fs.existsSync(SYSTEM_PROMPT_PATH) || !fs.existsSync(UMPS_DIR)) {
        console.warn('[Orchestrator] VTE_Agent_Build_Pack not found at root. Did you extract the PRD zip?');
        console.error('Expected paths:');
        console.error(' - ' + SYSTEM_PROMPT_PATH);
        console.error(' - ' + UMPS_DIR);
        process.exit(1);
    }

    const systemPrompt = fs.readFileSync(SYSTEM_PROMPT_PATH, 'utf8');
    const applier = new ChangeApplier(PROJECT_ROOT);
    const adapter = new OpenAIAdapter(PROJECT_ROOT);

    const umpFiles = fs.readdirSync(UMPS_DIR).filter(f => f.startsWith('UMP-') && f.endsWith('.md')).sort();

    console.log(`[Orchestrator] Discovered ${umpFiles.length} UMPs in the Build Queue.`);

    for (const umpFilename of umpFiles) {
        const umpId = umpFilename.replace('.md', '');
        const sealPath = path.join(SEALS_DIR, `${umpId}.seal.json`);

        if (fs.existsSync(sealPath)) {
            console.log(`[Orchestrator] SKIP: ${umpId} is already SEALED.`);
            continue;
        }

        console.log(`\n================================`);
        console.log(`[Orchestrator] EXECUTING: ${umpId}`);
        console.log(`================================`);

        const umpPrompt = fs.readFileSync(path.join(UMPS_DIR, umpFilename), 'utf8');

        // Dry Run mode detected if API key is missing
        if (!process.env.OPENAI_API_KEY) {
            console.log(`[Orchestrator] DRY RUN mode. OPENAI_API_KEY missing. Parsing only.`);
            const allowlist = applier.parseAllowlist(umpPrompt);
            console.log(`[Orchestrator] Detected Allowlist for ${umpId}:\n  - ${allowlist.join('\n  - ')}`);
        } else {
            // Live Execution
            const edits = await adapter.executeUMP(umpId, systemPrompt, umpPrompt);
            applier.applySafely(edits, umpId, umpPrompt);

            // Phase 19 Execution Accelerators would be programmaticlly triggered here in a real scenario
            // if (execSync('npm run dt:compile').status !== 0) throw Error(...)

            applier.seal(umpId);
        }
    }

    console.log('\n[Orchestrator] Loop Terminated. All UMPs processed or skipped.');
}

main().catch(err => {
    console.error('[Orchestrator] FATAL CATCH:', err);
    process.exit(1);
});
