import sys
import traceback
from pathlib import Path
from fastapi.testclient import TestClient
import uuid
import datetime
from datetime import timezone

sys.path.insert(0, str(Path('c:/Bintloop/VTE/ump_v2/spine/src')))

try:
    from main import app
    print("App imported successfully", flush=True)

    client = TestClient(app, raise_server_exceptions=False)
    payload = {
        'workspace_id': 'ws_123',
        'work_item_id': 'task_abc',
        'correlation_id': str(uuid.uuid4()),
        'organ_source': 'eyes',
        'organ_target': 'brain',
        'timestamp': datetime.datetime.now(timezone.utc).isoformat(),
        'payload': {
             'user_id': 'user_1',
             'status': 'delinquent',
             'ssn': '123-45-6789'
        }
    }
    response = client.post('/ingest', json=payload)
    print('STATUS:', response.status_code, flush=True)
    print('TEXT:', response.text, flush=True)
except Exception as e:
    traceback.print_exc(file=sys.stdout)
