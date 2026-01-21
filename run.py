#!/usr/bin/env python3
import os
import signal
import subprocess
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "mind_poc", "backend")
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "mind_poc", "frontend")


def start_backend() -> subprocess.Popen:
    command = [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"]
    return subprocess.Popen(command, cwd=BACKEND_DIR)


def start_frontend() -> subprocess.Popen:
    command = ["npm", "run", "dev"]
    return subprocess.Popen(command, cwd=FRONTEND_DIR)


def terminate_process(process: subprocess.Popen, name: str) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
    print(f"Stopped {name}.")


def main() -> int:
    if not os.path.isdir(BACKEND_DIR):
        print("Backend directory not found.")
        return 1
    if not os.path.isdir(FRONTEND_DIR):
        print("Frontend directory not found.")
        return 1

    print("Starting backend...")
    backend = start_backend()
    print("Starting frontend...")
    frontend = start_frontend()

    def handle_signal(signum, _frame):
        print(f"Received signal {signum}. Shutting down...")
        terminate_process(frontend, "frontend")
        terminate_process(backend, "backend")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    try:
        while True:
            backend_status = backend.poll()
            frontend_status = frontend.poll()
            if backend_status is not None:
                print(f"Backend exited with code {backend_status}.")
                terminate_process(frontend, "frontend")
                return backend_status
            if frontend_status is not None:
                print(f"Frontend exited with code {frontend_status}.")
                terminate_process(backend, "backend")
                return frontend_status
            time.sleep(0.5)
    except KeyboardInterrupt:
        handle_signal(signal.SIGINT, None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
