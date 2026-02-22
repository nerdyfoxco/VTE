# Load .env variables
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^#=]+)=(.*)$') {
        $name = $matches[1]
        $value = $matches[2]
        [System.Environment]::SetEnvironmentVariable($name, $value, [System.EnvironmentVariableTarget]::Process)
        Write-Host "Set Env: $name"
    }
}

$env:PYTHONPATH = "C:\Bintloop\VTE"
python chapters/CH03_INGESTION/runtime/visual_login_agent.py
