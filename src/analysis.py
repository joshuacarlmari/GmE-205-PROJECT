from report import Report


class RiskAnalyzer:
    def assess_risk(self, overlap_area, distance, voltage_kv, has_structure):
        if distance <= 30:
            return "HIGH"
        elif distance <= 100:
            return "MODERATE"
        return "LOW"


class EasementChecker:
    def __init__(self, parcels, easements, buildings=None):
        self.parcels = parcels
        self.easements = easements
        self.buildings = buildings if buildings else []
        self.risk_analyzer = RiskAnalyzer()

    def parcel_has_building(self, parcel):
        return any(
            parcel.geometry.intersects(building)
            for building in self.buildings
        )

    def find_affected_parcels(self):
        results = []

        for parcel in self.parcels:
            for easement in self.easements:
                corridor = easement.get_corridor()

                overlap_geom = parcel.intersection(corridor)
                overlap_area = 0 if overlap_geom.is_empty else overlap_geom.area

                distance = parcel.geometry.distance(easement.geometry)
                has_structure = self.parcel_has_building(parcel)

                risk = self.risk_analyzer.assess_risk(
                    overlap_area,
                    distance,
                    easement.voltage_kv,
                    has_structure
                )

                within_buffer = parcel.geometry.intersects(
                    easement.geometry.buffer(100)
                )

                if within_buffer and risk in ["HIGH", "MODERATE"]:
                    results.append({
                        "parcel_id": parcel.get_id(),
                        "owner": parcel.owner,
                        "parcel_area": round(parcel.area, 2),
                        "overlap_area": round(overlap_area, 2),
                        "distance": round(distance, 2),
                        "building_present": has_structure,
                        "risk": risk,
                        "barangay": parcel.barangay.name,
                        "municipality": parcel.barangay.municipality.name,
                        "province": parcel.barangay.municipality.province.name
                    })

        return Report(results)