"""
Sports Injury Risk Detection Intelligence Platform - Launcher
"""
import sys
import time
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    try:
        import asyncio
        # WindowsSelectorEventLoop avoids proactor WinError 10054 on browser disconnect
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

# Ensure project root is in python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if __name__ == "__main__":
    import uvicorn
    print("======================================================================")
    print("  [AI] SPORTS INJURY RISK DETECTION INTELLIGENCE PLATFORM")
    print("  Computer Vision - Pose Estimation - Biomechanical Analytics")
    print("======================================================================")
    print("  Server launching at: http://127.0.0.1:8000")
    print("  API Docs at:         http://127.0.0.1:8000/docs")
    print("======================================================================")
    
    while True:
        try:
            uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False, log_level="info")
        except KeyboardInterrupt:
            print("\nShutting down server...")
            break
        except Exception as e:
            print(f"[Server Warning] Recovering from connection event: {e}. Restarting server...")
            time.sleep(1)
