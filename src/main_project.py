from shapely.geometry import shape
from shapely.validation import explain_validity

from admin_units import Province, Municipality, Barangay
from spatial import Parcel, TransmissionLineEasement
from analysis import EasementChecker

import json
import os



def load_json(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


admin_cache = {}


def get_barangay(location):
    province_name = location["province"]
    municipality_name = location["municipality"]
    barangay_name = location["barangay"]

    if province_name not in admin_cache:
        admin_cache[province_name] = Province(province_name)

    province = admin_cache[province_name]

    municipality = next(
        (m for m in province.municipalities if m.name == municipality_name),
        None
    )

    if municipality is None:
        municipality = Municipality(municipality_name, province)

    barangay = next(
        (b for b in municipality.barangays if b.name == barangay_name),
        None
    )

    if barangay is None:
        barangay = Barangay(barangay_name, municipality)

    return barangay


def load_parcels(file_path):
    data = load_json(file_path)
    parcels = []

    for feature in data["features"]:
        properties = feature["properties"]
        polygon = shape(feature["geometry"])

        if not polygon.is_valid:
            print(
                f"Invalid Lot {properties.get('lot_no', 'Unknown')}: "
                f"{explain_validity(polygon)}"
            )
            polygon = polygon.buffer(0)

        location = properties.get(
            "location",
            {
                "barangay": "Unknown Barangay",
                "municipality": "Unknown Municipality",
                "province": "Unknown Province"
            }
        )

        barangay = get_barangay(location)

        parcel = Parcel(
            lot_no=properties.get("lot_no", "Unknown"),
            owner=properties.get("owner", "Unknown"),
            barangay=barangay,
            geometry=polygon
        )

        parcels.append(parcel)

    return parcels


def load_transmission_line(file_path):
    data = load_json(file_path)
    transmission_lines = []

    for feature in data["features"]:
        properties = feature["properties"]
        line = shape(feature["geometry"])

        transmission_line = TransmissionLineEasement(
            line_id=properties["line_id"],
            geometry=line,
            width_m=properties["width_m"],
            voltage_kv=properties["voltage_kv"]
        )

        transmission_lines.append(transmission_line)

    return transmission_lines


def load_buildings(file_path):
    data = load_json(file_path)
    buildings = []

    for feature in data["features"]:
        geometry = shape(feature["geometry"])

        if not geometry.is_valid:
            geometry = geometry.buffer(0)

        buildings.append(geometry)

    return buildings


def main():
    parcels = load_parcels("data/parcels.json")

    if not parcels:
        print("No parcels loaded.")
        return

    easements = load_transmission_line("data/transmission_line.json")

    if not easements:
        print("No transmission lines loaded.")
        return

    buildings = load_buildings("data/buildings.json")

    checker = EasementChecker(
        parcels,
        easements,
        buildings
    )

    report = checker.find_affected_parcels()

    affected_results = report.results

    lots_with_overlap = sum(
        1 for r in affected_results
        if r["overlap_area"] > 0
    )

    high_risk = sum(
        1 for r in affected_results
        if r["risk"] == "HIGH"
    )

    moderate_risk = sum(
        1 for r in affected_results
        if r["risk"] == "MODERATE"
    )

    print("\n=== AFFECTED PARCELS SUMMARY ===")
    print(f"Lots with Overlap with Transmission Lines: {lots_with_overlap}")
    print(f"High Risk Lots: {high_risk}")
    print(f"Moderate Risk Lots: {moderate_risk}")

    os.makedirs("output", exist_ok=True)

    report.export_csv(
        "output/affected_parcels_report.csv"
    )

    report.export_json(
        "output/affected_parcels_report.json"
    )

    report.export_map(
        parcels,
        easements,
        buildings,
        "output/affected_parcels_map.png"
    )


if __name__ == "__main__":
    main()