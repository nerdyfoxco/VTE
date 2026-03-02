import OpenAI from 'openai';
import { PrismaClient } from '@prisma/client';

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY || 'sk-mock-key-for-local-dev',
});

const prisma = new PrismaClient();

export class VectorService {
    /**
     * Generate an embedding using OpenAI text-embedding-ada-002 (1536 dimensions)
     */
    static async generateEmbedding(text: string): Promise<number[]> {
        if (process.env.OPENAI_API_KEY) {
            const response = await openai.embeddings.create({
                model: 'text-embedding-ada-002',
                input: text.replace(/\n/g, ' '),
            });
            return response.data[0].embedding;
        } else {
            console.warn("[VECTOR_SERVICE] Missing OPENAI_API_KEY. Returning mock embedding.");
            return new Array(1536).fill(0.01);
        }
    }

    /**
     * Upsert a chunk of text into the Postgres Vector Database for a given tenant
     */
    static async storeEmbedding(tenantId: string, sourceUri: string, content: string): Promise<void> {
        const embedding = await this.generateEmbedding(content);

        // Stringify the array for pgvector casting format "[0.1, 0.2, ...]"
        const embeddingString = `[${embedding.join(',')}]`;

        // Use Prisma raw queries because pgvector 'vector' type is Unsupported native
        await prisma.$executeRaw`
            INSERT INTO "VectorEmbedding" ("id", "tenantId", "sourceUri", "content", "embedding", "createdAt")
            VALUES (gen_random_uuid(), ${tenantId}, ${sourceUri}, ${content}, ${embeddingString}::vector, NOW())
        `;
        console.log(`[VECTOR_SERVICE] Stored embedding for ${sourceUri}`);
    }

    /**
     * Retrieve the nearest context chunks for a given query (Cosine Similarity)
     */
    static async searchSimilar(tenantId: string, query: string, limit: number = 3): Promise<{ content: string, sourceUri: string, distance: number }[]> {
        const queryEmbedding = await this.generateEmbedding(query);
        const embeddingString = `[${queryEmbedding.join(',')}]`;

        // Use Cosine Distance (<=>) operator provided by pgvector
        const results = await prisma.$queryRaw<any[]>`
            SELECT "sourceUri", "content", "embedding" <=> ${embeddingString}::vector as distance
            FROM "VectorEmbedding"
            WHERE "tenantId" = ${tenantId}
            ORDER BY distance ASC
            LIMIT ${limit}
        `;

        return results.map(row => ({
            sourceUri: row.sourceUri,
            content: row.content,
            distance: row.distance
        }));
    }
}
