import subprocess
import sys

print("Retail ETL pipeline started")

subprocess.run(
    [sys.executable, "src/extract.py"],
    check=True
)

subprocess.run(
    [sys.executable, "src/load.py"],
    check=True
)