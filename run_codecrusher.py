#!/usr/bin/env python3
"""
CodeCrusher Launcher Script
Wrapper script to handle proper module imports

Author: Martin Pfeffer (c) 2025
License: MIT
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Now import and run main
from main import main

if __name__ == "__main__":
    main()