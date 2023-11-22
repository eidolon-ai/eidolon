import argparse
import logging.config
from contextlib import asynccontextmanager

import dotenv
import uvicorn
from fastapi import FastAPI

from eidolon_sdk.agent_os import AgentOS

dotenv.load_dotenv()

# Set up the argument parser
parser = argparse.ArgumentParser(description="Start a FastAPI server.")
parser.add_argument("-p", "--port", type=int, default=8080, help="Port to run the FastAPI server on. Defaults to 8080.")
parser.add_argument("-r", "--reload", help="Reload the server when the code changes. Defaults to False.", action="store_true")
parser.add_argument('--debug', action='store_true', help='Turn on debug logging')
parser.add_argument("yaml_path", type=str, help="Path to a YAML file describing the agent machine to start.")

# Parse command line arguments
args = parser.parse_args()


@asynccontextmanager
async def start_os(app: FastAPI):
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("eidolon")
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)

    with open(args.yaml_path, 'r') as file:
        file_contents = file.read()

    os = AgentOS.from_yaml(file_contents)
    await os.start(app)
    yield
    os.stop()

app = FastAPI(lifespan=start_os)

if __name__ == "__main__":
    log_level_str = "debug" if args.debug else "info"

    # Run the server
    uvicorn.run("eidolon_sdk.agent_http_server:app", host="0.0.0.0", port=args.port, log_level=log_level_str, reload=args.reload)
