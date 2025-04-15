# logger.py
import logging

# Create custom logger
logger = logging.getLogger("myapp")
logger.setLevel(logging.INFO)  # You can change to DEBUG for dev mode

# Formatter for logs
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# File handler
file_handler = logging.FileHandler("app.log", mode="a")
file_handler.setFormatter(formatter)

# Add both handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
