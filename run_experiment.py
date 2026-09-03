from pathlib import Path
import time

from src.feldchip_simulation import run_campaign, write_outputs


def main() -> None:
    started = time.perf_counter()
    rows, examples = run_campaign()
    summary = write_outputs(Path("results"), rows, examples)
    elapsed = time.perf_counter() - started
    print(f"Versuchskampagne abgeschlossen: {len(rows)} Modellläufe in {elapsed:.2f} s")
    for row in summary:
        print(
            f"{row['model']:<30} "
            f"Trennrate={100*float(row['accuracy_mean']):5.1f}% "
            f"Wiederhol-RMSE={float(row['repeatability_rmse_mean']):.3f}"
        )


if __name__ == "__main__":
    main()
