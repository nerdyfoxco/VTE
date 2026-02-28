import { NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

declare global {
    var appFolioEngineState: any;
    var appFolioActionResolver: any;
}

if (!global.appFolioEngineState) {
    global.appFolioEngineState = {
        status: 'OFFLINE',
        message: 'Engine Offline. Press Start to boot the RPA pipeline.',
        otpCountdown: 0,
        actionPhase: 'NONE'
    };
}

export async function POST(req: Request) {
    const body = await req.json();
    const { action, payload } = body;

    console.log(`[Next.js API] Received Action: ${action} with Payload: ${payload || 'none'}`);

    if (action === 'START_PIPELINE' && global.appFolioEngineState.status === 'OFFLINE') {
        global.appFolioEngineState.status = 'KICKOFF';
        global.appFolioEngineState.message = 'Initializing Playwright Browser Instance...';

        // Spawn the Headed Browser script as a child process
        const scriptPath = path.resolve(process.cwd(), '../../chapters/eyes/real_appfolio_extract.js');

        const rpaProcess = spawn('node', [scriptPath], {
            cwd: path.resolve(process.cwd(), '../../chapters/eyes'),
            stdio: ['pipe', 'pipe', 'pipe'] // IPC stdio
        });

        // Event listener for stdout to parse engine state from the script
        rpaProcess.stdout.on('data', (data) => {
            const output = data.toString();
            console.log(`[RPA STDOUT] ${output}`);

            if (output.includes('CHALLENGE_AVAILABILITY')) {
                global.appFolioEngineState.status = 'WAITING_ON_USER';
                global.appFolioEngineState.message = 'Are you physically available to help complete Multi-Factor Auth if prompted?';
                global.appFolioEngineState.actionPhase = 'AVAILABILITY';
            } else if (output.includes('CHALLENGE_OTP_INPUT')) {
                global.appFolioEngineState.status = 'WAITING_ON_USER';
                global.appFolioEngineState.message = 'Enter the 6-digit OTP code sent to the configured device.';
                global.appFolioEngineState.actionPhase = 'OTP';
                global.appFolioEngineState.otpCountdown = 30; // Start countdown
            } else if (output.includes('CHALLENGE_CAPTCHA')) {
                global.appFolioEngineState.status = 'WAITING_ON_USER';
                global.appFolioEngineState.message = 'CAPTCHA detected. Please solve it physically in the browser instance, then confirm here.';
                global.appFolioEngineState.actionPhase = 'CAPTCHA_CONFIRM';
            } else if (output.includes('CHALLENGE_FAILED_RESEND_PROMPT')) {
                global.appFolioEngineState.status = 'WAITING_ON_USER';
                global.appFolioEngineState.message = 'Previous OTP failed or timed out. Please input a new code.';
                global.appFolioEngineState.actionPhase = 'OTP_RETRY';
                global.appFolioEngineState.otpCountdown = 0; // Immediate resend available
            } else if (output.includes('EXTRACTION_SUCCESS')) {
                global.appFolioEngineState.status = 'DONE';
                global.appFolioEngineState.message = 'Data extraction finished successfully. You can close this window.';
                global.appFolioEngineState.actionPhase = 'NONE';
            } else if (output.includes('SESSION_ESTABLISHED')) {
                global.appFolioEngineState.status = 'RUNNING';
                global.appFolioEngineState.message = 'Automation running seamlessly in background (Dashboard reached).';
                global.appFolioEngineState.actionPhase = 'NONE';
            } else if (output.includes('FATAL ERROR')) {
                global.appFolioEngineState.status = 'FAILED';
                global.appFolioEngineState.message = `Engine failed: ${output}`;
                global.appFolioEngineState.actionPhase = 'NONE';
            } else if (output.includes('OTP_COUNTDOWN_TICK')) {
                // Example tick format: OTP_COUNTDOWN_TICK:25
                const match = output.match(/OTP_COUNTDOWN_TICK:(\d+)/);
                if (match) {
                    global.appFolioEngineState.otpCountdown = parseInt(match[1]);
                }
            }
        });

        rpaProcess.stderr.on('data', (data) => {
            console.error(`[RPA STDERR] ${data}`);
            global.appFolioEngineState.status = 'CRASHED';
            global.appFolioEngineState.message = `Process threw an error: ${data}`;
            global.appFolioEngineState.actionPhase = 'NONE';
        });

        rpaProcess.on('close', (code) => {
            console.log(`[Next.js API] RPA Process exited with code ${code}`);
            if (global.appFolioEngineState.status !== 'DONE' && global.appFolioEngineState.status !== 'FAILED') {
                global.appFolioEngineState.status = 'OFFLINE';
                global.appFolioEngineState.message = 'Process terminated unexpectedly. Press Start to boot again.';
                global.appFolioEngineState.actionPhase = 'NONE';
            }
        });

        // Store a reference to stdin so subsequent POSTs can send data to the script
        global.appFolioActionResolver = rpaProcess.stdin;

        return NextResponse.json({ success: true, state: global.appFolioEngineState });
    }

    if (global.appFolioActionResolver && global.appFolioEngineState.status !== 'OFFLINE') {
        if (action === 'SUBMIT') {
            global.appFolioActionResolver.write(`${payload}\n`);
            global.appFolioEngineState.status = 'RUNNING';
            global.appFolioEngineState.message = 'Validating input...';
        } else {
            // Treat actions like "YES", "NO", "RESEND" as the string payloads themselves
            global.appFolioActionResolver.write(`${action}\n`);
            global.appFolioEngineState.status = 'RUNNING';
            global.appFolioEngineState.message = `Processing ${action}...`;
            if (action === 'RESEND') {
                global.appFolioEngineState.message = `Requesting new OTP...`;
                global.appFolioEngineState.otpCountdown = 30;
            }
        }
        return NextResponse.json({ success: true, state: global.appFolioEngineState });
    }

    return NextResponse.json({ error: 'Engine is not running or invalid action' }, { status: 400 });
}
