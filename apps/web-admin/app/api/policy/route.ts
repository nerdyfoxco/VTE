import { NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export async function POST(req: Request) {
    try {
        const body = await req.json();
        const { workspaceId, version, globalWaitDays, contactThresholdMax, isActive } = body;

        if (!workspaceId || !version) {
            return NextResponse.json({ error: 'Missing required configuration keys.' }, { status: 400 });
        }

        const policy = await prisma.policyVersion.create({
            data: {
                workspaceId,
                version,
                globalWaitDays: globalWaitDays || 0,
                contactThresholdMax: contactThresholdMax || 3,
                isActive: isActive || false,
            }
        });

        return NextResponse.json({ success: true, policy }, { status: 201 });
    } catch (error: any) {
        console.error('[ControlPlane API] Policy creation failed:', error.message);
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}

export async function GET(req: Request) {
    const { searchParams } = new URL(req.url);
    const workspaceId = searchParams.get('workspaceId');

    if (!workspaceId) {
        return NextResponse.json({ error: 'workspaceId is required for multi-tenant isolation.' }, { status: 400 });
    }

    try {
        const policies = await prisma.policyVersion.findMany({
            where: { workspaceId }
        });

        return NextResponse.json({ policies }, { status: 200 });
    } catch (error: any) {
        console.error('[ControlPlane API] Policy retrieval failed:', error.message);
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
