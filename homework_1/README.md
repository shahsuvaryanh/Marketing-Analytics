# Bass model: GoPro and HOVERAir

Analysis of HOVERAir X1 ProMax using historical worldwide GoPro camera shipments.

- `bass_diffusion.ipynb`: analysis, Python code, results and citations.
- `data/gopro_shipments.csv`: annual historical shipments and source IDs.
- `img/`: historical fit and adoption forecast figures.
- `report/report.pdf`: final report.
- `report/report_source.md`: editable report source.
- `references/sources.md`: reference links and data definitions.
- `references/DS-223-Bass-model.pdf`: lecture methodology.

Install dependencies with `python -m pip install -r requirements.txt`.
Start Jupyter with `jupyter lab`, open the notebook from this folder, and run all cells in order.

The analysis fits the lecture's annual-sales Bass equation, estimates HOVERAir's market separately using explicit Fermi assumptions, and projects annual adoption for ten model years.
