from enum import Enum
from asyncio import Lock

class BackpressureState(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"

class BackpressureError(Exception):
    """Raised when ingestion is attempted while the system is overloaded."""
    pass

class BackpressureManager:
    """
    Phase 3 Data Plane (Lungs): Tracks queue depth to emit backpressure signals.
    Fails closed (throws exception) if ingestion goes over capacity.
    """
    def __init__(self, max_capacity: int = 1000):
        self.max_capacity = max_capacity
        self._current_load = 0
        self._state = BackpressureState.ACTIVE
        self._lock = Lock()

    async def register_ingestion(self, count: int = 1) -> None:
        """
        Records incoming items. If adding this count exceeds capacity,
        rejects the batch explicitly by throwing BackpressureError.
        """
        async with self._lock:
            if self._state == BackpressureState.PAUSED:
                raise BackpressureError(f"System is currently PAUSED due to backpressure. Load: {self._current_load}/{self.max_capacity}")

            if self._current_load + count > self.max_capacity:
                self._state = BackpressureState.PAUSED
                raise BackpressureError(f"Ingestion rejected. Adding {count} items exceeds capacity ({self.max_capacity}). State is now PAUSED.")

            self._current_load += count
            
    async def release_capacity(self, count: int = 1) -> None:
        """
        Frees up capacity as items are processed by the Brain/Legs.
        Automatically resumes ingestion if dropping below 80% capacity threshold.
        """
        async with self._lock:
            self._current_load = max(0, self._current_load - count)
            
            # Hysteresis: resume taking traffic when load drops below 80% to prevent thrashing
            if self._state == BackpressureState.PAUSED and self._current_load <= (self.max_capacity * 0.8):
                self._state = BackpressureState.ACTIVE

    def get_state(self) -> BackpressureState:
        return self._state
        
    def get_load(self) -> int:
        return self._current_load
