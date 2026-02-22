import sys
import unittest
import asyncio
from pathlib import Path

current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from backpressure_manager import BackpressureManager, BackpressureState, BackpressureError

class TestBackpressureManager(unittest.IsolatedAsyncioTestCase):
    
    async def asyncSetUp(self):
        self.manager = BackpressureManager(max_capacity=100)

    async def test_initial_state_active(self):
        self.assertEqual(self.manager.get_state(), BackpressureState.ACTIVE)
        self.assertEqual(self.manager.get_load(), 0)

    async def test_successful_ingestion(self):
        await self.manager.register_ingestion(50)
        self.assertEqual(self.manager.get_load(), 50)
        self.assertEqual(self.manager.get_state(), BackpressureState.ACTIVE)

    async def test_exceeding_capacity_triggers_paused_and_throws(self):
        await self.manager.register_ingestion(90)
        
        with self.assertRaises(BackpressureError) as context:
            await self.manager.register_ingestion(15)  # 90 + 15 > 100
            
        self.assertIn("exceeds capacity", str(context.exception))
        self.assertEqual(self.manager.get_state(), BackpressureState.PAUSED)
        self.assertEqual(self.manager.get_load(), 90) # Should not have added the 15

    async def test_ingestion_blocked_while_paused(self):
        # Force a pause natively
        with self.assertRaises(BackpressureError):
            await self.manager.register_ingestion(101)
            
        with self.assertRaises(BackpressureError) as context:
            await self.manager.register_ingestion(1)
            
        self.assertIn("System is currently PAUSED", str(context.exception))

    async def test_release_capacity_resumes_system(self):
        await self.manager.register_ingestion(90)
        try:
             await self.manager.register_ingestion(15)
        except BackpressureError:
             pass
             
        self.assertEqual(self.manager.get_state(), BackpressureState.PAUSED)
        
        # Release capacity below the 80% hysteresis threshold (80 limit)
        await self.manager.release_capacity(15) # 90 - 15 = 75
        self.assertEqual(self.manager.get_state(), BackpressureState.ACTIVE)

if __name__ == '__main__':
    unittest.main()
