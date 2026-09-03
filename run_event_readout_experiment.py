from pathlib import Path
import time

from src.event_readout_experiment import run_event_readout_campaign, write_outputs


def main() -> None:
    started = time.perf_counter()
    rows = run_event_readout_campaign()
    write_outputs(Path("results_event_readout"), rows)
    print(f"Ereignisauslese-Exploration abgeschlossen in {time.perf_counter()-started:.2f} s")


if __name__ == "__main__":
    main()
