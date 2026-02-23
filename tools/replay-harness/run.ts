import * as fs from 'fs';
import * as path from 'path';
import { DecisionEvaluator } from '../../chapters/brain/evaluator';

const FIXTURES_DIR = path.join(__dirname, 'fixtures');
// Ensure it resolves to the actual location of the compiled graph
const GRAPH_PATH = path.resolve(__dirname, '../dt-compiler/compiled/decision_graph.json');

function main() {
    console.log('[Replay Harness] Initializing deterministic evaluation sandbox...');

    if (!fs.existsSync(GRAPH_PATH)) {
        console.error(`[Replay Harness] FATAL: Missing static [decision_graph.json]. Run 'dt-compiler' first.`);
        process.exit(1);
    }

    const evaluator = new DecisionEvaluator(GRAPH_PATH);

    const fixtureFiles = fs.readdirSync(FIXTURES_DIR).filter(f => f.endsWith('.json'));

    let totalPasses = 0;
    let totalFailures = 0;

    for (const file of fixtureFiles) {
        const fixturePath = path.join(FIXTURES_DIR, file);
        const fixtureStr = fs.readFileSync(fixturePath, 'utf8');
        const fixture = JSON.parse(fixtureStr);

        console.log(`\n[Replay Harness] Evaluating Fixture: ${file}`);
        console.log(`  Context:`, fixture.context);

        const result = evaluator.evaluate(fixture.context);

        const passed = (result.action === fixture.expectedAction && result.reason === fixture.expectedReason);

        if (passed) {
            console.log(`  [PASS] -> Output: ${result.action} (${result.reason}) exactly matched expectations.`);
            totalPasses++;
        } else {
            console.error(`  [FAIL] -> Expected: ${fixture.expectedAction} (${fixture.expectedReason})`);
            console.error(`         -> Actual:   ${result.action} (${result.reason})`);
            totalFailures++;
        }
    }

    console.log(`\n[Replay Summary] Passed: ${totalPasses} | Failed: ${totalFailures}`);
    if (totalFailures > 0) {
        console.error(`[Replay Harness] CI Halting. Determinism contract violated.`);
        process.exit(1);
    } else {
        process.exit(0);
    }
}

main();
