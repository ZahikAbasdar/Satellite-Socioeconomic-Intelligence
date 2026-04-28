#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# Satellite-Driven Socioeconomic Intelligence — Launch Script
# Usage: ./run.sh
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend/app"
BACKEND_PORT=8000
FRONTEND_PORT=8501

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'
YELLOW='\033[1;33m'; BOLD='\033[1m'; RESET='\033[0m'

echo ""
echo -e "${CYAN}${BOLD}"
echo "  ╔══════════════════════════════════════════════════════════╗"
echo "  ║   🛰️  SATELLITE-DRIVEN SOCIOECONOMIC INTELLIGENCE v2.0  ║"
echo "  ║         India + Global · FastAPI · Streamlit · AI        ║"
echo "  ╚══════════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# Check Python
PYTHON=$(which python3 || which python)
if [ -z "$PYTHON" ]; then
    echo -e "${RED}❌ Python not found. Install Python 3.9+${RESET}"
    exit 1
fi
PYTHON_VER=$($PYTHON --version 2>&1 | awk '{print $2}')
echo -e "  ${GREEN}✓${RESET} Python $PYTHON_VER found"

# Install dependencies
echo -e "  ${CYAN}📦 Checking dependencies...${RESET}"
$PYTHON -m pip install -r "$SCRIPT_DIR/requirements.txt" -q --break-system-packages 2>/dev/null || \
$PYTHON -m pip install -r "$SCRIPT_DIR/requirements.txt" -q 2>/dev/null
echo -e "  ${GREEN}✓${RESET} Dependencies ready"

# Pre-train ML model (if needed)
echo -e "  ${CYAN}🧠 Loading ML model...${RESET}"
cd "$BACKEND_DIR"
PYTHONPATH="$BACKEND_DIR" $PYTHON -c "
import sys; sys.path.insert(0, '.')
from src.model import get_predictor
p = get_predictor()
print('  \033[0;32m✓\033[0m Model ready')
" 2>/dev/null
cd "$SCRIPT_DIR"

# Start FastAPI backend
echo ""
echo -e "  ${CYAN}🚀 Starting FastAPI backend (port $BACKEND_PORT)...${RESET}"
cd "$BACKEND_DIR"
PYTHONPATH="$BACKEND_DIR" $PYTHON -m uvicorn main:app \
    --host 0.0.0.0 \
    --port $BACKEND_PORT \
    --log-level warning &
BACKEND_PID=$!
cd "$SCRIPT_DIR"

# Wait for backend to be ready
echo -e "  ${YELLOW}   Waiting for backend...${RESET}"
for i in $(seq 1 20); do
    sleep 1
    HEALTH=$($PYTHON -c "
import urllib.request
try:
    urllib.request.urlopen('http://127.0.0.1:$BACKEND_PORT/health', timeout=2)
    print('ok')
except: print('no')
" 2>/dev/null)
    if [ "$HEALTH" = "ok" ]; then
        echo -e "  ${GREEN}✓${RESET} Backend running at http://localhost:$BACKEND_PORT"
        break
    fi
    if [ $i -eq 20 ]; then
        echo -e "  ${YELLOW}⚠ Backend health timeout — may still be loading${RESET}"
    fi
done

# Start Streamlit frontend
echo ""
echo -e "  ${CYAN}🎨 Starting Streamlit frontend (port $FRONTEND_PORT)...${RESET}"
PYTHONPATH="$SCRIPT_DIR/src:$SCRIPT_DIR" \
$PYTHON -m streamlit run "$SCRIPT_DIR/main.py" \
    --server.port $FRONTEND_PORT \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --browser.gatherUsageStats false \
    --theme.base dark \
    --theme.primaryColor "#63b3ed" \
    --theme.backgroundColor "#080c14" \
    --theme.secondaryBackgroundColor "#0d1424" \
    --theme.textColor "#f0f4ff" &
FRONTEND_PID=$!
sleep 3

echo ""
echo -e "  ${BOLD}──────────────────────────────────────────────────────────${RESET}"
echo -e "  ${GREEN}${BOLD}🎉  Application is running!${RESET}"
echo -e "  ──────────────────────────────────────────────────────────"
echo -e "  ${CYAN}🌐  Frontend  →  http://localhost:$FRONTEND_PORT${RESET}"
echo -e "  ${CYAN}⚙️   Backend   →  http://localhost:$BACKEND_PORT${RESET}"
echo -e "  ${CYAN}📖  API Docs  →  http://localhost:$BACKEND_PORT/docs${RESET}"
echo -e "  ──────────────────────────────────────────────────────────"
echo -e "  Press ${BOLD}Ctrl+C${RESET} to stop all services"
echo ""

# Graceful shutdown
cleanup() {
    echo ""
    echo -e "  ${YELLOW}Stopping services...${RESET}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo -e "  ${GREEN}✓ Stopped. Goodbye 👋${RESET}"
    exit 0
}
trap cleanup SIGINT SIGTERM

# Monitor children
while true; do
    sleep 5
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "  ${RED}Backend process died — restarting...${RESET}"
        cd "$BACKEND_DIR"
        PYTHONPATH="$BACKEND_DIR" $PYTHON -m uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT --log-level warning &
        BACKEND_PID=$!
        cd "$SCRIPT_DIR"
    fi
done
