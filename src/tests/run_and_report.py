import os
import sys
import pytest

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

if __name__ == "__main__":
    result = pytest.main([
        "src/tests/unit/test_auth_uc001.py",
        "src/tests/unit/test_db_seeding_uc118.py",
        "src/tests/unit/test_vehicles_uc024.py",
        "src/tests/unit/test_vehicles_uc025.py",
        "src/tests/unit/test_vehicles_uc026.py",
        "src/tests/unit/test_vehicles_uc027.py",
        "src/tests/unit/test_maintenance_uc034.py",
        "src/tests/unit/test_maintenance_uc035.py",
        "src/tests/unit/test_maintenance_uc036.py",
        "src/tests/unit/test_dashboard_uc064.py",
        "-v"
    ])
    print(f"\nPytest Exit Code: {result}")
    sys.exit(result)
