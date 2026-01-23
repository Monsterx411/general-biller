# Logging configuration for the application

import logging
import os
from datetime import datetime

def setup_logging(log_dir="logs"):
    """Setup application logging"""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"loan_manager_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def get_logger(name):
    """Get a logger instance"""
    return logging.getLogger(name)
