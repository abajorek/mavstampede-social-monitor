# MavStampede Social Monitor

MavStampede Social Monitor is a **CSV-first toolkit** for collecting, normalizing, and
classifying social media comments related to Colorado Mesa University's Maverick
Stampede marching band. The project avoids direct scraping by relying on CSV
exports that the user downloads manually from Facebook, Instagram, or TikTok.

The toolchain follows four primary steps:

1. **find** – produce keyword search queries to use when hunting for public posts.
2. **parse-exports** – load and normalize comment CSV exports from `data/raw/`.
3. **classify** – apply heuristic rules to assign CMU relevance, sentiment, and themes.
4. **export** – copy the classified data into the final reporting CSV.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for a deeper tour of the stack,
configuration, and development workflow.
