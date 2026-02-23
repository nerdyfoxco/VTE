import { UMP_RESPONSE_SCHEMA } from './schema';
import * as fs from 'fs';
import * as path from 'path';

export class OpenAIAdapter {
    private apiKey: string;
    private repoRoot: string;

    constructor(repoRoot: string) {
        this.apiKey = process.env.OPENAI_API_KEY || '';
        this.repoRoot = repoRoot;

        if (!this.apiKey) {
            console.warn('[OpenAI Adapter] Warning: OPENAI_API_KEY is not set. API calls will fail.');
        }
    }

    public async executeUMP(umpId: string, systemPrompt: string, umpPrompt: string): Promise<{ path: string, content: string }[]> {
        console.log(`\n[OpenAI Adapter] Dispatched ${umpId} to OpenAI (Strict JSON Schema)...`);

        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: 'gpt-4o',
                messages: [
                    { role: 'system', content: systemPrompt },
                    { role: 'user', content: umpPrompt }
                ],
                response_format: UMP_RESPONSE_SCHEMA,
                temperature: 0.1
            })
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`[OpenAI Adapter] FATAL: OpenAI API Error: ${response.status} - ${errorText}`);
            process.exit(1);
        }

        const data = await response.json();
        const contentStr = data.choices[0].message.content;

        // Traceability: Save the raw LLM output for physical auditing
        const traceDir = path.join(this.repoRoot, 'repo', 'runs', umpId, 'openai');
        if (!fs.existsSync(traceDir)) fs.mkdirSync(traceDir, { recursive: true });
        fs.writeFileSync(path.join(traceDir, 'raw_response.json'), contentStr);

        const parsedContent = JSON.parse(contentStr);
        return parsedContent.edits || [];
    }
}
