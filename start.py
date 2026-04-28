#!/usr/bin/env python3
"""
Satellite-Driven Socioeconomic Intelligence
Single-file launcher — starts FastAPI backend + Streamlit frontend
Usage:  python start.py
        python start.py --backend-only
        python start.py --frontend-only
"""

import os
import sys
import time
import signal
import argparse
import subprocess
import threading

# ── ANSI colors ───────────────────────────────────────────────────────────────
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

BANNER = f"""
{CYAN}{BOLD}
  ╔══════════════════════════════════════════════════════════╗
  ║   🛰️  SATELLITE-DRIVEN SOCIOECONOMIC INTELLIGENCE v2.0  ║
  ║         AI · FastAPI · Streamlit · Plotly · Folium       ║
  ╚══════════════════════════════════════════════════════════╝
{RESET}"""

ROOT        = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT, "backend", "app")
FRONTEND    = os.path.join(ROOT, "main.py")
BACKEND_PORT  = 8000
FRONTEND_PORT = 8501

processes: list = []


def log(tag: str, msg: str, color: str = RESET):
    print(f"  {color}{BOLD}[{tag}]{RESET} {msg}")


def install_deps():
    req = os.path.join(ROOT, "requirements.txt")
    if not os.path.exists(req):
        log("WARN", "requirements.txt not found — skipping install", YELLOW)
        return
    log("SETUP", "Installing / verifying dependencies ...", CYAN)
    cmd = [sys.executable, "-m", "pip", "install", "-r", req, "-q"]
    # Try with --break-system-packages first (Linux system Python)
    try:
        subprocess.run(cmd + ["--break-system-packages"],
                       check=True, capture_output=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            log("WARN", f"pip install had issues: {e.stderr.decode()[:200]}", YELLOW)
    log("SETUP", f"{GREEN}Dependencies ready ✓{RESET}", "")


def pre_train_model():
    """Warm up / train the ML model before starting servers."""
    log("MODEL", "Pre-loading ML model (this takes ~3 s the first time) ...", CYAN)
    try:
        sys.path.insert(0, BACKEND_DIR)
        from app.src.model import get_predictor   # noqa
        get_predictor()
        log("MODEL", f"{GREEN}Model ready ✓{RESET}", "")
    except Exception as e:
        log("MODEL", f"{YELLOW}Model pre-load skipped: {e}{RESET}", "")
    finally:
        # Remove so subprocesses load cleanly
        if BACKEND_DIR in sys.path:
            sys.path.remove(BACKEND_DIR)


def start_backend():
    log("API", f"Starting FastAPI backend on port {BACKEND_PORT} ...", CYAN)
    env = os.environ.copy()
    env["PYTHONPATH"] = BACKEND_DIR + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "0.0.0.0",
            "--port", str(BACKEND_PORT),
            "--log-level", "warning",
            "--reload",
        ],
        cwd=BACKEND_DIR,
        env=env,
    )
    processes.append(proc)
    # Wait until it's up
    import urllib.request
    for attempt in range(20):
        time.sleep(1)
        try:
            urllib.request.urlopen(
                f"http://127.0.0.1:{BACKEND_PORT}/health", timeout=2
            )
            log("API", f"{GREEN}Backend online → http://localhost:{BACKEND_PORT}{RESET}", "")
            log("API", f"  Swagger docs  → http://localhost:{BACKEND_PORT}/docs", "")
            return True
        except Exception:
            pass
        if proc.poll() is not None:
            log("API", f"{RED}Backend crashed — check logs above{RESET}", "")
            return False
    log("API", f"{YELLOW}Backend health check timed out — may still be starting{RESET}", "")
    return True


def start_frontend():
    log("UI", f"Starting Streamlit frontend on port {FRONTEND_PORT} ...", CYAN)
    env = os.environ.copy()
    env["PYTHONPATH"] = (
        os.path.join(ROOT, "src") + os.pathsep
        + ROOT + os.pathsep
        + env.get("PYTHONPATH", "")
    )
    proc = subprocess.Popen(
        [
            sys.executable, "-m", "streamlit", "run", FRONTEND,
            "--server.port", str(FRONTEND_PORT),
            "--server.address", "0.0.0.0",
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false",
            "--browser.gatherUsageStats", "false",
            "--theme.base", "dark",
            "--theme.primaryColor", "#63b3ed",
            "--theme.backgroundColor", "#080c14",
            "--theme.secondaryBackgroundColor", "#0d1424",
            "--theme.textColor", "#f0f4ff",
        ],
        cwd=ROOT,
        env=env,
    )
    processes.append(proc)
    time.sleep(4)
    if proc.poll() is None:
        log("UI", f"{GREEN}Frontend online → http://localhost:{FRONTEND_PORT}{RESET}", "")
    else:
        log("UI", f"{RED}Frontend failed to start{RESET}", "")
    return proc.poll() is None


def shutdown(sig=None, frame=None):
    print()
    log("STOP", "Shutting down all services ...", YELLOW)
    for p in processes:
        try:
            p.terminate()
            p.wait(timeout=5)
        except Exception:
            try:
                p.kill()
            except Exception:
                pass
    log("STOP", "All services stopped. Goodbye 👋", GREEN)
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="SatSocio Intelligence Launcher")
    parser.add_argument("--backend-only",  action="store_true")
    parser.add_argument("--frontend-only", action="store_true")
    parser.add_argument("--no-install",    action="store_true", help="Skip pip install")
    args = parser.parse_args()

    signal.signal(signal.SIGINT,  shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    print(BANNER)

    if not args.no_install:
        install_deps()

    backend_ok  = True
    frontend_ok = True

    if not args.frontend_only:
        pre_train_model()
        backend_ok = start_backend()

    if not args.backend_only:
        frontend_ok = start_frontend()

    if not (backend_ok and frontend_ok):
        log("ERROR", "One or more services failed to start", RED)
        shutdown()

    print()
    print(f"  {BOLD}{'─'*56}{RESET}")
    print(f"  {GREEN}{BOLD}🎉  Application is running!{RESET}")
    print(f"  {'─'*56}")
    if not args.backend_only:
        print(f"  {CYAN}🌐  Frontend   →  http://localhost:{FRONTEND_PORT}{RESET}")
    if not args.frontend_only:
        print(f"  {CYAN}⚙️   Backend    →  http://localhost:{BACKEND_PORT}{RESET}")
        print(f"  {CYAN}📖  API Docs   →  http://localhost:{BACKEND_PORT}/docs{RESET}")
    print(f"  {'─'*56}")
    print(f"  Press {BOLD}Ctrl+C{RESET} to stop all services\n")

    # Keep alive — monitor child processes
    while True:
        time.sleep(5)
        dead = [p for p in processes if p.poll() is not None]
        if dead:
            log("WARN", f"{len(dead)} service(s) exited unexpectedly", YELLOW)
            shutdown()


if __name__ == "__main__":
    main()
