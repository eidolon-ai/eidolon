import argparse
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
parser.add_argument("yaml_path", type=str, help="Path to a YAML file describing the agent machine to start.")

# Parse command line arguments
args = parser.parse_args()


@asynccontextmanager
async def start_os(app: FastAPI):
    with open(args.yaml_path, 'r') as file:
        file_contents = file.read()

    os = AgentOS.from_yaml(file_contents)
    os.start(app)
    yield
    os.stop()

app = FastAPI(lifespan=start_os)

if __name__ == "__main__":

    # Run the server
    uvicorn.run("eidolon_sdk.agent_http_server:app", host="0.0.0.0", port=args.port, log_level="info", reload=args.reload)
