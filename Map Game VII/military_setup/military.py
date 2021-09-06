from empire_setup import empires


class Military:

    def __init__(self, unit_type, location_id, owner):
        self.unit_type = unit_type
        self.location_id = location_id
        self.owner = owner
        if self.unit_type != 'infantry' and self.unit_type != 'destroyer':
            self.amount_units_loaded = 0

    def move(self, new_location_id, distance):
        self.location_id = new_location_id

    def load(self, amount_units):
        if self.unit_type == 'airforce':
            if self.amount_units_loaded + amount_units <= 5:
                self.amount_units_loaded += amount_units
            else:
                return
        if self.unit_type == 'transport':
            if self.amount_units_loaded + amount_units <= 10:
                self.amount_units_loaded += amount_units

    def unload(self, amount_units):
        if self.amount_units_loaded - amount_units < 0:
            return
        self.amount_units_loaded -= amount_units
