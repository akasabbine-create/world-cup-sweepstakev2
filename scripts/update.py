import subprocess
import sys


def run(command):
    print("Running:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    print("Fetching live matches...")
    run([sys.executable, "scripts/fetch_matches.py"])

    print("Calculating leaderboard/state...")
    run([sys.executable, "-m", "engine.scorer"])

    print("Done.")
