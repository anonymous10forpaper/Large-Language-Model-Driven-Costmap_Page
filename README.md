# Policy Bridge Project Page

Static GitHub Pages site for **Natural-Language to Nav2: LLM-Driven Costmaps
for Industrial AMRs** and its Policy Bridge operator interface.

## Local preview

```bash
cd ~/turtlebot3_ws/Large-Language-Model-Driven-Costmap_Page
python3 -m http.server 8080
```

Open `http://localhost:8080` in a browser.

## Layout

```text
index.html       Page content and semantic structure
styles.css       Responsive visual design
script.js        Mobile navigation, tabs, and copy controls
assets/          GUI, pipeline, and RViz images
```

The site has no build step. GitHub Pages can publish the `main` branch from
the repository root.

## Participant Study

The primary navigation's **User Study** link opens `user-study.html`.
It includes the study map, English participant instructions, and expandable
task briefs with the paper's 80 commands (10 participants, T1-T8).
Participant command text is unchanged from the frozen paper dataset.
The page is static, uses the shared reference-map asset, and links back to
`index.html`.

### Reference Map

User Study and Benchmark both use `assets/study-map-factory6.png`, exported
from the actual Policy Bridge map scene using `factory6.yaml` and its saved
`factory6_waypoints.yaml` annotations. This replaces the earlier schematic;
waypoint positions, zone bounds, and occupancy geometry now match the GUI.
WP1/WP2 are beside Zone A, WP3/WP4 beside Zone B, WP5/WP6 beside Zone D,
and WP7/WP8 beside Zone E. The waypoint rows are not equally spaced.

`assets/study-map-factory6.json` records the source hashes, map origin and
resolution, zone bounds, and world/image coordinates for all eight waypoints.
This is a presentation correction only; participant commands and benchmark
policies have not changed.

To regenerate with PyQt5, PyYAML, and the Policy Bridge source available:

```bash
python3 tools/render_study_map.py \
  --policy-bridge-src /path/to/workspace/src/policy_bridge \
  --map /path/to/map/factory6.yaml \
  --annotations /path/to/map/factory6_waypoints.yaml \
  --output assets/study-map-factory6.png
```

The exporter checks coordinate round trips and rendered marker pixels.
It does not start ROS or change the source map or annotations.

## Benchmark

The **Benchmark** menu beside **User Study** opens `benchmark.html`:

- 150 natural-language commands, with ground-truth policies and L0-L4/type filters.
- 100 contradiction tests, with five conflict types and expected rejection decisions.
- 15 original prompt input-output pairs in their evaluation order (11 accept, 4 reject).

Commands and demonstration pairs are unchanged from the frozen paper archive.
For the 150-command set, the displayed eight-field policy JSON is a canonical
rendering of each archived gold signature, round-trip checked with the archived
evaluator, not a model prediction. The original signatures remain available.
Contradiction recognition targets are distinguished from end-to-end containment.

The page includes search, expandable JSON, copy/download controls, a reference
map, and source hashes. `benchmark-data.json` contains the full data bundle.
Both files are static and require no server-side processing or model calls.
Embedded Lucide icons are covered by `assets/benchmark-icons-LICENSE`.
The **Rule-based baseline code** link opens the runtime repository's
`policy_bridge/evaluation/` folder, which contains the actual v4 paper
baseline, its v3 helper dependency, and standalone execution instructions.

## Keepout Comparison

The **Keepout Comparison** menu opens `keepout-comparison.html`, an English-only
summary of five custom-layer and five native-filter trials. Recorded metrics,
protocol, anonymized configuration files, odometry, and costmap snapshots are
available in `data/keepout-comparison/` and `downloads/keepout-evidence.zip`.
Costmap figures are not displayed.

Recalculate recorded metrics and check source-artifact hashes with:

```bash
python3 tools/verify_keepout.py
```

See `data/keepout-comparison/README.txt` for metric definitions, anonymization,
and verification scope. This evidence release is not a full simulator rerun
package and does not claim independent experimental replication.
