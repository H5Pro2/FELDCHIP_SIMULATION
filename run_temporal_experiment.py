from pathlib import Path
import time

from src.temporal_experiment import run_temporal_campaign, write_temporal_outputs


def main() -> None:
    started = time.perf_counter()
    rows = run_temporal_campaign()
    summary = write_temporal_outputs(Path("results_temporal"), rows)
    print(f"Zeitlicher Hauptversuch abgeschlossen: {len(rows)} Modellläufe in {time.perf_counter()-started:.2f} s")
    for row in summary:
        print(f"{row['model']:<30} Trennrate={100*float(row['accuracy_mean']):5.1f}%")


if __name__ == "__main__":
    main()

