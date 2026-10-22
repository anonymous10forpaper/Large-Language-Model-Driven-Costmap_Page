Native Keepout Comparison: Recorded Evidence

Scope
This release documents a single-policy backend comparison in Gazebo, with
five custom-layer and five native-filter trials. It does not evaluate LLM,
validator, or policy-bridge runtime execution. Each trial starts fresh, uses
seed 42, and follows the fixed counterbalanced schedule in protocol.json.
The native configuration includes an additional filter-stage inflation layer;
the custom configuration uses the existing inflation layer after its plugin.

Metrics
Travel time is measured in simulation seconds from the first odometry sample
with abs(linear_x) > 0.01 after goal acceptance to the terminal callback.
Travel distance sums planar odometry displacements within that same interval.
Reported summaries use five trials per condition and sample SD (ddof = 1).

Verification
From the repository root, or the extracted keepout-evidence directory, run:
  python3 tools/verify_keepout.py
Python's standard library is sufficient; ROS and Gazebo are not required.
To check distribution file integrity from data/keepout-comparison, run:
  sha256sum -c SHA256SUMS

Provenance
Numerical records are unchanged. Usernames, hostnames, and local filesystem
paths in selected metadata and configuration files are anonymized. The release
manifest records original and public-copy SHA256 hashes for source artifacts.
Hashes embedded in original audit/manifests refer to pre-anonymized files;
use public_sha256 in release_manifest.json for public-copy integrity checks.
SHA256SUMS also covers the generated README and release manifest.

record_verification.json records checks performed on supplied records before
publication, separately from the experiment team's audit. The bundled script
recalculates travel metrics, sample statistics, and source-artifact integrity.
These checks do not constitute a simulator rerun or independent certification.
Ground-truth samples outside the zone do not establish continuous collision
freedom. Costmap arrays are included as evidence, without costmap figures.

This is a recorded-evidence package, not a complete simulator rerun package.
Simulator binaries, external maps/models, full logs, pilot runs, and unrelated
cohorts are omitted. No new experiments were performed for this release.
