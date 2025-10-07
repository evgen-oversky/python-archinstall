import sys
import subprocess
import time

start_time = time.time()

def run_command(cmd):
    try:
        result = subprocess.run(cmd, check=True capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"{e}")
        print(f"{e.stderr}")
        sys.exit(1)

def check_internet():
    pass

test


print(run_command(["ping", "-c", "1", "8.8.8.8"]).returncode)








duration = time.time() - start_time
print(f"{duration:.2f}")

