import os
import pathlib
from dotenv import load_dotenv


ENV_PATH_FILE = os.path.join(
    os.path.abspath(os.curdir), ".env"
)  # For handelling in package

load_dotenv(ENV_PATH_FILE, override=True)


ROOT = pathlib.Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data"
DATA_FILE = DATA_DIR / os.getenv("MIE_DATASET_FILE_NAME", "dataset-mie.json")
OUTPUT_DIR = ROOT / "output"
FLOW_TEMPLATE_PATH = ROOT / "src"
CLI_ALERT_POINT = 500
AI_API_KEY = os.getenv("MIE_AI_API_KEY", "")