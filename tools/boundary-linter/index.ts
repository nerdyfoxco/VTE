import * as fs from 'fs';
import * as path from 'path';

const PROJECT_ROOT = path.resolve(__dirname, '../../');
const CHAPTERS_DIR = path.join(PROJECT_ROOT, 'chapters');

// Define exactly which cross-boundaries are strictly legal
const ALLOWLIST = [
    'foundation',
    'spine',
    'types',
    'contracts'
];

let hasErrors = false;

function lintDirectory(dir: string, currentOrgan: string) {
    const files = fs.readdirSync(dir);

    for (const file of files) {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);

        if (stat.isDirectory()) {
            lintDirectory(fullPath, currentOrgan);
        } else if (file.endsWith('.ts') || file.endsWith('.tsx')) {
            lintFile(fullPath, currentOrgan);
        }
    }
}

function lintFile(filePath: string, currentOrgan: string) {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');

    lines.forEach((line, index) => {
        // Rudimentary heuristic for import statements mapping back to project directories
        if (line.trim().startsWith('import') && line.includes('from')) {
            const match = line.match(/from\s+['"](.*)['"]/);
            if (match && match[1]) {
                const importPath = match[1];

                // Only inspect relative physical paths targeting the chapters boundary
                if (importPath.includes('chapters/')) {
                    // Extract the targeted organ namespace
                    const targetOrganMatch = importPath.match(/chapters\/([^\/]+)/);
                    if (targetOrganMatch && targetOrganMatch[1]) {
                        const targetOrgan = targetOrganMatch[1];

                        // Enforce the strict isolation invariant
                        if (targetOrgan !== currentOrgan) {
                            console.error(`\n[Boundary Linter FATAL] File: ${path.relative(PROJECT_ROOT, filePath)}:${index + 1}`);
                            console.error(`  Target: The [${currentOrgan}] organ is illegally importing from [${targetOrgan}]`);
                            console.error(`  Constraint: Organs may only communicate by pushing opaque PipeEnvelopes to the Spine.`);
                            hasErrors = true;
                        }
                    }
                }
            }
        }
    });
}

function main() {
    console.log('[Boundary Linter] Auditing physical isolation geometry for Spine/Organ execution...');

    if (!fs.existsSync(CHAPTERS_DIR)) {
        console.warn('Chapters directory not found, assuming empty build.');
        process.exit(0);
    }

    const organs = fs.readdirSync(CHAPTERS_DIR)
        .filter(f => fs.statSync(path.join(CHAPTERS_DIR, f)).isDirectory());

    console.log(`[Boundary Linter] Discovered ${organs.length} execution organs: ${organs.join(', ')}`);

    for (const organ of organs) {
        lintDirectory(path.join(CHAPTERS_DIR, organ), organ);
    }

    if (hasErrors) {
        console.error('\n[Boundary Linter] FATAL: Physical Architecture Corrupted. CI Pipeline Halting.');
        process.exit(1);
    } else {
        console.log('\n[Boundary Linter] PASS: The Node architecture is mathematically pristine. Zero illegal entanglement detected.');
        process.exit(0);
    }
}

main();
