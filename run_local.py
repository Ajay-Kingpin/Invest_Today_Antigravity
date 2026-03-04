import subprocess
import time
import sys
import os
import signal

def kill_process_on_port(port):
    """Attempt to kill any process currently listening on a specific port."""
    try:
        if sys.platform == "win32":
            # Find the PID using netstat
            cmd = f'netstat -ano | findstr LISTENING | findstr ":{port}"'
            output = subprocess.check_output(cmd, shell=True).decode()
            for line in output.strip().split('\n'):
                if f":{port}" in line:
                    pid = line.strip().split()[-1]
                    print(f"⚠️ Port {port} is occupied by PID {pid}. Terminating...")
                    subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True)
    except Exception:
        pass # No process found or kill failed

def run_app():
    print("🚀 Starting Invest Today Local Environment...")
    
    # Clean up existing ports first
    kill_process_on_port(8000)
    kill_process_on_port(8501)
    
    # 1. Start the FastAPI Backend
    print("📦 Launching Backend API (FastAPI)...")
    backend_process = subprocess.Popen(
        [sys.executable, "main.py", "--api"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # 2. Give the backend a few seconds to warm up
    time.sleep(4)
    
    # 3. Start the Streamlit Frontend
    print("🎨 Launching Frontend UI (Streamlit)...")
    try:
        # We use 'streamlit run' which is usually in the Scripts folder of the venv
        streamlit_cmd = [sys.executable, "-m", "streamlit", "run", "app/ui/dashboard.py", "--server.port", "8501", "--server.headless", "true"]
        frontend_process = subprocess.Popen(streamlit_cmd)
        
        print("\n" + "="*50)
        print("✅ SYSTEM READY")
        print("FRONTEND LINK: http://localhost:8501")
        print("BACKEND API:   http://localhost:8000/docs")
        print("="*50 + "\n")
        print("Press Ctrl+C to stop both services.")
        
        # Wait for processes
        while True:
            time.sleep(1)
            if frontend_process.poll() is not None:
                print("⚠️ Frontend stopped unexpectedly.")
                break
            if backend_process.poll() is not None:
                print("⚠️ Backend stopped unexpectedly.")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
    finally:
        backend_process.terminate()
        if 'frontend_process' in locals():
            frontend_process.terminate()
        print("👋 Goodbye!")

if __name__ == "__main__":
    run_app()
