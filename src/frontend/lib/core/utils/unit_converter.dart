enum UnitSystem { metric, imperial }

class UnitConverter {
  static const double kmToMiles = 0.621371;
  static const double litersToGallons = 0.264172;
  static const double kmLToMpg = 2.35215;

  static double distance(double km, UnitSystem system) {
    if (system == UnitSystem.imperial) {
      return double.parse((km * kmToMiles).toStringAsFixed(2));
    }
    return double.parse(km.toStringAsFixed(2));
  }

  static String distanceLabel(double km, UnitSystem system) {
    final val = distance(km, system);
    final unit = system == UnitSystem.imperial ? 'mi' : 'km';
    return '$val $unit';
  }

  static double volume(double liters, UnitSystem system) {
    if (system == UnitSystem.imperial) {
      return double.parse((liters * litersToGallons).toStringAsFixed(2));
    }
    return double.parse(liters.toStringAsFixed(2));
  }

  static String volumeLabel(double liters, UnitSystem system) {
    final val = volume(liters, system);
    final unit = system == UnitSystem.imperial ? 'gal' : 'L';
    return '$val $unit';
  }

  static double efficiency(double kmPerL, UnitSystem system) {
    if (system == UnitSystem.imperial) {
      return double.parse((kmPerL * kmLToMpg).toStringAsFixed(2));
    }
    return double.parse(kmPerL.toStringAsFixed(2));
  }

  static String efficiencyLabel(double kmPerL, UnitSystem system) {
    final val = efficiency(kmPerL, system);
    final unit = system == UnitSystem.imperial ? 'MPG' : 'km/L';
    return '$val $unit';
  }
}
