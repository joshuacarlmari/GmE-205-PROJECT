class Province:
    def __init__(self, name):
        self.name = name
        self.municipalities = []

    def add_municipality(self, municipality):
        self.municipalities.append(municipality)


class Municipality:
    def __init__(self, name, province):
        self.name = name
        self.province = province
        self.barangays = []
        province.add_municipality(self)

    def add_barangay(self, barangay):
        self.barangays.append(barangay)


class Barangay:
    def __init__(self, name, municipality):
        self.name = name
        self.municipality = municipality
        self.parcels = []
        municipality.add_barangay(self)

    def add_parcel(self, parcel):
        self.parcels.append(parcel)



        