from pathlib import Path
import time

from src.multiscale_confirmation import (
    run_confirmation_campaign,
    run_technical_confirmation,
    write_outputs,
)


def main() -> None:
    started = time.perf_counter()
    technical_rows = run_technical_confirmation()
    task_rows = run_confirmation_campaign(technical_rows)
    write_outputs(Path("results_multiscale_confirmation"), technical_rows, task_rows)
    print(f"Zeitskalen-Bestätigung abgeschlossen in {time.perf_counter()-started:.2f} s")


if __name__ == "__main__":
    main()

