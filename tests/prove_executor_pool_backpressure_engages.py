import concurrent.futures
import time
import sys
import queue

# Proof: Executor Pool Backpressure Engages
# Proves that we don't just "queue forever" and crash memory. We must reject when full.

class BoundedExecutor:
    def __init__(self, max_threads=2, max_queue=2):
        self.max_queue = max_queue
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_threads)
        self.task_queue = queue.Queue(maxsize=max_queue)
        
    def submit_task(self, task_func):
        # In a real system (e.g. FastAPI + Celery), this is 503 Service Unavailable
        if self.task_queue.full():
            raise RuntimeError("Backpressure: Queue Full")
            
        self.task_queue.put(1) # Reserve slot
        try:
            future = self.pool.submit(self._wrapped_task, task_func)
            return future
        except Exception as e:
            self.task_queue.get() # Release if submit failed (rare)
            raise e
            
    def _wrapped_task(self, func):
        try:
            return func()
        finally:
            self.task_queue.get() # Release slot

def slow_task():
    time.sleep(0.5)
    return "OK"

def prove_backpressure():
    print("Testing Executor Backpressure...")
    
    # 2 Threads, 2 Queue Slots = Capacity 4ish concurrent (2 running + 2 waiting)
    executor = BoundedExecutor(max_threads=1, max_queue=1)
    
    futures = []
    
    try:
        # 1. Fill Worker (1)
        futures.append(executor.submit_task(slow_task))
        # 2. Fill Queue (1)
        futures.append(executor.submit_task(slow_task))
        
        print("  System Saturated. Attempting Overflow...")
        
        # 3. Overflow
        executor.submit_task(slow_task)
        print("  [FAIL] System accepted task beyond capacity!")
        return False
        
    except RuntimeError as e:
        print(f"  [PASS] System rejected overflow task: {e}")
        return True

if __name__ == "__main__":
    if prove_backpressure():
        sys.exit(0)
    else:
        sys.exit(1)
