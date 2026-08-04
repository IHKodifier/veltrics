import os
import sys
import pytest

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

if __name__ == "__main__":
    result = pytest.main(["src/tests/unit/test_auth_uc001.py", "-v"])
    print(f"\nPytest Exit Code: {result}")
    sys.exit(result)
