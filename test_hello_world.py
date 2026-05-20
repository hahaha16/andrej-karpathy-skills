import subprocess
import sys
from pathlib import Path
import unittest


class HelloWorldScriptTest(unittest.TestCase):
    def test_script_prints_expected_message(self):
        script_path = Path(__file__).with_name("hello-world.py")
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.stdout, "Hello from Symphony test\n")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
