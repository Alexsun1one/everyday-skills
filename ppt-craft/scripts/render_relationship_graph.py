#!/usr/bin/env python3
"""Render a relationship-graph.json contract into editable-oriented HTML slides.

The renderer intentionally uses only the Python standard library. It reads the
semantic graph contract, computes 960 x 540 pt slide layouts from layer order,
node roles, priorities, active paths, and optional graph views, then writes:

- slides/01-relationship-autolayout.html
- index.html
- layout-blueprint.json
"""

from __future__ import annotations

import argparse
import copy
import html
import json
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


STAGE_W = 960.0
STAGE_H = 540.0

CLAIM = {"x": 40.0, "y": 40.0, "w": 258.0, "h": 152.0}
EVIDENCE = {"x": 40.0, "y": 400.0, "w": 258.0, "h": 92.0}
GRAPH = {"x": 330.0, "y": 44.0, "w": 590.0, "h": 386.0}
LOOP = {"x": 330.0, "y": 452.0, "w": 590.0, "h": 48.0}

ROLE_COLORS = {
    "context": "#8FB6CF",
    "input": "#63CAFF",
    "actor": "#9CE3FF",
    "operation": "#EDBB66",
    "evidence": "#77E6B6",
    "risk": "#F4966F",
    "decision": "#B9F27D",
    "output": "#B9F27D",
    "feedback": "#8FB6CF",
    "loop": "#8FB6CF",
    "support": "#A78BFA",
}

RELATION_COLORS = {
    "feeds": "#63CAFF",
    "filters": "#F4966F",
    "transforms": "#EDBB66",
    "proves": "#77E6B6",
    "blocks": "#F4966F",
    "triggers": "#63CAFF",
    "compares": "#A8B3C7",
    "depends-on": "#A8B3C7",
    "amplifies": "#A78BFA",
    "loops": "#8FB6CF",
    "contradicts": "#F87171",
    "annotates": "#A8B3C7",
}

ROLE_Y_ANCHOR = {
    "context": 0.35,
    "input": 0.38,
    "actor": 0.4,
    "operation": 0.42,
    "evidence": 0.72,
    "risk": 0.22,
    "decision": 0.55,
    "output": 0.6,
    "feedback": 0.84,
    "loop": 0.84,
    "support": 0.66,
}

SWIMLANE_COLORS = [
    "rgba(99, 202, 255, 0.08)",
    "rgba(119, 230, 182, 0.08)",
    "rgba(237, 187, 102, 0.08)",
    "rgba(244, 150, 111, 0.08)",
    "rgba(167, 139, 250, 0.08)",
]


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float

    @property
    def cx(self) -> float:
        return self.x + self.w / 2

    @property
    def cy(self) -> float:
        return self.y + self.h / 2


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class LabelPlacement:
    position: float
    offset: Point
    width: float
    height: float
    score: float
    box: Box


@dataclass(frozen=True)
class RenderedNode:
    data: dict[str, Any]
    box: Box
    active: bool
    color: str


@dataclass(frozen=True)
class RenderedEdge:
    data: dict[str, Any]
    box: Box
    start: Point
    end: Point
    points: tuple[Point, ...]
    anchor_from: str
    anchor_to: str
    route: str
    label: str
    label_placement: LabelPlacement | None
    bundle_id: str
    bundle_lane: int
    color: str
    width: float
    dash: str
    arrow: str
    active: bool


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def pt(value: float) -> str:
    rounded = round(value, 2)
    if abs(rounded - round(rounded)) < 0.01:
        return str(int(round(rounded)))
    return f"{rounded:.2f}".rstrip("0").rstrip(".")


def browser_px(value_pt: float) -> str:
    return pt(value_pt * 4 / 3)


def pct(value: float, size: float) -> str:
    if size <= 0:
        return "0%"
    return f"{(value / size) * 100:.1f}%"


def clamp(value: float, minimum: float, maximum: float) -> float:
    if maximum < minimum:
        return minimum
    return max(minimum, min(maximum, value))


def intersects(a: Box, b: Box, padding: float = 0.0) -> bool:
    return not (
        a.x + a.w < b.x - padding
        or b.x + b.w < a.x - padding
        or a.y + a.h < b.y - padding
        or b.y + b.h < a.y - padding
    )


def intersection_area(a: Box, b: Box, padding: float = 0.0) -> float:
    left = max(a.x, b.x - padding)
    top = max(a.y, b.y - padding)
    right = min(a.x + a.w, b.x + b.w + padding)
    bottom = min(a.y + a.h, b.y + b.h + padding)
    return max(0.0, right - left) * max(0.0, bottom - top)


def box_outside_penalty(box: Box, bounds: dict[str, float]) -> float:
    left = max(0.0, bounds["x"] - box.x)
    top = max(0.0, bounds["y"] - box.y)
    right = max(0.0, box.x + box.w - (bounds["x"] + bounds["w"]))
    bottom = max(0.0, box.y + box.h - (bounds["y"] + bounds["h"]))
    return left + top + right + bottom


def edge_strength_weight(edge: dict[str, Any]) -> float:
    strength = str(edge.get("strength") or "normal")
    return {"weak": 0.65, "normal": 1.0, "strong": 1.35, "critical": 1.7}.get(strength, 1.0)


def edge_priority_weight(edge: dict[str, Any]) -> float:
    return edge_strength_weight(edge) + (1.5 if truthy(edge.get("active")) else 0.0)


