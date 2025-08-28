#!/usr/bin/env python3
"""
Digital Key Tracker - Main Application Entry Point
"""

from app.database import init_db
from app.cli import cli

if __name__ == '__main__':
    # Initialize the database
    init_db()
    
    # Run the CLI
    cli()