import os
from pir_sensor import run_pir_sensors

WORKSPACE = os.environ.get("SYSTEM_WORKSPACE", None)
if WORKSPACE is None:
    raise Exception("Workspace not defined")
MEDIA_DIR = os.path.join(WORKSPACE, "media")

if __name__ == "__main__":
    run_pir_sensors()
