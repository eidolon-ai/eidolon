import logging

# Basic configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Get logger for your module
logger = logging.getLogger("browser-service")
