#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows-compatible Runner
Fixes encoding issues for Windows Terminal
"""

import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    # Set UTF-8 encoding for stdout/stderr
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')
    
    # Set console to UTF-8
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Now import and run main
from main import main

if __name__ == "__main__":
    main()
