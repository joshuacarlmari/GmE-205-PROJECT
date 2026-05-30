class SpatialObject:
    def __init__(self, geometry):
        self.geometry = geometry

    def area(self):
        return self.geometry.area

    def length(self):
        return self.geometry.length

    def intersects(self, other):
        if isinstance(other, SpatialObject):
            return self.geometry.intersects(other.geometry)

        return self.geometry.intersects(other)

    def intersection(self, other):
        if isinstance(other, SpatialObject):
            return self.geometry.intersection(other.geometry)

        return self.geometry.intersection(other)

    def distance(self, other):
        if isinstance(other, SpatialObject):
            return self.geometry.distance(other.geometry)

        return self.geometry.distance(other)

    def get_id(self):
        raise NotImplementedError("Subclasses must implement get_id()")

    def get_type(self):
        raise NotImplementedError("Subclasses must implement get_type()")

    def describe(self):
        raise NotImplementedError("Subclasses must implement describe()")


class Parcel(SpatialObject):
    def __init__(self, lot_no, owner, barangay, geometry):
        super().__init__(geometry)
        self.lot_no = lot_no
        self.owner = owner
        self.barangay = barangay

        barangay.add_parcel(self)

    def cadastral_id(self):
        return (
            f"{self.barangay.municipality.province.name}-"
            f"{self.barangay.municipality.name}-"
            f"{self.barangay.name}-"
            f"{self.lot_no}"
        )

    def get_id(self):
        return self.lot_no

    def get_type(self):
        return "Parcel"

    def describe(self):
        return (
            f"Parcel {self.lot_no} owned by {self.owner}, "
            f"located in {self.barangay.name}, "
            f"with an area of {self.area():.2f} sq.m."
        )


class TransmissionLineEasement(SpatialObject):
    def __init__(self, line_id, geometry, width_m, voltage_kv):
        super().__init__(geometry)
        self.line_id = line_id
        self.width_m = width_m
        self.voltage_kv = voltage_kv

    def get_corridor(self):
        return self.geometry.buffer(self.width_m / 2)

    def get_id(self):
        return self.line_id

    def get_type(self):
        return "Transmission Line Easement"

    def describe(self):
        return (
            f"Transmission line {self.line_id} with {self.voltage_kv} kV "
            f"and easement width of {self.width_m} meters."
        )