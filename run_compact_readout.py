from pathlib import Path
import time

from src.feldchip_simulation import run_campaign, write_outputs


def main() -> None:
    started = time.perf_counter()
    rows, examples = run_campaign(readout="compact")
    summary = write_outputs(Path("results_compact"), rows, examples, readout="compact")
    elapsed = time.perf_counter() - started
    print(f"Kompakte Auslese abgeschlossen: {len(rows)} Modellläufe in {elapsed:.2f} s")
    for row in summary:
        print(f"{row['model']:<30} Trennrate={100*float(row['accuracy_mean']):5.1f}%")


if __name__ == "__main__":
    main()
