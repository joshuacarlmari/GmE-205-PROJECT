import csv
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx
from matplotlib.patches import Patch


class Report:
    def __init__(self, results):
        self.results = results

    def generate_table(self):
        print("\n=== AFFECTED PARCELS REPORT ===\n")

        for r in self.results:
            print(f"Lot Number: {r['parcel_id']}")
            print(f"Owner: {r['owner']}")
            print(f"Parcel Area: {r['parcel_area']:.2f}")
            print(f"Overlap Area: {r['overlap_area']:.2f}")
            print(f"Distance from Line: {r['distance']:.2f} m")
            print(f"Building Present: {r['building_present']}")
            print(f"Risk Level: {r['risk']}")
            print(f"Location: {r['barangay']}, {r['municipality']}, {r['province']}")
            print("-----------------------------")

    def export_csv(self, filename="affected_parcels_report.csv"):
        if not self.results:
            print("No affected parcels to export.")
            return

        fieldnames = [
            "parcel_id",
            "owner",
            "parcel_area",
            "overlap_area",
            "distance",
            "building_present",
            "risk",
            "barangay",
            "municipality",
            "province"
        ]

        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for r in self.results:
                row = r.copy()
                row["parcel_area"] = round(row["parcel_area"], 2)
                row["overlap_area"] = round(row["overlap_area"], 2)
                row["distance"] = round(row["distance"], 2)
                writer.writerow(row)

        print(f"\nCSV report exported successfully: {filename}")

    def export_txt(self, filename="affected_parcels_report.txt"):
        if not self.results:
            print("No affected parcels to export.")
            return

        with open(filename, "w", encoding="utf-8") as txtfile:
            txtfile.write("=== AFFECTED PARCELS REPORT ===\n\n")

            for r in self.results:
                txtfile.write(f"Lot Number: {r['parcel_id']}\n")
                txtfile.write(f"Owner: {r['owner']}\n")
                txtfile.write(f"Parcel Area: {r['parcel_area']:.2f}\n")
                txtfile.write(f"Overlap Area: {r['overlap_area']:.2f}\n")
                txtfile.write(f"Distance from Line: {r['distance']:.2f} m\n")
                txtfile.write(f"Building Present: {r['building_present']}\n")
                txtfile.write(f"Risk Level: {r['risk']}\n")
                txtfile.write(
                    f"Location: {r['barangay']}, "
                    f"{r['municipality']}, "
                    f"{r['province']}\n"
                )
                txtfile.write("----------------------------------------\n")

        print(f"TXT report exported successfully: {filename}")

    def export_map(self, parcels, easements, buildings=None, filename="affected_parcels_map.png"):
        if not self.results:
            print("No affected parcels to map.")
            return

        if buildings is None:
            buildings = []

        affected_ids = {str(r["parcel_id"]) for r in self.results}

        parcel_geoms = []
        affected_geoms = []

        for p in parcels:
            parcel_geoms.append(p.geometry)

            if str(p.lot_no) in affected_ids or str(p.get_id()) in affected_ids:
                affected_geoms.append(p.geometry)

        if not affected_geoms:
            print("No matching affected parcel geometries found for map.")
            return

        high_buffer_geoms = []
        moderate_buffer_geoms = []
        easement_geoms = []

        for e in easements:
            line = e.geometry
            high_buffer = line.buffer(30)
            moderate_buffer = line.buffer(100).difference(high_buffer)

            high_buffer_geoms.append(high_buffer)
            moderate_buffer_geoms.append(moderate_buffer)
            easement_geoms.append(e.get_corridor())

        crs_ptm_zone2 = "EPSG:3122"

        parcels_gdf = gpd.GeoDataFrame(geometry=parcel_geoms, crs=crs_ptm_zone2)
        affected_gdf = gpd.GeoDataFrame(geometry=affected_geoms, crs=crs_ptm_zone2)
        high_buffer_gdf = gpd.GeoDataFrame(geometry=high_buffer_geoms, crs=crs_ptm_zone2)
        moderate_buffer_gdf = gpd.GeoDataFrame(geometry=moderate_buffer_geoms, crs=crs_ptm_zone2)
        easement_gdf = gpd.GeoDataFrame(geometry=easement_geoms, crs=crs_ptm_zone2)
        buildings_gdf = gpd.GeoDataFrame(geometry=buildings, crs=crs_ptm_zone2)

        parcels_web = parcels_gdf.to_crs(epsg=3857)
        affected_web = affected_gdf.to_crs(epsg=3857)
        high_buffer_web = high_buffer_gdf.to_crs(epsg=3857)
        moderate_buffer_web = moderate_buffer_gdf.to_crs(epsg=3857)
        easement_web = easement_gdf.to_crs(epsg=3857)
        buildings_web = buildings_gdf.to_crs(epsg=3857)

        fig, ax = plt.subplots(figsize=(10, 10))

        xmin, ymin, xmax, ymax = affected_web.total_bounds
        padding = 150

        ax.set_xlim(xmin - padding, xmax + padding)
        ax.set_ylim(ymin - padding, ymax + padding)

        ctx.add_basemap(
            ax,
            source=ctx.providers.Esri.WorldImagery
        )

        parcels_web.plot(
            ax=ax,
            edgecolor="black",
            facecolor="none",
            linewidth=0.5,
            zorder=1
        )

        affected_web.plot(
            ax=ax,
            edgecolor="black",
            facecolor="yellow",
            linewidth=1,
            alpha=0.35,
            zorder=2
        )

        moderate_buffer_web.plot(
            ax=ax,
            edgecolor="orange",
            facecolor="orange",
            alpha=0.15,
            zorder=3
        )

        high_buffer_web.plot(
            ax=ax,
            edgecolor="red",
            facecolor="red",
            alpha=0.25,
            zorder=4
        )

        easement_web.plot(
            ax=ax,
            edgecolor="darkred",
            facecolor="none",
            linewidth=2,
            zorder=5
        )

        if not buildings_web.empty:
            buildings_web.plot(
                ax=ax,
                edgecolor="black",
                facecolor="blue",
                linewidth=0.5,
                alpha=0.8,
                zorder=6
            )

        ax.set_title("Transmission Line Buffer Risk Map")
        ax.set_axis_off()

        legend_elements = [
            Patch(facecolor="white", edgecolor="black", label="Unaffected Parcels"),
            Patch(facecolor="yellow", edgecolor="black", alpha=0.35, label="Affected Parcels"),
            Patch(facecolor="orange", edgecolor="orange", alpha=0.15, label="Moderate Risk Buffer (30–100 m)"),
            Patch(facecolor="red", edgecolor="red", alpha=0.25, label="High Risk Buffer (0–30 m)"),
            Patch(facecolor="none", edgecolor="darkred", label="Transmission Easement"),
            Patch(facecolor="blue", edgecolor="black", alpha=0.8, label="Buildings")
        ]

        ax.legend(handles=legend_elements, loc="upper left")

        plt.savefig(filename, dpi=300, bbox_inches="tight")
        plt.close()

        print(f"\nMap exported successfully: {filename}")

    def summary(self):
        total = len(self.results)
        high = sum(1 for r in self.results if r["risk"] == "HIGH")
        moderate = sum(1 for r in self.results if r["risk"] == "MODERATE")

        print("\n=== SUMMARY ===")
        print(f"Total Reported Parcels: {total}")
        print(f"High Risk Parcels: {high}")
        print(f"Moderate Risk Parcels: {moderate}")