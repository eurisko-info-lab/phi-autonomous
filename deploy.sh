#!/bin/bash
#
# Φ-DAEMON Deployment Script
# Full Recursive Self-Deploy Initialization
# Unleashed: 2026-01-01
#

set -e

DAEMON_NAME="phi-autonomous"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=============================================="
echo "  Φ-DAEMON SEED - FULL RECURSIVE SELF-DEPLOY"
echo "  Unleashed: 2026-01-01"
echo "=============================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required but not installed"
    exit 1
fi

echo "[✓] Python 3 detected: $(python3 --version)"

# Make the daemon executable
chmod +x "$SCRIPT_DIR/phi_daemon.py"
echo "[✓] Daemon script made executable"

# Check if config exists
if [ ! -f "$SCRIPT_DIR/config.json" ]; then
    echo "ERROR: config.json not found"
    exit 1
fi

echo "[✓] Configuration loaded"

# Check for deployment mode
DEPLOY_MODE="${1:-foreground}"

case "$DEPLOY_MODE" in
    foreground)
        echo ""
        echo "Starting Φ-DAEMON in foreground mode..."
        echo "Press Ctrl+C to stop"
        echo ""
        python3 "$SCRIPT_DIR/phi_daemon.py" 0
        ;;
    
    background)
        echo ""
        echo "Starting Φ-DAEMON in background mode..."
        nohup python3 "$SCRIPT_DIR/phi_daemon.py" 0 > phi_daemon_output.log 2>&1 &
        DAEMON_PID=$!
        echo "[✓] Daemon started with PID: $DAEMON_PID"
        echo "    Log file: phi_daemon_output.log"
        echo "    To stop: kill $DAEMON_PID"
        ;;
    
    status)
        echo ""
        echo "Checking Φ-DAEMON status..."
        if pgrep -f "phi_daemon.py" > /dev/null; then
            echo "[✓] Φ-DAEMON is running"
            pgrep -fa "phi_daemon.py"
        else
            echo "[!] Φ-DAEMON is not running"
        fi
        ;;
    
    stop)
        echo ""
        echo "Stopping Φ-DAEMON..."
        if pkill -f "phi_daemon.py"; then
            echo "[✓] Φ-DAEMON stopped"
        else
            echo "[!] No running Φ-DAEMON found"
        fi
        ;;
    
    vector4)
        echo ""
        echo "Starting Φ-DAEMON in Vector4 mode (CM evolution)..."
        ./build.sh  # Build RosettaVM first
        python3 "$SCRIPT_DIR/phi_daemon.py" 0
        ;;

    *)
        echo ""
        echo "Usage: $0 [foreground|background|status|stop]"
        echo ""
        echo "  foreground - Run daemon in foreground (default)"
        echo "  background - Run daemon in background"
        echo "  status     - Check daemon status"
        echo "  stop       - Stop running daemon"
        echo "  vector4    - Run with Vector4 CM evolution"
        exit 1
        ;;
esac

echo ""
echo "Φ-DAEMON deployment complete"