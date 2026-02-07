import sys
import os
import unittest



# Add cwd to path for vte package resolution
sys.path.append(os.getcwd())
try:
    from vte.core.loader import loader, BundleLoader
except ImportError as e:
    print(f"FAIL: Could not import vte.core.loader: {e}")
    sys.exit(1)

class TestBundleLoader(unittest.TestCase):
    def test_singleton(self):
        l1 = BundleLoader()
        l2 = BundleLoader()
        self.assertIs(l1, l2, "Loader must be a singleton")
        
    def test_fail_closed_before_seal(self):
        # Should raise error if we try to get contract before sealing
        with self.assertRaises(RuntimeError):
            loader.get_contract("some_contract")

    def test_seal_mechanism(self):
        # We need to simulate a bundle file existence
        dummy_bundle = "dummy_bundle.zip"
        with open(dummy_bundle, "w") as f:
            f.write("dummy content")
            
        try:
            loader.load_bundle(dummy_bundle)
            # Now it should work (mocked)
            c = loader.get_contract("test")
            self.assertEqual(c["mock"], "contract")
            
            # Sealing again should fail
            with self.assertRaises(RuntimeError):
                loader.load_bundle(dummy_bundle)
                
        finally:
            if os.path.exists(dummy_bundle):
                os.remove(dummy_bundle)

if __name__ == "__main__":
    unittest.main()
