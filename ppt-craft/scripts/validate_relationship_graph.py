#!/usr/bin/env python3
"""Validate a PPT Craft relationship-graph contract JSON before rendering."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


VALID_EXPORTS = {"pptx-native", "intentional-raster", "html-only"}
VALID_ROUTES = {"straight", "orthogonal", "elbow", "dogleg", "avoid", "curve", "bezier", "cubic"}
VALID_ANCHORS = {"auto", "left", "right", "top", "bottom", "center"}


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"relationship-graph invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("relationship-graph must be a JSON object")
    return data


def box_valid(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and all(isinstance(value.get(key), (int, float)) for key in ("x", "y", "w", "h"))
        and value["w"] > 0
        and value["h"] > 0
    )


def size_valid(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and all(isinstance(value.get(key), (int, float)) for key in ("w", "h"))
        and value["w"] > 0
        and value["h"] > 0
    )


def validate(
    data: dict[str, Any],
    *,
    require_native: bool,
    require_active_path: bool,
    min_layers: int,
    base_dir: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    for key in ("version", "graph_id", "purpose", "layers", "nodes", "edges", "export_policy"):
        if key not in data:
            errors.append(f"missing required field: {key}")

    layers = data.get("layers")
    nodes = data.get("nodes")
    edges = data.get("edges")
    if not isinstance(layers, list) or not layers:
        errors.append("layers must be a non-empty array")
        layers = []
    if not isinstance(nodes, list) or not nodes:
        errors.append("nodes must be a non-empty array")
        nodes = []
    if not isinstance(edges, list):
        errors.append("edges must be an array")
        edges = []

    layer_ids: set[str] = set()
    for index, layer in enumerate(layers, start=1):
        if not isinstance(layer, dict):
            errors.append(f"layers[{index}] must be an object")
            continue
        layer_id = str(layer.get("id") or "").strip()
        if not layer_id:
            errors.append(f"layers[{index}] missing id")
            continue
        if layer_id in layer_ids:
            errors.append(f"duplicate layer id: {layer_id}")
        layer_ids.add(layer_id)
        if not str(layer.get("name") or "").strip():
            errors.append(f"layer {layer_id} missing name")
        if not str(layer.get("role") or "").strip():
            errors.append(f"layer {layer_id} missing role")

    if len(layer_ids) < min_layers:
        errors.append(f"expected at least {min_layers} graph layers, found {len(layer_ids)}")

    node_ids: set[str] = set()
    for index, node in enumerate(nodes, start=1):
        if not isinstance(node, dict):
            errors.append(f"nodes[{index}] must be an object")
            continue
        node_id = str(node.get("id") or "").strip()
        if not node_id:
            errors.append(f"nodes[{index}] missing id")
            continue
        if node_id in node_ids:
            errors.append(f"duplicate node id: {node_id}")
        node_ids.add(node_id)
        layer = str(node.get("layer") or "").strip()
        if not layer:
            errors.append(f"node {node_id} missing layer")
        elif layer not in layer_ids:
            errors.append(f"node {node_id} references unknown layer: {layer}")
        if not str(node.get("label") or "").strip():
            errors.append(f"node {node_id} missing label")
        if not box_valid(node.get("box")):
            errors.append(f"node {node_id} missing valid box")
        collapsed_members = node.get("collapsed_members")
        if collapsed_members is not None and not isinstance(collapsed_members, list):
            errors.append(f"node {node_id} collapsed_members must be an array when present")

    swimlanes = data.get("swimlanes")
    swimlane_ids: set[str] = set()
    if swimlanes is not None:
        if not isinstance(swimlanes, list):
            errors.append("swimlanes must be an array when present")
        else:
            for index, lane in enumerate(swimlanes, start=1):
                if not isinstance(lane, dict):
                    errors.append(f"swimlanes[{index}] must be an object")
                    continue
                lane_id = str(lane.get("id") or "").strip()
                if not lane_id:
                    errors.append(f"swimlanes[{index}] missing id")
                    continue
                if lane_id in swimlane_ids:
                    errors.append(f"duplicate swimlane id: {lane_id}")
                swimlane_ids.add(lane_id)
                if not str(lane.get("name") or "").strip():
                    errors.append(f"swimlane {lane_id} missing name")

    subgraphs = data.get("subgraphs")
    if subgraphs is not None:
        if not isinstance(subgraphs, list):
            errors.append("subgraphs must be an array when present")
        else:
            subgraph_ids: set[str] = set()
            for index, subgraph in enumerate(subgraphs, start=1):
                if not isinstance(subgraph, dict):
                    errors.append(f"subgraphs[{index}] must be an object")
                    continue
                subgraph_id = str(subgraph.get("id") or "").strip()
                if not subgraph_id:
                    errors.append(f"subgraphs[{index}] missing id")
                    continue
                if subgraph_id in subgraph_ids:
                    errors.append(f"duplicate subgraph id: {subgraph_id}")
                subgraph_ids.add(subgraph_id)
                members = subgraph.get("members")
                if not isinstance(members, list) or not members:
                    errors.append(f"subgraph {subgraph_id} members must be a non-empty array")
                else:
                    for member in members:
                        if str(member) not in node_ids:
                            errors.append(f"subgraph {subgraph_id} references unknown member node: {member}")
                lane = str(subgraph.get("swimlane") or "").strip()
                if lane and swimlane_ids and lane not in swimlane_ids:
                    errors.append(f"subgraph {subgraph_id} references unknown swimlane: {lane}")

    edge_ids: set[str] = set()
    active_edges = 0
    native_edges = 0
    for index, edge in enumerate(edges, start=1):
        if not isinstance(edge, dict):
            errors.append(f"edges[{index}] must be an object")
            continue
        edge_id = str(edge.get("id") or "").strip()
        if not edge_id:
            errors.append(f"edges[{index}] missing id")
            continue
        if edge_id in edge_ids:
            errors.append(f"duplicate edge id: {edge_id}")
        edge_ids.add(edge_id)
        start = str(edge.get("from") or "").strip()
        end = str(edge.get("to") or "").strip()
        if start not in node_ids:
            errors.append(f"edge {edge_id} starts from unknown node: {start}")
        if end not in node_ids:
            errors.append(f"edge {edge_id} points to unknown node: {end}")
        layer = str(edge.get("layer") or "").strip()
        if not layer:
            errors.append(f"edge {edge_id} missing layer")
        elif layer not in layer_ids:
            errors.append(f"edge {edge_id} references unknown layer: {layer}")
        if not str(edge.get("relation") or "").strip():
            errors.append(f"edge {edge_id} missing relation")
        export = str(edge.get("export") or "").strip()
        if export not in VALID_EXPORTS:
            errors.append(f"edge {edge_id} export must be one of: {', '.join(sorted(VALID_EXPORTS))}")
        if export == "pptx-native":
            native_edges += 1
        route = str(edge.get("route") or "").strip()
        if route and route not in VALID_ROUTES:
            errors.append(f"edge {edge_id} route must be one of: {', '.join(sorted(VALID_ROUTES))}")
        route_bend = edge.get("route_bend")
        if route_bend is not None and (not isinstance(route_bend, (int, float)) or not 0 <= route_bend <= 1):
            errors.append(f"edge {edge_id} route_bend must be a number between 0 and 1")
        loop_side = str(edge.get("loop_side") or "").strip()
        if loop_side and loop_side not in {"top", "bottom"}:
            errors.append(f"edge {edge_id} loop_side must be top or bottom")
        for field in ("anchor_from", "anchor_to"):
            anchor = str(edge.get(field) or "").strip()
            if anchor and anchor not in VALID_ANCHORS:
                errors.append(f"edge {edge_id} {field} must be one of: {', '.join(sorted(VALID_ANCHORS))}")
        label_position = edge.get("label_position")
        if label_position is not None and (not isinstance(label_position, (int, float)) or not 0 <= label_position <= 1):
            errors.append(f"edge {edge_id} label_position must be a number between 0 and 1")
        label_priority = edge.get("label_priority")
        if label_priority is not None and (not isinstance(label_priority, int) or not 1 <= label_priority <= 5):
            errors.append(f"edge {edge_id} label_priority must be an integer from 1 to 5")
        bundle = edge.get("bundle")
        if bundle is not None and not isinstance(bundle, (str, bool)):
            errors.append(f"edge {edge_id} bundle must be a string id or boolean")
        avoid = edge.get("avoid")
        if avoid is not None:
            if not isinstance(avoid, list):
                errors.append(f"edge {edge_id} avoid must be an array of node ids")
            else:
                for node_id in avoid:
                    if str(node_id) not in node_ids:
                        errors.append(f"edge {edge_id} avoid references unknown node: {node_id}")
        if edge.get("active") is True:
            active_edges += 1
            if require_native and export != "pptx-native":
                errors.append(f"active edge {edge_id} must export as pptx-native")

    policy = data.get("export_policy")
    if not isinstance(policy, dict):
        errors.append("export_policy must be an object")
    else:
        default_export = str(policy.get("default_edge_export") or "").strip()
        if default_export not in VALID_EXPORTS:
            errors.append("export_policy.default_edge_export must be pptx-native, intentional-raster, or html-only")
        if require_native and default_export != "pptx-native":
            errors.append("export_policy.default_edge_export must be pptx-native for this route")

    if require_active_path and active_edges == 0:
        errors.append("at least one edge must be active for viewer reading order")
    if require_native and edges and native_edges == 0:
        errors.append("native PPTX route requires at least one pptx-native edge")

    views = data.get("views")
    if views is not None:
        if not isinstance(views, list):
            errors.append("views must be an array when present")
        else:
            view_ids: set[str] = set()
            subgraph_ids = {
                str(subgraph.get("id") or "")
                for subgraph in data.get("subgraphs", []) or []
                if isinstance(subgraph, dict) and subgraph.get("id")
            }
            for index, view in enumerate(views, start=1):
                if not isinstance(view, dict):
                    errors.append(f"views[{index}] must be an object")
                    continue
                view_id = str(view.get("id") or "").strip()
                if not view_id:
                    errors.append(f"views[{index}] missing id")
                elif view_id in view_ids:
                    errors.append(f"duplicate view id: {view_id}")
                view_ids.add(view_id)
                if not str(view.get("title") or "").strip():
                    errors.append(f"view {view_id or index} missing title")
                referenced_nodes: set[str] = set()
                referenced_edges: set[str] = set()
                for field in ("include_nodes", "focus_nodes"):
                    values = view.get(field)
                    if values is not None and not isinstance(values, list):
                        errors.append(f"view {view_id or index} {field} must be an array")
                        continue
                    for node_id in values or []:
                        if str(node_id) not in node_ids:
                            errors.append(f"view {view_id or index} {field} references unknown node: {node_id}")
                        referenced_nodes.add(str(node_id))
                for field in ("include_edges", "focus_edges", "active_edges", "active_path_edges"):
                    values = view.get(field)
                    if values is not None and not isinstance(values, list):
                        errors.append(f"view {view_id or index} {field} must be an array")
                        continue
                    for edge_id in values or []:
                        if str(edge_id) not in edge_ids:
                            errors.append(f"view {view_id or index} {field} references unknown edge: {edge_id}")
                        referenced_edges.add(str(edge_id))
                collapse_values = view.get("collapse_subgraphs")
                if collapse_values is not None and not isinstance(collapse_values, list):
                    errors.append(f"view {view_id or index} collapse_subgraphs must be an array")
                else:
                    for subgraph_id in collapse_values or []:
                        if str(subgraph_id) not in subgraph_ids:
                            errors.append(f"view {view_id or index} collapse_subgraphs references unknown subgraph: {subgraph_id}")
                visual_slots = view.get("visual_slots")
                if visual_slots is not None and not isinstance(visual_slots, list):
                    errors.append(f"view {view_id or index} visual_slots must be an array")
                elif isinstance(visual_slots, list):
                    slot_ids: set[str] = set()
                    for slot_index, slot in enumerate(visual_slots, start=1):
                        if not isinstance(slot, dict):
                            errors.append(f"view {view_id or index} visual_slots[{slot_index}] must be an object")
                            continue
                        slot_id = str(slot.get("id") or "").strip()
                        if not slot_id:
                            errors.append(f"view {view_id or index} visual_slots[{slot_index}] missing id")
                        elif slot_id in slot_ids:
                            errors.append(f"view {view_id or index} duplicate visual slot id: {slot_id}")
                        slot_ids.add(slot_id)
                        if not box_valid(slot.get("box")):
                            errors.append(f"view {view_id or index} visual slot {slot_id or slot_index} missing valid box")
                        fit = str(slot.get("fit") or "").strip()
                        if fit and fit not in {"cover", "contain", "fill", "scale-down"}:
                            errors.append(f"view {view_id or index} visual slot {slot_id or slot_index} fit must be cover, contain, fill, or scale-down")
                        opacity = slot.get("opacity")
                        if opacity is not None and (not isinstance(opacity, (int, float)) or not 0 <= opacity <= 1):
                            errors.append(f"view {view_id or index} visual slot {slot_id or slot_index} opacity must be between 0 and 1")
                        blend_mode = str(slot.get("blend_mode") or "").strip()
                        if blend_mode and blend_mode not in {"normal", "multiply", "screen", "overlay", "soft-light", "lighten"}:
                            errors.append(f"view {view_id or index} visual slot {slot_id or slot_index} has unsupported blend_mode: {blend_mode}")
                        src = str(slot.get("src") or "").strip()
                        if src and base_dir and not (src.startswith(("http://", "https://", "data:", "/"))):
                            if not (base_dir / src).exists():
                                errors.append(f"view {view_id or index} visual slot {slot_id or slot_index} src not found: {src}")
                        source = str(slot.get("source") or slot.get("source_image") or "").strip()
                        if source and base_dir and not (source.startswith(("http://", "https://", "data:", "/"))):
                            if not (base_dir / source).exists():
                                errors.append(f"view {view_id or index} visual slot {slot_id or slot_index} source not found: {source}")
                        for field in ("crop_box", "source_crop"):
                            if slot.get(field) is not None and not box_valid(slot.get(field)):
                                errors.append(f"view {view_id or index} visual slot {slot_id or slot_index} {field} must be a valid box")
                        for field in ("output_size", "asset_size"):
                            if slot.get(field) is not None and not size_valid(slot.get(field)):
                                errors.append(f"view {view_id or index} visual slot {slot_id or slot_index} {field} must be a valid size")
                        for field in ("transparent_threshold", "transparent_chroma", "transparent_softness"):
                            value = slot.get(field)
                            if value is not None and (not isinstance(value, (int, float)) or not 0 <= value <= 255):
                                errors.append(f"view {view_id or index} visual slot {slot_id or slot_index} {field} must be between 0 and 255")
                if not referenced_nodes and not referenced_edges:
                    errors.append(f"view {view_id or index} must reference at least one node or edge")

    layout_policy = data.get("layout_policy")
    if layout_policy is not None and not isinstance(layout_policy, dict):
        errors.append("layout_policy must be an object when present")
    elif isinstance(layout_policy, dict):
        edge_bundling = layout_policy.get("edge_bundling")
        if edge_bundling is not None and not isinstance(edge_bundling, dict):
            errors.append("layout_policy.edge_bundling must be an object when present")
        elif isinstance(edge_bundling, dict):
            min_edges = edge_bundling.get("min_edges")
            if min_edges is not None and (not isinstance(min_edges, int) or min_edges < 2):
                errors.append("layout_policy.edge_bundling.min_edges must be an integer >= 2")
        label_placement = layout_policy.get("label_placement")
        if label_placement is not None and not isinstance(label_placement, dict):
            errors.append("layout_policy.label_placement must be an object when present")
        node_crowding = layout_policy.get("node_crowding")
        if node_crowding is not None and not isinstance(node_crowding, dict):
            errors.append("layout_policy.node_crowding must be an object when present")
        edge_density = layout_policy.get("edge_density")
        if edge_density is not None and not isinstance(edge_density, dict):
            errors.append("layout_policy.edge_density must be an object when present")
        subgraph_collapse = layout_policy.get("subgraph_collapse")
        if subgraph_collapse is not None and not isinstance(subgraph_collapse, dict):
            errors.append("layout_policy.subgraph_collapse must be an object when present")

    active_paths = data.get("active_paths", [])
    if active_paths is not None and not isinstance(active_paths, list):
        errors.append("active_paths must be an array when present")
    elif isinstance(active_paths, list):
        for index, path_item in enumerate(active_paths, start=1):
            if not isinstance(path_item, dict):
                errors.append(f"active_paths[{index}] must be an object")
                continue
            for edge_id in path_item.get("edges", []):
                if edge_id not in edge_ids:
                    errors.append(f"active path {path_item.get('id', index)} references unknown edge: {edge_id}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--require-native", action="store_true")
    parser.add_argument("--require-active-path", action="store_true")
    parser.add_argument("--min-layers", type=int, default=2)
    args = parser.parse_args()

    data = read_json(args.path)
    errors = validate(
        data,
        require_native=args.require_native,
        require_active_path=args.require_active_path,
        min_layers=args.min_layers,
        base_dir=args.path.resolve().parent,
    )
    if errors:
        print("relationship-graph-validation-failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"relationship-graph-validation-ok path={args.path.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
