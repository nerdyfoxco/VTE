import { NextResponse } from 'next/server';

// Global singleton for the AppFolio Engine state since API routes are stateless by default
declare global {
    var appFolioEngineState: any;
    var appFolioActionResolver: any;
}

if (!global.appFolioEngineState) {
    global.appFolioEngineState = {
        status: 'OFFLINE',
        message: 'Engine Offline. Press Start to boot the RPA pipeline.',
        otpCountdown: 0,
        actionPhase: 'NONE' // NONE|AVAILABILITY|CAPTCHA|OTP|OTP_RETRY
    };
}

export async function GET() {
    return NextResponse.json(global.appFolioEngineState);
}
