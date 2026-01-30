#!/usr/bin/env python 
# encoding: utf-8
import sys
import os

# Ensure the current directory is in sys.path to allow running without installation
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from scriptLattes.run import main

if __name__ == "__main__":
    main()
