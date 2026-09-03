from pathlib import Path
import time

from src.return_experiment import (
    ranked_admissible,
    run_dt_validation,
    run_return_sweep,
    write_preregistered_outputs,
)


def main() -> None:
    started = time.perf_counter()
    rows = run_return_sweep()
    validation_rows = run_dt_validation(rows)
    write_preregistered_outputs(Path("results_return"), rows, validation_rows)
    eligible = ranked_admissible(rows)
    print(f"Rückführungssweep abgeschlossen: {len(rows)} Läufe in {time.perf_counter()-started:.2f} s")
    print(f"Zulässige Kandidaten vor Zeitschrittprüfung: {len(eligible)}")


if __name__ == "__main__":
    main()
