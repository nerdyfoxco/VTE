import * as fs from 'fs';
import * as path from 'path';

export class ChangeApplier {
    private repoRoot: string;

    constructor(repoRoot: string) {
        this.repoRoot = repoRoot;
    }

    public parseAllowlist(umpPromptContext: string): string[] {
        // Regex extracts lines directly under "Files:" until a blank line or next section
        const match = umpPromptContext.match(/Files:\s*\n([\s\S]*?)(?:\n\n|\n[A-Z])/);
        if (!match) return [];

        return match[1].split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0 && !line.startsWith('-'));
    }

    public applySafely(edits: { path: string, content: string }[], umpId: string, umpPrompt: string) {
        console.log(`\n[Applier] Applying modifications for ${umpId}...`);

        const allowlist = this.parseAllowlist(umpPrompt);

        for (const edit of edits) {
            // Anti-Path Traversal Check
            if (edit.path.includes('..') || path.isAbsolute(edit.path)) {
                console.error(`  [FATAL] Boundary Violation: Agent attempted path traversal on ${edit.path}.`);
                process.exit(1);
            }

            // Allowlist Authorization Check
            if (!allowlist.includes(edit.path)) {
                console.error(`  [FATAL] Security Violation: Agent attempted to write to an unauthorized file: ${edit.path}`);
                console.error(`          Allowed by UMP: ${allowlist.join(', ')}`);
                process.exit(1);
            }

            const targetPath = path.join(this.repoRoot, edit.path);
            const targetDir = path.dirname(targetPath);

            if (!fs.existsSync(targetDir)) {
                fs.mkdirSync(targetDir, { recursive: true });
            }

            fs.writeFileSync(targetPath, edit.content);
            console.log(`  [OK] Wrote: ${edit.path}`);
        }
    }

    public seal(umpId: string) {
        const sealDir = path.join(this.repoRoot, 'repo', 'seals');
        if (!fs.existsSync(sealDir)) fs.mkdirSync(sealDir, { recursive: true });

        const sealData = {
            umpId,
            status: "SEALED",
            timestamp: new Date().toISOString()
        };

        fs.writeFileSync(path.join(sealDir, `${umpId}.seal.json`), JSON.stringify(sealData, null, 2));
        console.log(`[Applier] ${umpId} is permanently SEALED.`);
    }
}
