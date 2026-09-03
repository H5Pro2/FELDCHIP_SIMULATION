from pathlib import Path
import time

from src.adaptation_experiment import run_exploratory_campaign, run_technical_screen, write_outputs


def main() -> None:
    started = time.perf_counter()
    technical_rows = run_technical_screen()
    task_rows = run_exploratory_campaign(technical_rows)
    write_outputs(Path("results_adaptation"), technical_rows, task_rows)
    print(f"Adaptations-Exploration abgeschlossen in {time.perf_counter()-started:.2f} s")


if __name__ == "__main__":
    main()
