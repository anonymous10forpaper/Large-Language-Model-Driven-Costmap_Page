"""Export the reference map using the actual Policy Bridge GUI renderer."""

import argparse
from dataclasses import asdict
import hashlib
import json
import math
import os
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy-bridge-src", type=Path, required=True)
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    sys.path.insert(0, str(args.policy_bridge_src.resolve()))
    from PyQt5.QtCore import QRectF
    from PyQt5.QtGui import QColor, QFont, QImage, QPainter
    from PyQt5.QtWidgets import QApplication
    from policy_bridge.waypoint_map import load_map_annotations, load_ros_map_yaml
    from policy_bridge.waypoint_map_gui import WaypointMapView

    app = QApplication([])
    app.setFont(QFont("DejaVu Sans", 10))
    spec = load_ros_map_yaml(args.map)
    annotations = load_map_annotations(args.annotations)
    if not annotations.waypoints or not annotations.zones:
        raise ValueError("The reference map requires saved waypoints and zones")
    view = WaypointMapView()
    view.set_map(spec)
    view.set_waypoints(annotations.waypoints)
    view.set_zones(annotations.zones)
    app.processEvents()

    # Render the GUI scene at 2x density without editor controls or viewport margins.
    scale = 2
    width, height = view.image_width, view.image_height
    image = QImage(width * scale, height * scale, QImage.Format_ARGB32)
    image.setDevicePixelRatio(scale)
    image.fill(QColor("white"))
    painter = QPainter(image)
    painter.setRenderHint(QPainter.Antialiasing, True)
    view.scene().render(painter, QRectF(0, 0, width, height), view.sceneRect())
    painter.end()

    positions = {}
    for name, (x, y, yaw) in annotations.waypoints.items():
        pixel = spec.world_to_pixel(x, y, height)
        if view._marker_pixels.get(name) != pixel:
            raise ValueError(f"Waypoint is missing from the GUI scene: {name}")
        roundtrip = spec.pixel_to_world(*pixel, height)
        if not all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip((x, y), roundtrip)):
            raise ValueError(f"Coordinate round-trip failed: {name}")
        output_pixel = [value * scale for value in pixel]
        color = image.pixelColor(*(round(value) for value in output_pixel))
        if color.name() != "#22836a":
            raise ValueError(f"Rendered waypoint center is not at its expected pixel: {name}")
        positions[name] = {"x": x, "y": y, "yaw": yaw, "image_pixel": output_pixel}

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if not image.save(str(args.output), "PNG"):
        raise OSError(f"Could not save {args.output}")

    def source(path):
        return {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

    metadata = {
        "description": "Reference map rendered from the Policy Bridge GUI scene, not a schematic.",
        "sources": [source(args.map), source(spec.image_path), source(args.annotations)],
        "renderer": "policy_bridge.waypoint_map_gui.WaypointMapView",
        "resolution_m_per_source_pixel": spec.resolution,
        "origin": [spec.origin_x, spec.origin_y, spec.origin_yaw],
        "source_image_size": [width, height],
        "output_image_size": [image.width(), image.height()],
        "render_scale": scale,
        "waypoints": positions,
        "zones": {name: asdict(bounds) for name, bounds in annotations.zones.items()},
    }
    args.output.with_suffix(".json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Saved {args.output}: {image.width()} x {image.height()}, {len(positions)} checked waypoints")


if __name__ == "__main__":
    main()
