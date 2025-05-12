import sys
import os
import pytest

# Add the parent directory to Python path so 'backend' is treated as a top-level package
sys.path.insert(0, os.path.abspath('.'))

# Run the tests
if __name__ == "__main__":
    # Run pytest programmatically
    pytest.main(['backend'])
