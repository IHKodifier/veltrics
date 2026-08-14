import sys
import pytest

if __name__ == "__main__":
    retcode = pytest.main(["src/tests/unit/test_auth_uc001.py", "-v"])
    sys.exit(retcode)
