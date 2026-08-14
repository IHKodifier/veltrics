import pytest

class UnitConverter:
    KM_TO_MILES = 0.621371
    LITERS_TO_GALLONS = 0.264172
    KML_TO_MPG = 2.35215

    @classmethod
    def convert_distance(cls, km: float, unit_system: str) -> float:
        if unit_system.upper() == "IMPERIAL":
            return round(km * cls.KM_TO_MILES, 2)
        return round(km, 2)

    @classmethod
    def convert_volume(cls, liters: float, unit_system: str) -> float:
        if unit_system.upper() == "IMPERIAL":
            return round(liters * cls.LITERS_TO_GALLONS, 2)
        return round(liters, 2)

    @classmethod
    def convert_efficiency(cls, km_per_l: float, unit_system: str) -> float:
        if unit_system.upper() == "IMPERIAL":
            return round(km_per_l * cls.KML_TO_MPG, 2)
        return round(km_per_l, 2)

def test_uc114_metric_returns_original_values():
    assert UnitConverter.convert_distance(100.0, "METRIC") == 100.0
    assert UnitConverter.convert_volume(50.0, "METRIC") == 50.0
    assert UnitConverter.convert_efficiency(15.0, "METRIC") == 15.0

def test_uc114_imperial_conversions():
    # 100 km -> 62.14 miles
    assert UnitConverter.convert_distance(100.0, "IMPERIAL") == 62.14
    # 50 liters -> 13.21 gallons
    assert UnitConverter.convert_volume(50.0, "IMPERIAL") == 13.21
    # 15 km/L -> 35.28 MPG
    assert UnitConverter.convert_efficiency(15.0, "IMPERIAL") == 35.28