def median(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def most_common(values: list[str], fallback: str = "") -> str:
    cleaned = [value for value in values if value]
    if not cleaned:
        return fallback
    return Counter(cleaned).most_common(1)[0][0]


def css_class(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip())
    return value.strip("-") or "item"


def slug(value: str, fallback: str = "relationship-autolayout") -> str:
    cleaned = css_class(value.lower())
    return cleaned or fallback


def read_graph(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"relationship graph is invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("relationship graph must be a JSON object")
    return data


def truthy(value: Any) -> bool:
    return value is True or str(value).lower() == "true"


def node_swimlane_id(node: dict[str, Any]) -> str:
    return str(node.get("swimlane") or node.get("group") or node.get("cluster") or "").strip()


def swimlane_records(graph: dict[str, Any], nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    policy = graph.get("layout_policy") if isinstance(graph.get("layout_policy"), dict) else {}
    configured = graph.get("swimlanes") or policy.get("swimlanes")
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    if isinstance(configured, list):
        for index, lane in enumerate(configured):
            if not isinstance(lane, dict):
                continue
            lane_id = str(lane.get("id") or "").strip()
            if not lane_id or lane_id in seen:
                continue
            seen.add(lane_id)
            records.append({
                "id": lane_id,
                "name": str(lane.get("name") or lane_id),
                "order": int(lane.get("order") if isinstance(lane.get("order"), int) else index),
                "color": str(lane.get("color") or SWIMLANE_COLORS[len(records) % len(SWIMLANE_COLORS)]),
            })
    for node in nodes:
        lane_id = node_swimlane_id(node)
        if lane_id and lane_id not in seen:
            seen.add(lane_id)
            records.append({
                "id": lane_id,
                "name": lane_id.replace("-", " ").title(),
                "order": len(records),
                "color": SWIMLANE_COLORS[len(records) % len(SWIMLANE_COLORS)],
            })
    return sorted(records, key=lambda item: (item.get("order", 9999), str(item["id"])))


def apply_subgraph_collapses(graph: dict[str, Any]) -> dict[str, Any]:
    """Rewrite a graph so declared collapsed subgraphs become aggregate nodes."""

    subgraphs = graph.get("subgraphs") or []
    if not isinstance(subgraphs, list):
        return {"collapsed_subgraphs": 0, "collapsed_members": 0, "collapsed_internal_edges": 0}

    nodes = [node for node in graph.get("nodes", []) if isinstance(node, dict) and node.get("id")]
    node_by_id = {str(node["id"]): node for node in nodes}
    member_to_group: dict[str, str] = {}
    collapsed_records: list[dict[str, Any]] = []

    for subgraph in subgraphs:
        if not isinstance(subgraph, dict) or not truthy(subgraph.get("collapsed")):
            continue
        group_id = str(subgraph.get("id") or "").strip()
        if not group_id:
            continue
        members = [
            str(member)
            for member in subgraph.get("members", []) or []
            if str(member) in node_by_id and str(member) != group_id
        ]
        if not members:
            continue
        source_nodes = [node_by_id[member] for member in members]
        if group_id not in node_by_id:
            layer = str(subgraph.get("layer") or most_common([str(node.get("layer") or "") for node in source_nodes], "graph"))
            role = str(subgraph.get("role") or most_common([str(node.get("role") or "") for node in source_nodes], "support"))
            swimlane = str(subgraph.get("swimlane") or most_common([node_swimlane_id(node) for node in source_nodes], ""))
            aggregate_node = {
                "id": group_id,
                "label": str(subgraph.get("name") or subgraph.get("label") or group_id),
                "layer": layer,
                "role": role,
                "priority": max([int(node.get("priority") or 3) for node in source_nodes] + [3]),
                "box": {"x": 0, "y": 0, "w": 1, "h": 1},
                "collapsed": True,
                "collapsed_members": members,
            }
            if swimlane:
                aggregate_node["swimlane"] = swimlane
            nodes.append(aggregate_node)
            node_by_id[group_id] = aggregate_node
        else:
            node_by_id[group_id]["collapsed"] = True
            node_by_id[group_id]["collapsed_members"] = members
            if subgraph.get("name") and not node_by_id[group_id].get("label"):
                node_by_id[group_id]["label"] = str(subgraph["name"])
        for member in members:
            member_to_group[member] = group_id
        collapsed_records.append({"id": group_id, "members": members})

    if not member_to_group:
        return {"collapsed_subgraphs": 0, "collapsed_members": 0, "collapsed_internal_edges": 0}

    graph["nodes"] = [
        node
        for node in nodes
        if str(node.get("id") or "") not in member_to_group
    ]

    rewritten_edges: list[dict[str, Any]] = []
    skipped_internal = 0
    skipped_duplicates = 0
    collapsed_edge_index: dict[tuple[str, str, str, str], int] = {}
    for edge in graph.get("edges", []) or []:
        if not isinstance(edge, dict):
            continue
        start = str(edge.get("from") or "")
        end = str(edge.get("to") or "")
        rewritten = dict(edge)
        collapsed = False
        if start in member_to_group:
            rewritten["from"] = member_to_group[start]
            collapsed = True
        if end in member_to_group:
            rewritten["to"] = member_to_group[end]
            collapsed = True
        if rewritten.get("from") == rewritten.get("to"):
            skipped_internal += 1
            continue
        if collapsed:
            rewritten["collapsed_endpoint"] = True
            rewritten.setdefault("bundle", f"collapsed-{rewritten['from']}-to-{rewritten['to']}")
            key = (
                str(rewritten.get("from") or ""),
                str(rewritten.get("to") or ""),
                str(rewritten.get("relation") or ""),
                str(rewritten.get("layer") or ""),
            )
            if key in collapsed_edge_index:
                existing_index = collapsed_edge_index[key]
                if truthy(rewritten.get("active")) and not truthy(rewritten_edges[existing_index].get("active")):
                    rewritten_edges[existing_index] = rewritten
                skipped_duplicates += 1
                continue
            collapsed_edge_index[key] = len(rewritten_edges)
        rewritten_edges.append(rewritten)
    graph["edges"] = rewritten_edges

    valid_edges = {str(edge.get("id") or "") for edge in rewritten_edges}
    for path_item in graph.get("active_paths", []) or []:
        if isinstance(path_item, dict) and isinstance(path_item.get("edges"), list):
            path_item["edges"] = [edge_id for edge_id in path_item["edges"] if str(edge_id) in valid_edges]

    return {
        "collapsed_subgraphs": len(collapsed_records),
        "collapsed_members": len(member_to_group),
        "collapsed_internal_edges": skipped_internal,
        "collapsed_duplicate_edges": skipped_duplicates,
        "collapsed_ids": [record["id"] for record in collapsed_records],
    }


def normalize_graph(graph: dict[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(graph)
    normalized["_collapse_diagnostics"] = apply_subgraph_collapses(normalized)
    return normalized


def graph_views(graph: dict[str, Any]) -> list[dict[str, Any]]:
    configured = graph.get("views")
    if not isinstance(configured, list) or not configured:
        return [{"id": "relationship-autolayout", "_default": True}]
    views: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, view in enumerate(configured, start=1):
        if not isinstance(view, dict):
            continue
        view_id = slug(str(view.get("id") or f"view-{index}"), f"view-{index}")
        if view_id in seen:
            view_id = f"{view_id}-{index}"
        seen.add(view_id)
        views.append({**view, "id": view_id})
    return views or [{"id": "relationship-autolayout", "_default": True}]


def list_field(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def filtered_graph_for_view(base_graph: dict[str, Any], view: dict[str, Any]) -> dict[str, Any]:
    graph = copy.deepcopy(base_graph)
    if view.get("_default"):
        graph.pop("views", None)
        graph["_view"] = {"id": "relationship-autolayout", "index_title": graph_title(graph)}
        return graph

    node_ids = set(list_field(view.get("include_nodes")) + list_field(view.get("focus_nodes")))
    edge_ids = set(list_field(view.get("include_edges")) + list_field(view.get("focus_edges")))
    active_edges = set(list_field(view.get("active_edges")) + list_field(view.get("active_path_edges")))
    edge_ids.update(active_edges)

    all_edges = [edge for edge in graph.get("edges", []) or [] if isinstance(edge, dict)]
    if edge_ids:
        for edge in all_edges:
            if str(edge.get("id") or "") in edge_ids:
                node_ids.add(str(edge.get("from") or ""))
                node_ids.add(str(edge.get("to") or ""))

    node_by_id = {
        str(node.get("id") or ""): node
        for node in graph.get("nodes", []) or []
        if isinstance(node, dict) and node.get("id")
    }
    subgraphs = [item for item in graph.get("subgraphs", []) or [] if isinstance(item, dict)]
    explicit_collapse_ids = set(list_field(view.get("collapse_subgraphs")))
    if explicit_collapse_ids:
        for subgraph in subgraphs:
            if str(subgraph.get("id") or "") in explicit_collapse_ids:
                node_ids.update(str(member) for member in subgraph.get("members", []) or [])

    changed = True
    while changed:
        changed = False
        for subgraph in subgraphs:
            group_id = str(subgraph.get("id") or "")
            members = {str(member) for member in subgraph.get("members", []) or [] if str(member) in node_by_id}
            if not members:
                continue
            should_expand = group_id in node_ids or bool(members & node_ids)
            if explicit_collapse_ids and group_id not in explicit_collapse_ids and not bool(members & node_ids):
                should_expand = False
            if should_expand:
                before = len(node_ids)
                node_ids.update(members)
                changed = changed or len(node_ids) != before

    if node_ids:
        graph["nodes"] = [
            node
            for node in graph.get("nodes", []) or []
            if isinstance(node, dict) and str(node.get("id") or "") in node_ids
        ]
        kept_node_ids = {str(node.get("id") or "") for node in graph["nodes"]}
        if edge_ids:
            graph["edges"] = [
                edge
                for edge in all_edges
                if str(edge.get("id") or "") in edge_ids
                and str(edge.get("from") or "") in kept_node_ids
                and str(edge.get("to") or "") in kept_node_ids
            ]
        else:
            graph["edges"] = [
                edge
                for edge in all_edges
                if str(edge.get("from") or "") in kept_node_ids
                and str(edge.get("to") or "") in kept_node_ids
            ]
        used_layers = {str(node.get("layer") or "") for node in graph["nodes"]}
        graph["layers"] = [
            layer
            for layer in graph.get("layers", []) or []
            if isinstance(layer, dict) and str(layer.get("id") or "") in used_layers
        ]
        used_swimlanes = {node_swimlane_id(node) for node in graph["nodes"] if node_swimlane_id(node)}
        if isinstance(graph.get("swimlanes"), list):
            graph["swimlanes"] = [
                lane
                for lane in graph["swimlanes"]
                if isinstance(lane, dict) and str(lane.get("id") or "") in used_swimlanes
            ]
        graph["subgraphs"] = [
            subgraph
            for subgraph in subgraphs
            if {str(member) for member in subgraph.get("members", []) or []} & kept_node_ids
            or str(subgraph.get("id") or "") in explicit_collapse_ids
        ]

    kept_edge_ids = {str(edge.get("id") or "") for edge in graph.get("edges", []) or [] if isinstance(edge, dict)}
    if active_edges:
        for edge in graph.get("edges", []) or []:
            if isinstance(edge, dict):
                edge["active"] = str(edge.get("id") or "") in active_edges
        graph["active_paths"] = [{
            "id": f"{view['id']}-active",
            "edges": [edge_id for edge_id in list_field(view.get("active_edges")) + list_field(view.get("active_path_edges")) if edge_id in kept_edge_ids],
            "message": str(view.get("message") or view.get("purpose") or "Active edges mark the viewer reading path."),
        }]
    else:
        filtered_paths = []
        for path_item in graph.get("active_paths", []) or []:
            if not isinstance(path_item, dict):
                continue
            path_edges = [edge_id for edge_id in path_item.get("edges", []) or [] if str(edge_id) in kept_edge_ids]
            if path_edges:
                filtered_paths.append({**path_item, "edges": path_edges})
        graph["active_paths"] = filtered_paths

    if view.get("title"):
        graph["title"] = str(view["title"])
    if view.get("purpose"):
        graph["purpose"] = str(view["purpose"])
    if view.get("message") and not graph.get("active_paths"):
        graph["active_paths"] = [{"id": f"{view['id']}-message", "edges": [], "message": str(view["message"])}]

    graph.pop("views", None)
    graph["_view"] = {
        "id": str(view["id"]),
        "index_title": str(view.get("title") or graph_title(graph)),
        "purpose": str(view.get("purpose") or graph.get("purpose") or ""),
        "visual_slots": view.get("visual_slots") if isinstance(view.get("visual_slots"), list) else [],
    }
    return graph


def graph_visual_slots(graph: dict[str, Any]) -> list[dict[str, Any]]:
    view = graph.get("_view") if isinstance(graph.get("_view"), dict) else {}
    slots = view.get("visual_slots")
    if not isinstance(slots, list):
        return []
    clean: list[dict[str, Any]] = []
    for index, slot in enumerate(slots, start=1):
        if not isinstance(slot, dict):
            continue
        box = slot.get("box")
        if not isinstance(box, dict):
            continue
        if not all(isinstance(box.get(key), (int, float)) for key in ("x", "y", "w", "h")):
            continue
        if float(box["w"]) <= 0 or float(box["h"]) <= 0:
            continue
        clean.append({
            **slot,
            "id": str(slot.get("id") or f"visual-slot-{index}"),
            "box": {key: float(box[key]) for key in ("x", "y", "w", "h")},
            "fit": str(slot.get("fit") or "cover"),
            "transparent": truthy(slot.get("transparent")),
            "blend_mode": str(slot.get("blend_mode") or ("screen" if truthy(slot.get("transparent")) else "normal")),
            "crop": str(slot.get("crop") or ""),
        })
    return clean


def slot_src_for_html(src: str) -> str:
    src = src.strip()
    if not src:
        return ""
    if src.startswith(("http://", "https://", "data:", "/", "../", "./")):
        return src
    return f"../{src}"


def layer_records(graph: dict[str, Any]) -> list[dict[str, Any]]:
    records = [item for item in graph.get("layers", []) if isinstance(item, dict) and item.get("id")]
    seen = {str(item["id"]) for item in records}
    for node in graph.get("nodes", []):
        if not isinstance(node, dict):
            continue
        layer = str(node.get("layer") or "").strip()
        if layer and layer not in seen:
            records.append({"id": layer, "name": layer, "role": "support", "visual_treatment": "auto-added"})
            seen.add(layer)
    return records


def active_edge_order(graph: dict[str, Any]) -> tuple[dict[str, int], set[str]]:
    order: dict[str, int] = {}
    active: set[str] = set()
    cursor = 0
    for path_item in graph.get("active_paths", []) or []:
        if not isinstance(path_item, dict):
            continue
        for edge_id in path_item.get("edges", []) or []:
            edge_key = str(edge_id)
            active.add(edge_key)
            order.setdefault(edge_key, cursor)
            cursor += 1
    for edge in graph.get("edges", []) or []:
        if isinstance(edge, dict) and truthy(edge.get("active")):
            edge_id = str(edge.get("id") or "")
            if edge_id:
                active.add(edge_id)
                order.setdefault(edge_id, cursor)
                cursor += 1
    return order, active


def node_active_rank(graph: dict[str, Any], edge_order: dict[str, int]) -> dict[str, int]:
    ranks: dict[str, int] = {}
    for edge in graph.get("edges", []) or []:
        if not isinstance(edge, dict):
            continue
        edge_id = str(edge.get("id") or "")
        if edge_id not in edge_order:
            continue
        for endpoint in ("from", "to"):
            node_id = str(edge.get(endpoint) or "")
            if not node_id:
                continue
            ranks[node_id] = min(ranks.get(node_id, 9999), edge_order[edge_id])
    return ranks


def layer_crossings(graph: dict[str, Any], order_by_layer: dict[str, list[str]], layer_ids: list[str]) -> int:
    layer_index = {layer_id: index for index, layer_id in enumerate(layer_ids)}
    node_pos: dict[str, tuple[str, int]] = {}
    for layer_id, node_ids in order_by_layer.items():
        for index, node_id in enumerate(node_ids):
            node_pos[node_id] = (layer_id, index)
    crossings = 0
    buckets: dict[tuple[str, str], list[tuple[int, int, float]]] = {}
    for edge in graph.get("edges", []) or []:
        if not isinstance(edge, dict):
            continue
        start = str(edge.get("from") or "")
        end = str(edge.get("to") or "")
        if start not in node_pos or end not in node_pos:
            continue
        start_layer, start_index = node_pos[start]
        end_layer, end_index = node_pos[end]
        if start_layer == end_layer:
            continue
        if layer_index.get(start_layer, 0) > layer_index.get(end_layer, 0):
            key = (end_layer, start_layer)
            pair = (end_index, start_index, edge_priority_weight(edge))
        else:
            key = (start_layer, end_layer)
            pair = (start_index, end_index, edge_priority_weight(edge))
        buckets.setdefault(key, []).append(pair)
    for pairs in buckets.values():
        for index, first in enumerate(pairs):
            for second in pairs[index + 1:]:
                if (first[0] - second[0]) * (first[1] - second[1]) < 0:
                    crossings += 1
    return crossings


def optimized_node_order(
    graph: dict[str, Any],
    grouped: dict[str, list[dict[str, Any]]],
    layer_ids: list[str],
    ranks: dict[str, int],
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    def initial_sort(node: dict[str, Any]) -> tuple[int, int, int, str]:
        node_id = str(node.get("id") or "")
        rank = ranks.get(node_id, 9999)
        active_score = 0 if truthy(node.get("active")) or rank < 9999 else 1
        priority = int(node.get("priority") or 3)
        return (rank, active_score, -priority, node_id)

    order_by_layer = {
        layer_id: [str(node.get("id")) for node in sorted(grouped.get(layer_id, []), key=initial_sort)]
        for layer_id in layer_ids
    }
    original_order = {layer_id: list(node_ids) for layer_id, node_ids in order_by_layer.items()}
    before = layer_crossings(graph, order_by_layer, layer_ids)

    edge_records = [edge for edge in graph.get("edges", []) or [] if isinstance(edge, dict)]

    def neighbor_barycenter(node_id: str, layer_index: int, direction: int) -> float | None:
        neighbor_layer_index = layer_index + direction
        if neighbor_layer_index < 0 or neighbor_layer_index >= len(layer_ids):
            return None
        neighbor_layer = layer_ids[neighbor_layer_index]
        neighbor_positions = {nid: idx for idx, nid in enumerate(order_by_layer.get(neighbor_layer, []))}
        total = 0.0
        weight_total = 0.0
        for edge in edge_records:
            start = str(edge.get("from") or "")
            end = str(edge.get("to") or "")
            other = ""
            if start == node_id:
                other = end
            elif end == node_id:
                other = start
            if other and other in neighbor_positions:
                weight = edge_priority_weight(edge)
                total += neighbor_positions[other] * weight
                weight_total += weight
        if weight_total <= 0:
            return None
        return total / weight_total

    # Layered barycentric sweeps: cheap, deterministic, and explainable.
    for _ in range(6):
        for direction, indices in ((1, range(1, len(layer_ids))), (-1, range(len(layer_ids) - 2, -1, -1))):
            for layer_index in indices:
                layer_id = layer_ids[layer_index]
                ids = order_by_layer.get(layer_id, [])
                original_index = {node_id: index for index, node_id in enumerate(ids)}
                ids.sort(key=lambda node_id: (
                    neighbor_barycenter(node_id, layer_index, -direction)
                    if neighbor_barycenter(node_id, layer_index, -direction) is not None
                    else float(original_index[node_id]),
                    ranks.get(node_id, 9999),
                    original_index[node_id],
                    node_id,
                ))

    after = layer_crossings(graph, order_by_layer, layer_ids)
    if after > before:
        order_by_layer = original_order
        after = before

    node_by_id = {
        str(node.get("id")): node
        for bucket in grouped.values()
        for node in bucket
        if isinstance(node, dict) and node.get("id")
    }
    ordered = {
        layer_id: [node_by_id[node_id] for node_id in node_ids if node_id in node_by_id]
        for layer_id, node_ids in order_by_layer.items()
    }
    return ordered, {
        "crossings_before": before,
        "crossings_after": after,
        "crossings_reduced": max(0, before - after),
        "sweeps": 6,
    }


def layout_nodes(graph: dict[str, Any]) -> tuple[dict[str, RenderedNode], dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any]]:
    nodes = [item for item in graph.get("nodes", []) if isinstance(item, dict) and item.get("id")]
    layers = layer_records(graph)
    swimlanes = swimlane_records(graph, nodes)
    layer_by_id = {str(item["id"]): item for item in layers}
    layer_ids_with_nodes: list[str] = []
    for layer in layers:
        layer_id = str(layer["id"])
        if any(str(node.get("layer") or "") == layer_id for node in nodes):
            layer_ids_with_nodes.append(layer_id)
    for node in nodes:
        layer_id = str(node.get("layer") or "").strip()
        if layer_id and layer_id not in layer_ids_with_nodes:
            layer_ids_with_nodes.append(layer_id)
    if not layer_ids_with_nodes:
        layer_ids_with_nodes = ["graph"]

    edge_order, _active_edges = active_edge_order(graph)
    ranks = node_active_rank(graph, edge_order)

    node_count = max(1, len(nodes))
    layer_count = max(1, len(layer_ids_with_nodes))
    lane_layer_counts: Counter[tuple[str, str]] = Counter()
    lane_weights: dict[str, int] = {}
    for node in nodes:
        lane_id = node_swimlane_id(node)
        if lane_id:
            lane_layer_counts[(str(node.get("layer") or "graph"), lane_id)] += 1
    for (_layer_id, lane_id), count in lane_layer_counts.items():
        lane_weights[lane_id] = max(lane_weights.get(lane_id, 1), count)
    max_lane_bucket = max(lane_weights.values(), default=1)
    min_node_w = 72 if layer_count >= 7 else 84 if layer_count >= 6 else 92
    node_w = clamp((GRAPH["w"] - max(0, layer_count - 1) * 18) / layer_count, min_node_w, 116)
    if node_count > 12:
        node_w = min(node_w, 94 if layer_count >= 7 else 100)
    if swimlanes and max_lane_bucket >= 3:
        node_h = 20
    elif swimlanes and max_lane_bucket >= 2:
        node_h = 42 if node_count <= 10 else 30
    elif swimlanes and node_count > 12:
        node_h = 30
    else:
        node_h = 54 if node_count <= 10 else 46

    y_min = GRAPH["y"] + 48
    y_max = GRAPH["y"] + GRAPH["h"] - node_h - 20
    swimlane_geometry: dict[str, dict[str, Any]] = {}
    if swimlanes:
        lane_gap = 6.0
        available = max(80.0, y_max - y_min + node_h)
        weighted_available = max(80.0, available - lane_gap * (len(swimlanes) - 1))
        total_weight = sum(max(1, lane_weights.get(str(lane["id"]), 1)) for lane in swimlanes)
        cursor_y = y_min
        for index, lane in enumerate(swimlanes):
            weight = max(1, lane_weights.get(str(lane["id"]), 1))
            lane_h = max(node_h + 18.0, weighted_available * weight / max(1, total_weight))
            y = cursor_y
            swimlane_geometry[str(lane["id"])] = {
                "x": GRAPH["x"],
                "y": round(y, 2),
                "w": GRAPH["w"],
                "h": round(min(lane_h, GRAPH["y"] + GRAPH["h"] - y - 12), 2),
                "name": str(lane.get("name") or lane["id"]),
                "color": str(lane.get("color") or SWIMLANE_COLORS[index % len(SWIMLANE_COLORS)]),
                "order": index,
            }
            cursor_y += lane_h + lane_gap

    grouped: dict[str, list[dict[str, Any]]] = {layer_id: [] for layer_id in layer_ids_with_nodes}
    for node in nodes:
        grouped.setdefault(str(node.get("layer") or "graph"), []).append(node)
    ordered_by_layer, layout_diagnostics = optimized_node_order(graph, grouped, layer_ids_with_nodes, ranks)

    rendered: dict[str, RenderedNode] = {}
    layer_geometry: dict[str, dict[str, Any]] = {}

    for col, layer_id in enumerate(layer_ids_with_nodes):
        if layer_count == 1:
            x = GRAPH["x"] + (GRAPH["w"] - node_w) / 2
        else:
            x = GRAPH["x"] + col * ((GRAPH["w"] - node_w) / (layer_count - 1))
        layer = layer_by_id.get(layer_id, {"id": layer_id, "name": layer_id, "role": "support"})
        layer_geometry[layer_id] = {
            "x": round(x, 2),
            "name": str(layer.get("name") or layer_id),
            "role": str(layer.get("role") or "support"),
        }

        ordered = ordered_by_layer.get(layer_id, [])
        lane_buckets: dict[str, list[str]] = {}
        for bucket_node in ordered:
            lane_id = node_swimlane_id(bucket_node)
            if lane_id and lane_id in swimlane_geometry:
                lane_buckets.setdefault(lane_id, []).append(str(bucket_node.get("id") or ""))
        for row, node in enumerate(ordered):
            role = str(node.get("role") or layer.get("role") or "support")
            anchor = ROLE_Y_ANCHOR.get(role, 0.5)
            lane_id = node_swimlane_id(node)
            if lane_id and lane_id in swimlane_geometry:
                lane = swimlane_geometry[lane_id]
                bucket = lane_buckets.get(lane_id, [])
                row_in_lane = bucket.index(str(node.get("id") or "")) if str(node.get("id") or "") in bucket else 0
                lane_top = float(lane["y"]) + 9
                lane_bottom = float(lane["y"]) + float(lane["h"]) - node_h - 9
                if len(bucket) <= 1 or lane_bottom <= lane_top:
                    y = lane_top + max(0, lane_bottom - lane_top) / 2
                    y += (anchor - 0.5) * min(18, float(lane["h"]) * 0.18)
                else:
                    y = lane_top + row_in_lane * ((lane_bottom - lane_top) / (len(bucket) - 1))
                y = clamp(y, lane_top, max(lane_top, lane_bottom))
            elif len(ordered) == 1:
                y = y_min + anchor * max(0, y_max - y_min)
            else:
                y = y_min + row * ((y_max - y_min) / (len(ordered) - 1))
                y += (anchor - 0.5) * 42
            y = clamp(y, y_min, y_max)
            node_id = str(node["id"])
            active = truthy(node.get("active")) or ranks.get(node_id, 9999) < 9999
            color = ROLE_COLORS.get(role, ROLE_COLORS.get(str(layer.get("role") or ""), "#A8B3C7"))
            rendered[node_id] = RenderedNode(
                data=node,
                box=Box(x=x, y=y, w=node_w, h=node_h),
                active=active,
                color=color,
            )

    layout_diagnostics["swimlanes"] = len(swimlane_geometry)
    return rendered, layer_geometry, swimlane_geometry, layout_diagnostics


def anchor_between(start: Box, end: Box) -> tuple[Point, Point]:
    dx = end.cx - start.cx
    dy = end.cy - start.cy
    if abs(dx) >= abs(dy):
        first = Point(start.x + (start.w if dx >= 0 else 0), start.cy)
        second = Point(end.x if dx >= 0 else end.x + end.w, end.cy)
    else:
        first = Point(start.cx, start.y + (start.h if dy >= 0 else 0))
        second = Point(end.cx, end.y if dy >= 0 else end.y + end.h)
    return first, second


def anchor_sides(start: Box, end: Box) -> tuple[str, str]:
    dx = end.cx - start.cx
    dy = end.cy - start.cy
    if abs(dx) >= abs(dy):
        return ("right", "left") if dx >= 0 else ("left", "right")
    return ("bottom", "top") if dy >= 0 else ("top", "bottom")


def anchor_point(box: Box, anchor: str, fallback: Point) -> Point:
    anchor = anchor.lower()
    if anchor == "left":
        return Point(box.x, box.cy)
    if anchor == "right":
        return Point(box.x + box.w, box.cy)
    if anchor == "top":
        return Point(box.cx, box.y)
    if anchor == "bottom":
        return Point(box.cx, box.y + box.h)
    if anchor == "center":
        return Point(box.cx, box.cy)
    return fallback


def segment_aabb_intersects(a: Point, b: Point, box: Box, gap: float = 0.0) -> bool:
    min_x = min(a.x, b.x)
    max_x = max(a.x, b.x)
    min_y = min(a.y, b.y)
    max_y = max(a.y, b.y)
    return max_x >= box.x - gap and min_x <= box.x + box.w + gap and max_y >= box.y - gap and min_y <= box.y + box.h + gap


def orthogonal_points(start: Point, end: Point, bend: float = 0.5) -> tuple[Point, ...]:
    if abs(end.x - start.x) >= abs(end.y - start.y):
        mid_x = start.x + (end.x - start.x) * bend
        return (start, Point(mid_x, start.y), Point(mid_x, end.y), end)
    mid_y = start.y + (end.y - start.y) * bend
    return (start, Point(start.x, mid_y), Point(end.x, mid_y), end)


def avoid_points(start: Point, end: Point, avoid_boxes: list[Box], gap: float = 24.0) -> tuple[Point, ...]:
    crosses = [box for box in avoid_boxes if segment_aabb_intersects(start, end, box, gap)]
    if not crosses:
        return (start, end)
    top_lane = min(box.y for box in crosses) - gap
    bottom_lane = max(box.y + box.h for box in crosses) + gap
    if top_lane > GRAPH["y"] + gap:
        mid_y = top_lane
    else:
        mid_y = min(GRAPH["y"] + GRAPH["h"] - gap, bottom_lane)
    return (start, Point(start.x, mid_y), Point(end.x, mid_y), end)


def point_at_path(points: tuple[Point, ...], position: float) -> tuple[Point, float]:
    if len(points) <= 1:
        return (points[0] if points else Point(0, 0), 0.0)
    lengths: list[float] = []
    total = 0.0
    for index in range(len(points) - 1):
        length = math.hypot(points[index + 1].x - points[index].x, points[index + 1].y - points[index].y)
        lengths.append(length)
        total += length
    target = clamp(position, 0.0, 1.0) * total
    for index, length in enumerate(lengths):
        if target <= length or index == len(lengths) - 1:
            ratio = target / length if length else 0.0
            point = Point(
                points[index].x + (points[index + 1].x - points[index].x) * ratio,
                points[index].y + (points[index + 1].y - points[index].y) * ratio,
            )
            angle = math.atan2(points[index + 1].y - points[index].y, points[index + 1].x - points[index].x)
            return point, angle
        target -= length
    return points[-1], 0.0


def route_points_for_edge(edge: dict[str, Any], start: Point, end: Point, nodes: dict[str, RenderedNode]) -> tuple[Point, ...]:
    route = str(edge.get("route") or "straight").lower()
    relation = str(edge.get("relation") or "").lower()
    bend = float(edge.get("route_bend") or edge.get("bend") or 0.5)
    if start.x > end.x and relation == "loops":
        if str(edge.get("loop_side") or "").lower() == "top":
            lane_y = GRAPH["y"] + 18
        else:
            lane_y = min(LOOP["y"] - 12, GRAPH["y"] + GRAPH["h"] + 12)
        exit_x = min(STAGE_W - 24, GRAPH["x"] + GRAPH["w"] + 18)
        entry_x = end.x
        return (start, Point(exit_x, start.y), Point(exit_x, lane_y), Point(entry_x, lane_y), Point(entry_x, end.y), end)
    if start.x > end.x and route in {"orthogonal", "elbow", "dogleg"}:
        lane_y = min(LOOP["y"] - 12, GRAPH["y"] + GRAPH["h"] + 12)
        return (start, Point(start.x, lane_y), Point(end.x, lane_y), end)
    if route in {"orthogonal", "elbow", "dogleg"}:
        return orthogonal_points(start, end, bend=clamp(bend, 0.08, 0.92))
    if route == "avoid":
        avoid_boxes = [
            nodes[str(node_id)].box
            for node_id in edge.get("avoid", []) or []
            if str(node_id) in nodes
        ]
        return avoid_points(start, end, avoid_boxes)
    return (start, end)


def apply_edge_bundling(graph: dict[str, Any], edges: list[dict[str, Any]], nodes: dict[str, RenderedNode]) -> dict[str, tuple[str, int, tuple[Point, ...]]]:
    policy = graph.get("layout_policy") if isinstance(graph.get("layout_policy"), dict) else {}
    bundling_policy = policy.get("edge_bundling") if isinstance(policy.get("edge_bundling"), dict) else {}
    if bundling_policy.get("enabled") is False:
        return {}
    min_edges = int(bundling_policy.get("min_edges") or 2)
    lane_gap_default = float(bundling_policy.get("lane_gap") or 7.5)
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for item in edges:
        edge = item["edge"]
        bundle_intent = edge.get("bundle")
        if bundle_intent is False:
            continue
        if str(edge.get("route") or "").lower() in {"curve", "bezier", "cubic"}:
            continue
        from_node = nodes.get(str(edge.get("from") or ""))
        to_node = nodes.get(str(edge.get("to") or ""))
        if not from_node or not to_node:
            continue
        from_layer = str(from_node.data.get("layer") or "")
        to_layer = str(to_node.data.get("layer") or "")
        if from_layer == to_layer:
            continue
        if isinstance(bundle_intent, str) and bundle_intent.strip():
            key = ("custom", bundle_intent.strip())
        else:
            key = (from_layer, to_layer)
        groups.setdefault(key, []).append(item)

    bundled: dict[str, tuple[str, int, tuple[Point, ...]]] = {}
    for (from_layer, to_layer), group in groups.items():
        if len(group) < min_edges:
            continue
        starts = [item["start"] for item in group]
        ends = [item["end"] for item in group]
        horizontal = abs(median([end.x - start.x for start, end in zip(starts, ends)])) >= abs(median([end.y - start.y for start, end in zip(starts, ends)]))
        bundle_id = to_layer if from_layer == "custom" else f"{from_layer}-to-{to_layer}"
        ordered = sorted(group, key=lambda item: (item["start"].y + item["end"].y, item["start"].x + item["end"].x, str(item["edge"].get("id"))))
        lane_gap = lane_gap_default if len(group) <= 4 else max(4.5, lane_gap_default * 0.72)
        if horizontal:
            bus = median([(item["start"].x + item["end"].x) / 2 for item in group])
            for index, item in enumerate(ordered):
                offset = (index - (len(ordered) - 1) / 2) * lane_gap
                lane_x = bus + offset
                points = (item["start"], Point(lane_x, item["start"].y), Point(lane_x, item["end"].y), item["end"])
                bundled[str(item["edge"].get("id"))] = (bundle_id, index, points)
        else:
            bus = median([(item["start"].y + item["end"].y) / 2 for item in group])
            for index, item in enumerate(ordered):
                offset = (index - (len(ordered) - 1) / 2) * lane_gap
                lane_y = bus + offset
                points = (item["start"], Point(item["start"].x, lane_y), Point(item["end"].x, lane_y), item["end"])
                bundled[str(item["edge"].get("id"))] = (bundle_id, index, points)
    return bundled


def label_placement_for_edge(
    edge: dict[str, Any],
    points: tuple[Point, ...],
    node_boxes: list[Box],
    placed_labels: list[Box],
) -> LabelPlacement | None:
    label = str(edge.get("label") or "")
    if not label:
        return None
    width = max(42.0, min(92.0, len(label) * 7.0))
    height = 16.0
    priority = int(edge.get("label_priority") or 3)
    priority_multiplier = 1.0 + (priority - 3) * 0.18
    explicit_position = edge.get("label_position")
    positions = [float(explicit_position)] if isinstance(explicit_position, (int, float)) else [0.5, 0.42, 0.58, 0.34, 0.66]
    offset_distances = [-26.0, 26.0, -44.0, 44.0, -62.0, 62.0, -80.0, 80.0, 0.0]
    best: LabelPlacement | None = None
    for position in positions:
        base, angle = point_at_path(points, position)
        normal = Point(-math.sin(angle), math.cos(angle))
        for distance in offset_distances:
            offset = Point(normal.x * distance, normal.y * distance)
            box = Box(base.x + offset.x - width / 2, base.y + offset.y - height / 2, width, height)
            score = abs(position - 0.5) * 30 + abs(distance) * 0.08
            score += box_outside_penalty(box, GRAPH) * 80 * priority_multiplier
            for node_box in node_boxes:
                score += intersection_area(box, node_box, 8) * 4 * priority_multiplier
            for label_box in placed_labels:
                score += intersection_area(box, label_box, 5) * 5 * priority_multiplier
            if best is None or score < best.score:
                best = LabelPlacement(position=position, offset=offset, width=width, height=height, score=round(score, 2), box=box)
    if best:
        placed_labels.append(best.box)
    return best


def layout_edges(graph: dict[str, Any], nodes: dict[str, RenderedNode]) -> list[RenderedEdge]:
    edge_order, active_edges = active_edge_order(graph)
    candidates: list[dict[str, Any]] = []
    for edge in graph.get("edges", []) or []:
        if not isinstance(edge, dict) or not edge.get("id"):
            continue
        start_node = nodes.get(str(edge.get("from") or ""))
        end_node = nodes.get(str(edge.get("to") or ""))
        if not start_node or not end_node:
            continue
        start, end = anchor_between(start_node.box, end_node.box)
        anchor_from, anchor_to = anchor_sides(start_node.box, end_node.box)
        explicit_anchor_from = str(edge.get("anchor_from") or "").strip().lower()
        explicit_anchor_to = str(edge.get("anchor_to") or "").strip().lower()
        start = anchor_point(start_node.box, explicit_anchor_from, start)
        end = anchor_point(end_node.box, explicit_anchor_to, end)
        left = min(start.x, end.x)
        top = min(start.y, end.y)
        width = max(1.0, abs(end.x - start.x))
        height = max(1.0, abs(end.y - start.y))
        candidates.append({
            "edge": edge,
            "start": start,
            "end": end,
            "anchor_from": str(edge.get("anchor_from") or anchor_from),
            "anchor_to": str(edge.get("anchor_to") or anchor_to),
            "base_box": Box(left, top, width, height),
        })

    bundle_routes = apply_edge_bundling(graph, candidates, nodes)
    node_boxes = [node.box for node in nodes.values()]
    placed_labels: list[Box] = []
    rendered: list[RenderedEdge] = []
    for item in candidates:
        edge = item["edge"]
        edge_id = str(edge.get("id") or "")
        start = item["start"]
        end = item["end"]
        style = edge.get("style") if isinstance(edge.get("style"), dict) else {}
        relation = str(edge.get("relation") or "")
        active = truthy(edge.get("active")) or edge_id in active_edges
        color = str(style.get("color") or RELATION_COLORS.get(relation, "#A8B3C7"))
        base_width = float(style.get("width") or (3 if active else 2))
        dash = str(style.get("dash") or ("dash" if relation in {"blocks", "loops", "contradicts"} else ""))
        arrow = str(style.get("arrow") or "end")
        route = str(edge.get("route") or "straight")
        label = str(edge.get("label") or "")
        bundle_id = ""
        bundle_lane = -1
        points = route_points_for_edge(edge, start, end, nodes)
        if edge_id in bundle_routes:
            bundle_id, bundle_lane, points = bundle_routes[edge_id]
            if route == "straight":
                route = "orthogonal"
        left = min(point.x for point in points)
        top = min(point.y for point in points)
        right = max(point.x for point in points)
        bottom = max(point.y for point in points)
        box = Box(left, top, max(1.0, right - left), max(1.0, bottom - top))
        local_points = tuple(Point(point.x - left, point.y - top) for point in points)
        label_placement = label_placement_for_edge(edge, points, node_boxes, placed_labels)
        rendered.append(
            RenderedEdge(
                data={**edge, "_active_order": edge_order.get(edge_id, 9999)},
                box=box,
                start=local_points[0],
                end=local_points[-1],
                points=local_points,
                anchor_from=item["anchor_from"],
                anchor_to=item["anchor_to"],
                route=route,
                label=label,
                label_placement=label_placement,
                bundle_id=bundle_id,
                bundle_lane=bundle_lane,
                color=color,
                width=base_width,
                dash=dash,
                arrow=arrow,
                active=active,
            )
        )
    rendered.sort(key=lambda edge: (0 if edge.active else 1, edge.data.get("_active_order", 9999), str(edge.data.get("id"))))
    return rendered


def absolute_edge_points(edge: RenderedEdge) -> tuple[Point, ...]:
    return tuple(Point(edge.box.x + point.x, edge.box.y + point.y) for point in edge.points)


def rect_distance(a: Box, b: Box) -> float:
    dx = max(a.x - (b.x + b.w), b.x - (a.x + a.w), 0.0)
    dy = max(a.y - (b.y + b.h), b.y - (a.y + a.h), 0.0)
    return math.hypot(dx, dy)


def node_crowding_metrics(nodes: dict[str, RenderedNode]) -> dict[str, Any]:
    node_items = list(nodes.items())
    overlaps = 0
    min_gap = 9999.0
    pressure = 0.0
    desired_gap = 12.0
    close_pairs: list[dict[str, Any]] = []
    for index, (first_id, first) in enumerate(node_items):
        for second_id, second in node_items[index + 1:]:
            gap = rect_distance(first.box, second.box)
            min_gap = min(min_gap, gap)
            if intersects(first.box, second.box, 1):
                overlaps += 1
                pressure += 4.0
                close_pairs.append({"a": first_id, "b": second_id, "gap": round(gap, 2), "overlap": True})
            elif gap < desired_gap:
                pressure += (desired_gap - gap) / desired_gap
                close_pairs.append({"a": first_id, "b": second_id, "gap": round(gap, 2), "overlap": False})
    return {
        "node_overlaps": overlaps,
        "node_crowding_score": round(pressure, 2),
        "min_node_gap": 0 if min_gap == 9999.0 else round(min_gap, 2),
        "close_node_pairs": close_pairs[:8],
    }


def edge_density_metrics(edges: list[RenderedEdge]) -> dict[str, Any]:
    if not edges:
        return {"edge_density_peak": 0, "edge_density_hot_cells": 0, "edge_density_score": 0}
    cols = 8
    rows = 5
    cell_w = GRAPH["w"] / cols
    cell_h = GRAPH["h"] / rows
    counts = [[0 for _ in range(cols)] for _ in range(rows)]
    for edge in edges:
        points = absolute_edge_points(edge)
        for index in range(len(points) - 1):
            a = points[index]
            b = points[index + 1]
            for row in range(rows):
                for col in range(cols):
                    cell = Box(GRAPH["x"] + col * cell_w, GRAPH["y"] + row * cell_h, cell_w, cell_h)
                    if segment_aabb_intersects(a, b, cell, 0):
                        counts[row][col] += 1
    flattened = [value for row in counts for value in row]
    peak = max(flattened, default=0)
    hot_threshold = max(5, math.ceil(len(edges) * 0.28))
    hot_cells = sum(1 for value in flattened if value >= hot_threshold)
    score = peak + hot_cells * 0.35
    return {
        "edge_density_peak": peak,
        "edge_density_hot_cells": hot_cells,
        "edge_density_score": round(score, 2),
        "edge_density_grid": counts,
    }


def split_label(label: str) -> tuple[str, str]:
    parts = re.split(r"\s*[|/]\s*", label, maxsplit=1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    if len(label) > 12:
        return label[:12], label[12:26]
    return label, ""


def graph_title(graph: dict[str, Any]) -> str:
    for key in ("title", "name"):
        value = str(graph.get(key) or "").strip()
        if value:
            return value
    graph_id = str(graph.get("graph_id") or "relationship graph")
    return graph_id.replace("-", " ").title()


def css_edge_vars(edge: RenderedEdge) -> str:
    dx = edge.end.x - edge.start.x
    dy = edge.end.y - edge.start.y
    length = math.hypot(dx, dy)
    angle = math.degrees(math.atan2(dy, dx))
    line_style = "dashed" if edge.dash else "solid"
    values = {
        "left": f"{pt(edge.box.x - GRAPH['x'])}pt",
        "top": f"{pt(edge.box.y - GRAPH['y'])}pt",
        "width": f"{pt(edge.box.w)}pt",
        "height": f"{pt(edge.box.h)}pt",
        "--line-x": f"{pt(edge.start.x)}pt",
        "--line-y": f"{pt(edge.start.y)}pt",
        "--line-end-x": f"{pt(edge.end.x)}pt",
        "--line-end-y": f"{pt(edge.end.y)}pt",
        "--line-len": f"{pt(length)}pt",
        "--line-angle": f"{pt(angle)}deg",
        "--edge-color": edge.color,
        "--edge-width": f"{pt(edge.width)}pt",
        "--edge-style": line_style,
        "--edge-opacity": "0.96" if edge.active else "0.48",
    }
    return "; ".join(f"{key}: {value}" for key, value in values.items())


def render_slide(
    graph: dict[str, Any],
    nodes: dict[str, RenderedNode],
    edges: list[RenderedEdge],
    layer_geometry: dict[str, dict[str, Any]],
    swimlane_geometry: dict[str, dict[str, Any]],
) -> str:
    title = graph_title(graph)
    purpose = str(graph.get("purpose") or "Relationship graph auto layout.")
    active_paths = [item for item in graph.get("active_paths", []) or [] if isinstance(item, dict)]
    path_message = str(active_paths[0].get("message") if active_paths else "Active edges mark the viewer reading path.")

    layer_labels = []
    for layer_id, info in layer_geometry.items():
        layer_labels.append(
            f'<span class="layer-label" data-pptx-text="true" data-graph-label="{esc(layer_id)}" '
            f'data-visual-qa-zone="graph" style="left:{pt(float(info["x"]) - GRAPH["x"])}pt">'
            f'{esc(info["name"])}</span>'
        )
    swimlane_markup = []
    for lane_id, info in swimlane_geometry.items():
        swimlane_markup.append(
            f'<div class="swimlane" data-graph-swimlane="{esc(lane_id)}" '
            f'style="top:{pt(float(info["y"]) - GRAPH["y"])}pt; height:{pt(float(info["h"]))}pt; '
            f'--lane-fill:{esc(info.get("color", "rgba(99,202,255,0.08)"))}">'
            f'<span data-pptx-text="true" data-visual-qa-zone="graph">{esc(info.get("name", lane_id))}</span></div>'
        )

    edge_markup = []
    edge_label_markup = []
    for edge in edges:
        edge_id = str(edge.data.get("id") or "")
        from_x = pct(edge.start.x, edge.box.w)
        from_y = pct(edge.start.y, edge.box.h)
        to_x = pct(edge.end.x, edge.box.w)
        to_y = pct(edge.end.y, edge.box.h)
        dash_attr = f' data-pptx-dash="{esc(edge.dash)}"' if edge.dash else ""
        route_attr = f' data-pptx-route="{esc(edge.route)}"' if edge.route and edge.route != "straight" else ""
        waypoint_attr = ""
        if len(edge.points) > 2:
            stage_waypoints = [
                f"stage:{pct(edge.box.x + point.x, STAGE_W)},{pct(edge.box.y + point.y, STAGE_H)}"
                for point in edge.points[1:-1]
            ]
            waypoint_attr = f' data-pptx-waypoints="{esc(";".join(stage_waypoints))}"'
        bundle_attr = ""
        if edge.bundle_id:
            bundle_attr = f' data-graph-bundle="{esc(edge.bundle_id)}" data-graph-bundle-lane="{edge.bundle_lane}"'
        label_attr = ""
        if edge.label:
            placement = edge.label_placement
            label_position = placement.position if placement else 0.5
            label_offset = placement.offset if placement else Point(0, -14)
            label_width = placement.width if placement else max(42, min(92, len(edge.label) * 7))
            label_score = placement.score if placement else 9999
            label_attr = (
                f' data-pptx-label="{esc(edge.label)}" data-pptx-label-position="{pt(label_position)}" '
                f'data-pptx-label-offset="{browser_px(label_offset.x)},{browser_px(label_offset.y)}" '
                f'data-pptx-label-width="{browser_px(label_width)}" data-pptx-label-height="{browser_px(edge.label_placement.height if edge.label_placement else 16)}" '
                f'data-graph-label-score="{pt(label_score)}"'
            )
        segment_markup = ""
        if len(edge.points) > 2:
            parts = []
            for index in range(len(edge.points) - 1):
                a = edge.points[index]
                b = edge.points[index + 1]
                length = math.hypot(b.x - a.x, b.y - a.y)
                angle = math.degrees(math.atan2(b.y - a.y, b.x - a.x))
                parts.append(
                    f'<i class="edge-segment" style="left:{pt(a.x)}pt; top:{pt(a.y)}pt; '
                    f'width:{pt(length)}pt; --seg-angle:{pt(angle)}deg"></i>'
                )
            final_a = edge.points[-2]
            final_b = edge.points[-1]
            final_angle = math.degrees(math.atan2(final_b.y - final_a.y, final_b.x - final_a.x))
            parts.append(
                f'<i class="edge-arrow" style="left:{pt(final_b.x)}pt; top:{pt(final_b.y)}pt; '
                f'--seg-angle:{pt(final_angle)}deg"></i>'
            )
            segment_markup = "".join(parts)
        rendered_class = " edge-routed" if segment_markup else ""
        edge_markup.append(
            f'<div class="edge edge-{esc(css_class(edge_id))}{rendered_class}" data-arrow="{esc(edge.arrow)}" '
            f'data-graph-edge="{esc(edge_id)}" data-graph-from="{esc(edge.data.get("from", ""))}" '
            f'data-graph-to="{esc(edge.data.get("to", ""))}" data-graph-layer="{esc(edge.data.get("layer", ""))}" '
            f'data-graph-relation="{esc(edge.data.get("relation", ""))}" '
            f'data-graph-strength="{esc(edge.data.get("strength", ""))}" data-graph-active="{str(edge.active).lower()}" '
            f'{bundle_attr} '
            f'data-pptx-connector data-pptx-from="{from_x},{from_y}" data-pptx-to="{to_x},{to_y}" '
            f'data-pptx-anchor-from="{esc(edge.anchor_from)}" data-pptx-anchor-to="{esc(edge.anchor_to)}"{route_attr}{waypoint_attr}{label_attr} '
            f'data-pptx-arrow="{esc(edge.arrow)}" data-pptx-color="{esc(edge.color)}" '
            f'data-pptx-width="{pt(edge.width)}"{dash_attr} style="{esc(css_edge_vars(edge))}">{segment_markup}</div>'
        )
        if edge.label and edge.label_placement:
            label_x = edge.label_placement.box.cx - GRAPH["x"]
            label_y = edge.label_placement.box.cy - GRAPH["y"]
            edge_label_markup.append(
                f'<span class="edge-label" data-pptx="ignore" data-graph-label="{esc(edge_id)}" '
                f'data-graph-label-score="{pt(edge.label_placement.score)}" '
                f'style="left:{pt(label_x)}pt; top:{pt(label_y)}pt; width:{pt(edge.label_placement.width)}pt; --edge-color:{esc(edge.color)}">{esc(edge.label)}</span>'
            )

    node_markup = []
    for node_id, node in nodes.items():
        role = str(node.data.get("role") or "support")
        layer = str(node.data.get("layer") or "")
        swimlane_id = node_swimlane_id(node.data)
        primary, secondary = split_label(str(node.data.get("label") or node_id))
        collapsed_members = node.data.get("collapsed_members") if isinstance(node.data.get("collapsed_members"), list) else []
        if collapsed_members:
            secondary = f"{len(collapsed_members)} signals collapsed"
        else:
            secondary = secondary or role
        compact = node.box.h <= 30
        style = (
            f"left:{pt(node.box.x - GRAPH['x'])}pt; top:{pt(node.box.y - GRAPH['y'])}pt; "
            f"width:{pt(node.box.w)}pt; height:{pt(node.box.h)}pt; --accent:{node.color}; "
            f"--node-pad-y:{'5pt' if compact else '9pt'}; --node-pad-x:{'7pt' if compact else '10pt'}; "
            f"--node-title:{'8.2pt' if compact else '11pt'}; --node-meta:{'0pt' if compact else '7.4pt'};"
        )
        node_markup.append(
            f'<div class="node role-{esc(css_class(role))}" data-graph-node="{esc(node_id)}" '
            f'data-graph-layer="{esc(layer)}" data-graph-role="{esc(role)}" '
            f'data-graph-swimlane="{esc(swimlane_id)}" data-graph-collapsed="{str(bool(collapsed_members)).lower()}" '
            f'data-graph-compact="{str(compact).lower()}" '
            f'data-graph-priority="{esc(node.data.get("priority", ""))}" data-graph-active="{str(node.active).lower()}" '
            f'style="{esc(style)}"><strong>{esc(primary)}</strong><span>{esc(secondary)}</span></div>'
        )

    active_path_edges: list[str] = []
    if active_paths:
        active_path_edges = [str(item) for item in active_paths[0].get("edges", []) or []]
    if not active_path_edges:
        active_path_edges = [str(edge.data.get("id")) for edge in edges if edge.active][:4]

    path_chips = []
    for edge_id in active_path_edges[:5]:
        edge = next((item for item in edges if str(item.data.get("id")) == edge_id), None)
        label = str(edge.data.get("relation") if edge else edge_id)
        path_chips.append(f'<span class="chip active" data-graph-label="{esc(edge_id)}">{esc(label)}</span>')
    if not path_chips:
        path_chips.append('<span class="chip" data-graph-label="autolayout">auto layout</span>')

    visual_slot_markup = []
    for slot in graph_visual_slots(graph):
        box = slot["box"]
        slot_id = str(slot["id"])
        role = str(slot.get("role") or slot.get("asset_role") or "atmosphere")
        src = str(slot.get("src") or "")
        opacity = clamp(float(slot.get("opacity") or 0.72), 0.05, 1.0)
        fit = str(slot.get("fit") or "cover")
        transparent_attr = str(bool(slot.get("transparent"))).lower()
        blend_mode = str(slot.get("blend_mode") or "normal")
        if src:
            visual_slot_markup.append(
                f'<img class="visual-slot" data-visual-slot="{esc(slot_id)}" data-asset-role="{esc(role)}" '
                f'data-visual-transparent="{transparent_attr}" data-asset-fit="{esc(fit)}" '
                f'alt="" src="{esc(slot_src_for_html(src))}" style="left:{pt(box["x"])}pt; top:{pt(box["y"])}pt; '
                f'width:{pt(box["w"])}pt; height:{pt(box["h"])}pt; opacity:{pt(opacity)}; object-fit:{esc(fit)}; '
                f'mix-blend-mode:{esc(blend_mode)}" />'
            )
        else:
            visual_slot_markup.append(
                f'<div class="visual-slot visual-slot-empty" data-visual-slot="{esc(slot_id)}" '
                f'data-asset-role="{esc(role)}" data-visual-transparent="{transparent_attr}" data-asset-fit="{esc(fit)}" '
                f'style="left:{pt(box["x"])}pt; top:{pt(box["y"])}pt; '
                f'width:{pt(box["w"])}pt; height:{pt(box["h"])}pt; opacity:{pt(opacity)}"></div>'
            )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      width: 960pt;
      height: 540pt;
      overflow: hidden;
      background: #050b12;
      color: #f8fbff;
      font-family: "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
      position: relative;
    }}
    .slide {{
      position: relative;
      width: 960pt;
      height: 540pt;
      overflow: hidden;
      background: #050b12;
    }}
    .visual-slot {{
      position: absolute;
      object-fit: cover;
      border: 1pt solid rgba(120, 194, 255, 0.2);
      border-radius: 8pt;
      z-index: 1;
      pointer-events: none;
    }}
    .visual-slot[data-visual-transparent="true"] {{
      border-color: transparent;
      border-radius: 0;
    }}
    .visual-slot-empty {{
      background: rgba(8, 20, 34, 0.84);
    }}
    .claim {{
      position: absolute;
      left: {pt(CLAIM["x"])}pt;
      top: {pt(CLAIM["y"])}pt;
      width: {pt(CLAIM["w"])}pt;
      height: {pt(CLAIM["h"])}pt;
      padding: 20pt 21pt;
      border: 1pt solid rgba(120, 194, 255, 0.28);
      border-radius: 8pt;
      background: rgba(8, 20, 34, 0.94);
      z-index: 3;
    }}
    h1 {{ font-size: 25pt; line-height: 1.06; font-weight: 760; color: #ffffff; }}
    p {{ margin-top: 10pt; font-size: 10.5pt; line-height: 1.38; color: #d9e8f7; }}
    .graph {{
      position: absolute;
      left: {pt(GRAPH["x"])}pt;
      top: {pt(GRAPH["y"])}pt;
      width: {pt(GRAPH["w"])}pt;
      height: {pt(GRAPH["h"])}pt;
      z-index: 2;
    }}
    .rail {{
      position: absolute;
      top: 26pt;
      bottom: 0;
      width: 1pt;
      background: rgba(120, 194, 255, 0.1);
    }}
    .layer-label {{
      position: absolute;
      top: 0;
      max-width: 108pt;
      color: #6e91a8;
      font-size: 7pt;
      line-height: 1;
      text-transform: uppercase;
      white-space: nowrap;
    }}
    .swimlane {{
      position: absolute;
      left: 0;
      width: 100%;
      border: 1pt solid rgba(120, 194, 255, 0.08);
      border-radius: 8pt;
      background: var(--lane-fill);
      z-index: 0;
    }}
    .swimlane span {{
      position: absolute;
      left: 8pt;
      top: 5pt;
      color: rgba(217, 232, 247, 0.42);
      font-size: 6.8pt;
      line-height: 1;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0;
    }}
    .edge {{
      position: absolute;
      min-width: 1pt;
      min-height: 1pt;
      pointer-events: none;
      opacity: var(--edge-opacity);
      z-index: 1;
    }}
    .edge::before {{
      content: "";
      position: absolute;
      left: var(--line-x);
      top: var(--line-y);
      width: var(--line-len);
      height: 0;
      border-top: var(--edge-width) var(--edge-style) var(--edge-color);
      transform-origin: 0 0;
      transform: rotate(var(--line-angle));
    }}
    .edge::after {{
      content: "";
      position: absolute;
      left: var(--line-end-x);
      top: var(--line-end-y);
      width: 0;
      height: 0;
      border-top: 4pt solid transparent;
      border-bottom: 4pt solid transparent;
      border-left: 6pt solid var(--edge-color);
      transform-origin: 0 50%;
      transform: translate(-1pt, -4pt) rotate(var(--line-angle));
    }}
    .edge[data-arrow="none"]::after,
    .edge[data-arrow="begin"]::after {{ display: none; }}
    .edge-routed::before,
    .edge-routed::after {{ display: none; }}
    .edge-segment {{
      position: absolute;
      display: block;
      height: 0;
      border-top: var(--edge-width) var(--edge-style) var(--edge-color);
      transform-origin: 0 0;
      transform: rotate(var(--seg-angle));
    }}
    .edge-arrow {{
      position: absolute;
      display: block;
      width: 0;
      height: 0;
      border-top: 4pt solid transparent;
      border-bottom: 4pt solid transparent;
      border-left: 6pt solid var(--edge-color);
      transform-origin: 0 50%;
      transform: translate(-1pt, -4pt) rotate(var(--seg-angle));
    }}
    .edge[data-arrow="none"] .edge-arrow,
    .edge[data-arrow="begin"] .edge-arrow {{ display: none; }}
    .edge-label {{
      position: absolute;
      z-index: 3;
      max-width: 92pt;
      padding: 3pt 6pt;
      border: 1pt solid color-mix(in srgb, var(--edge-color) 46%, transparent);
      border-radius: 999pt;
      background: rgba(8, 20, 34, 0.92);
      color: #d9e8f7;
      font-size: 7pt;
      line-height: 1;
      font-weight: 700;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      transform: translate(-50%, -50%);
      pointer-events: none;
    }}
    .node {{
      position: absolute;
      padding: var(--node-pad-y) var(--node-pad-x);
      border: 1pt solid color-mix(in srgb, var(--accent) 68%, transparent);
      border-radius: 7pt;
      background: #09192a;
      z-index: 4;
    }}
    .node[data-graph-active="true"] {{
      border-color: var(--accent);
      background: #0d2238;
    }}
    .node[data-graph-collapsed="true"] {{
      border-style: dashed;
      background: #101d2b;
    }}
    .node strong {{
      display: block;
      color: #ffffff;
      font-size: var(--node-title);
      line-height: 1.1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .node span {{
      display: block;
      margin-top: 4pt;
      color: #9ebcd1;
      font-size: var(--node-meta);
      line-height: 1.2;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .node[data-graph-compact="true"] span {{ display: none; }}
    .caption {{
      position: absolute;
      left: {pt(EVIDENCE["x"])}pt;
      top: {pt(EVIDENCE["y"])}pt;
      width: {pt(EVIDENCE["w"])}pt;
      min-height: {pt(EVIDENCE["h"])}pt;
      padding: 14pt 15pt;
      border: 1pt solid rgba(237, 187, 102, 0.36);
      border-radius: 7pt;
      background: rgba(18, 27, 38, 0.94);
      z-index: 3;
    }}
    .caption strong {{ display: block; color: #edbb66; font-size: 11.5pt; line-height: 1.1; }}
    .caption span {{ display: block; margin-top: 7pt; color: #d9e8f7; font-size: 9.5pt; line-height: 1.35; }}
    .loop {{
      position: absolute;
      left: {pt(LOOP["x"])}pt;
      top: {pt(LOOP["y"])}pt;
      width: {pt(LOOP["w"])}pt;
      height: {pt(LOOP["h"])}pt;
      display: grid;
      grid-template-columns: repeat({max(1, len(path_chips))}, 1fr);
      gap: 8pt;
      z-index: 3;
    }}
    .chip {{
      display: grid;
      place-items: center;
      min-width: 0;
      padding: 0 9pt;
      border: 1pt solid rgba(120, 194, 255, 0.34);
      border-radius: 999pt;
      background: rgba(8, 20, 34, 0.94);
      color: #d9e8f7;
      font-size: 9.5pt;
      font-weight: 700;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .chip.active {{
      color: #edbb66;
      border-color: rgba(237, 187, 102, 0.64);
    }}
  </style>
</head>
<body>
  <main class="slide">
    {"".join(visual_slot_markup)}
    <section class="claim">
      <h1>{esc(title)}</h1>
      <p>{esc(purpose[:170])}</p>
    </section>
    <section class="graph" data-graph="{esc(graph.get("graph_id", "relationship-graph"))}">
      {"".join(f'<span class="rail" style="left:{pt(float(info["x"]) - GRAPH["x"])}pt"></span>' for info in layer_geometry.values())}
      {"".join(swimlane_markup)}
      {"".join(layer_labels)}
      {"".join(edge_markup)}
      {"".join(edge_label_markup)}
      {"".join(node_markup)}
    </section>
    <section class="caption">
      <strong>Active path</strong>
      <span>{esc(path_message[:185])}</span>
    </section>
    <section class="loop">
      {"".join(path_chips)}
    </section>
  </main>
</body>
</html>
"""


def render_index(title: str, slides: list[dict[str, str]]) -> str:
    manifest_slides = ",\n".join(
        "          {\n"
        f"            id: \"{esc(slide['id'])}\",\n"
        f"            src: \"{esc(slide['src'])}\",\n"
        f"            title: \"{esc(slide['title'])}\"\n"
        "          }"
        for slide in slides
    )
    first_src = slides[0]["src"] if slides else "slides/01-relationship-autolayout.html"
    return f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <title>{esc(title)}</title>
    <script>
      window.DECK_MANIFEST = {{
        title: "{esc(title)}",
        slides: [
{manifest_slides}
        ]
      }};
      window.location.replace("{esc(first_src)}");
    </script>
  </head>
  <body></body>
</html>
"""


def slide_blueprint(
    slide_id: str,
    graph: dict[str, Any],
    nodes: dict[str, RenderedNode],
    edges: list[RenderedEdge],
    layer_geometry: dict[str, dict[str, Any]],
    swimlane_geometry: dict[str, dict[str, Any]],
    diagnostics: dict[str, Any],
) -> dict[str, Any]:
    node_boxes = {
        node_id: {
            "x": round(node.box.x, 2),
            "y": round(node.box.y, 2),
            "w": round(node.box.w, 2),
            "h": round(node.box.h, 2),
            "layer": str(node.data.get("layer") or ""),
            "swimlane": node_swimlane_id(node.data),
            "collapsed": bool(node.data.get("collapsed_members")),
        }
        for node_id, node in nodes.items()
    }
    edge_boxes = {
        str(edge.data.get("id")): {
            "x": round(edge.box.x, 2),
            "y": round(edge.box.y, 2),
            "w": round(edge.box.w, 2),
            "h": round(edge.box.h, 2),
            "from": str(edge.data.get("from") or ""),
            "to": str(edge.data.get("to") or ""),
            "relation": str(edge.data.get("relation") or ""),
            "layer": str(edge.data.get("layer") or ""),
            "active": edge.active,
            "route": edge.route,
            "anchor_from": edge.anchor_from,
            "anchor_to": edge.anchor_to,
            "label": edge.label,
            "bundle": edge.bundle_id,
            "bundle_lane": edge.bundle_lane,
            "label_score": edge.label_placement.score if edge.label_placement else None,
            "waypoints": [
                {"x": round(edge.box.x + point.x, 2), "y": round(edge.box.y + point.y, 2)}
                for point in edge.points[1:-1]
            ],
        }
        for edge in edges
    }
    bundled_edges = [edge for edge in edges if edge.bundle_id]
    scored_labels = [edge for edge in edges if edge.label_placement]
    crowding = node_crowding_metrics(nodes)
    density = edge_density_metrics(edges)
    return {
        "id": slide_id,
        "archetype": "system-loop",
        "job": "render relationship-graph.json view with auto layout into editable-oriented HTML",
        "claim": CLAIM,
        "evidence": EVIDENCE,
        "visual": GRAPH,
        "loop": LOOP,
        "graph": {
            "graph_id": graph.get("graph_id"),
            "view_id": (graph.get("_view") or {}).get("id"),
            "nodes": node_boxes,
            "edges": edge_boxes,
            "layers": layer_geometry,
            "swimlanes": swimlane_geometry,
            "layout_strategy": "layer columns + swimlane bands + subgraph collapse + barycentric crossing minimization + crowding/density scoring + edge bundling + label placement scoring",
            "diagnostics": {
                **diagnostics,
                "bundled_edges": len(bundled_edges),
                "edge_bundles": len({edge.bundle_id for edge in bundled_edges}),
                "scored_labels": len(scored_labels),
                "max_label_score": max((edge.label_placement.score for edge in scored_labels), default=0),
                **crowding,
                **density,
            },
        },
        "visual_assets": [
            {
                "id": str(slot["id"]),
                "role": str(slot.get("role") or slot.get("asset_role") or "atmosphere"),
                "box": slot["box"],
                "src": str(slot.get("src") or ""),
                "prompt": str(slot.get("prompt") or ""),
                "fit": str(slot.get("fit") or "cover"),
                "rules": [
                    "decorative or metaphorical only",
                    "must not carry necessary text",
                    "must not overlap claim/evidence/graph/loop text zones",
                ],
            }
            for slot in graph_visual_slots(graph)
        ],
        "empty": [
            "claim/evidence rail owns prose",
            "graph labels remain native editable text",
            "all core edges are HTML elements with PPTX connector data attributes",
        ],
    }


def layout_blueprint(slides: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "stage": {
            "width": STAGE_W,
            "height": STAGE_H,
            "safe": {"x": 40, "y": 40, "w": 880, "h": 460},
        },
        "slides": slides,
    }


def render(graph_path: Path, out_dir: Path) -> None:
    base_graph = read_graph(graph_path)
    views = graph_views(base_graph)
    slides_dir = out_dir / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)
    for stale_slide in slides_dir.glob("*.html"):
        stale_slide.unlink()

    title = graph_title(base_graph)
    manifest_slides: list[dict[str, str]] = []
    blueprint_slides: list[dict[str, Any]] = []
    total_nodes = 0
    total_edges = 0
    total_bundled_edges = 0
    total_scored_labels = 0
    max_crowding = 0.0
    max_density_peak = 0
    max_crossings_before = 0
    max_crossings_after = 0
    max_swimlanes = 0
    max_collapsed = 0

    for index, view in enumerate(views, start=1):
        slide_stem = "01-relationship-autolayout" if view.get("_default") else f"{index:02d}-{slug(str(view['id']))}"
        graph = normalize_graph(filtered_graph_for_view(base_graph, view))
        nodes, layers, swimlanes, diagnostics = layout_nodes(graph)
        diagnostics.update(graph.get("_collapse_diagnostics") or {})
        edges = layout_edges(graph, nodes)
        slide_title = (graph.get("_view") or {}).get("index_title") or graph_title(graph)
        slide_file = f"{slide_stem}.html"
        (slides_dir / slide_file).write_text(
            render_slide(graph, nodes, edges, layers, swimlanes),
            encoding="utf-8",
        )
        manifest_slides.append({"id": slide_stem, "src": f"slides/{slide_file}", "title": str(slide_title)})
        blueprint_slides.append(slide_blueprint(slide_stem, graph, nodes, edges, layers, swimlanes, diagnostics))

        bundled_edges = sum(1 for edge in edges if edge.bundle_id)
        scored_labels = sum(1 for edge in edges if edge.label_placement)
        crowding = node_crowding_metrics(nodes)
        density = edge_density_metrics(edges)
        total_nodes += len(nodes)
        total_edges += len(edges)
        total_bundled_edges += bundled_edges
        total_scored_labels += scored_labels
        max_crowding = max(max_crowding, float(crowding["node_crowding_score"]))
        max_density_peak = max(max_density_peak, int(density["edge_density_peak"]))
        max_crossings_before = max(max_crossings_before, int(diagnostics.get("crossings_before", 0)))
        max_crossings_after = max(max_crossings_after, int(diagnostics.get("crossings_after", 0)))
        max_swimlanes = max(max_swimlanes, int(diagnostics.get("swimlanes", 0)))
        max_collapsed = max(max_collapsed, int(diagnostics.get("collapsed_subgraphs", 0)))

    (out_dir / "index.html").write_text(render_index(title, manifest_slides), encoding="utf-8")
    (out_dir / "layout-blueprint.json").write_text(
        json.dumps(layout_blueprint(blueprint_slides), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        "relationship-graph-rendered "
        f"out={out_dir.resolve()} slides={len(manifest_slides)} nodes={total_nodes} edges={total_edges} "
        f"max_crossings_before={max_crossings_before} max_crossings_after={max_crossings_after} "
        f"bundled_edges={total_bundled_edges} scored_labels={total_scored_labels} "
        f"max_node_crowding={round(max_crowding, 2)} max_edge_density_peak={max_density_peak} "
        f"max_swimlanes={max_swimlanes} max_collapsed_subgraphs={max_collapsed}"
    )


def resolve_paths(input_path: Path, out_arg: Path | None) -> tuple[Path, Path]:
    if input_path.is_dir():
        graph_path = input_path / "relationship-graph.json"
        out_dir = out_arg or input_path
    else:
        graph_path = input_path
        out_dir = out_arg or input_path.parent
    if not graph_path.exists():
        raise SystemExit(f"relationship-graph.json not found: {graph_path}")
    return graph_path.resolve(), out_dir.resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Deck directory or relationship-graph.json path")
    parser.add_argument("--out", type=Path, help="Output deck directory. Defaults to the input deck/file parent.")
    args = parser.parse_args()

    graph_path, out_dir = resolve_paths(args.input, args.out)
    render(graph_path, out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
