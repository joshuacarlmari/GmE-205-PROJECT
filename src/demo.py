from shapely.geometry import Polygon, LineString

from admin_units import Province, Municipality, Barangay
from spatial import Parcel, TransmissionLineEasement
from analysis import RiskAnalyzer


def main():

    province = Province("Palawan")
    municipality = Municipality("San Vicente", province)
    barangay = Barangay("New Agutaya", municipality)

    overlapping_parcel = Parcel(
        "2289",
        "Imelda De Guzman",
        barangay,
        Polygon([
            (0, 0),
            (10, 0),
            (10, 10),
            (0, 10)
        ])
    )

    buffer_only_parcel = Parcel(
        "2290",
        "Carlos Reyes",
        barangay,
        Polygon([
            (40, 0),
            (50, 0),
            (50, 10),
            (40, 10)
        ])
    )

    transmission_line = TransmissionLineEasement(
        "TL-01",
        LineString([
            (5, -10),
            (5, 20)
        ]),
        width_m=6,
        voltage_kv=230
    )

    spatial_objects = [
        overlapping_parcel,
        buffer_only_parcel,
        transmission_line
    ]

    print("=== POLYMORPHISM DEMO ===\n")

    for obj in spatial_objects:
        print(f"Type: {obj.get_type()}")
        print(f"ID: {obj.get_id()}")
        print(obj.describe())
        print("--------------------------")

    print("\n=== RISK ANALYSIS DEMO ===\n")

    risk_analyzer = RiskAnalyzer()

    for parcel in [overlapping_parcel, buffer_only_parcel]:

        corridor = transmission_line.get_corridor()

        overlap_geom = parcel.geometry.intersection(corridor)

        overlap_area = (
            0 if overlap_geom.is_empty
            else overlap_geom.area
        )

        distance = parcel.geometry.distance(
            transmission_line.geometry
        )

        risk = risk_analyzer.assess_risk(
            overlap_area,
            distance,
            transmission_line.voltage_kv,
            False
        )

        print(f"Parcel ID: {parcel.get_id()}")
        print(f"Owner: {parcel.owner}")
        print(f"Distance from Line: {distance:.2f} m")
        print(f"Overlap Area: {overlap_area:.2f} sq.m")
        print(f"Risk Level: {risk}")
        print("--------------------------")


if __name__ == "__main__":
    main()