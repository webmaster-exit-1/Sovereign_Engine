import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUNTIME_DIR = os.path.join(BASE_DIR, ".runtime")
SOCKET_FILENAME = "sovereign_master.sock"
SOCKET_PATH = os.path.join(RUNTIME_DIR, SOCKET_FILENAME)

# Phase contract: newline-delimited UTF-8 JSON payloads.
JSON_FRAME_DELIMITER = "\n"

# Fixed worker pool and aligned listen backlog policy.
MAX_WORKERS = 5
SOCKET_BACKLOG = MAX_WORKERS

# Startup health-check policy.
READINESS_TIMEOUT_SECONDS = 5.0
READINESS_PROBE_INTERVAL_SECONDS = 0.25
