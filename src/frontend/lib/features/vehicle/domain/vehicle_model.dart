class VehicleTypeModel {
  final String id;
  final String make;
  final String model;
  final String category;
  final String defaultFuelType;
  final int recommendedOilIntervalKm;
  final int recommendedOilIntervalDays;

  VehicleTypeModel({
    required this.id,
    required this.make,
    required this.model,
    required this.category,
    required this.defaultFuelType,
    required this.recommendedOilIntervalKm,
    required this.recommendedOilIntervalDays,
  });

  factory VehicleTypeModel.fromJson(Map<String, dynamic> json) {
    return VehicleTypeModel(
      id: json['id'] as String,
      make: json['make'] as String,
      model: json['model'] as String,
      category: json['category'] as String? ?? 'Sedan',
      defaultFuelType: json['default_fuel_type'] as String? ?? 'Petrol',
      recommendedOilIntervalKm: json['recommended_oil_interval_km'] as int? ?? 5000,
      recommendedOilIntervalDays: json['recommended_oil_interval_days'] as int? ?? 180,
    );
  }
}

class VehicleModel {
  final String id;
  final String organizationId;
  final String? assignedDriverId;
  final String? vin;
  final String licensePlate;
  final String registrationProvince;
  final String make;
  final String model;
  final int year;
  final String fuelType;
  final double initialOdometerKm;
  final double currentOdometerKm;
  final String status;
  final String? photoUrl;
  final bool isAdRewarded;
  final Map<String, dynamic> customSpecs;

  VehicleModel({
    required this.id,
    required this.organizationId,
    this.assignedDriverId,
    this.vin,
    required this.licensePlate,
    this.registrationProvince = "Punjab",
    required this.make,
    required this.model,
    required this.year,
    required this.fuelType,
    required this.initialOdometerKm,
    required this.currentOdometerKm,
    required this.status,
    this.photoUrl,
    required this.isAdRewarded,
    this.customSpecs = const {},
  });

  factory VehicleModel.fromJson(Map<String, dynamic> json) {
    return VehicleModel(
      id: json['id'] as String,
      organizationId: json['organization_id'] as String,
      assignedDriverId: json['assigned_driver_id'] as String?,
      vin: json['vin'] as String?,
      licensePlate: json['license_plate'] as String,
      registrationProvince: json['registration_province'] as String? ?? 'Punjab',
      make: json['make'] as String,
      model: json['model'] as String,
      year: json['year'] as int,
      fuelType: json['fuel_type'] as String? ?? 'Petrol',
      initialOdometerKm: (json['initial_odometer_km'] as num).toDouble(),
      currentOdometerKm: (json['current_odometer_km'] as num).toDouble(),
      status: json['status'] as String? ?? 'ACTIVE',
      photoUrl: json['photo_url'] as String?,
      isAdRewarded: json['is_ad_rewarded'] as bool? ?? false,
      customSpecs: (json['custom_specs'] as Map<String, dynamic>?) ?? {},
    );
  }
}

class VehicleDetailModel extends VehicleModel {
  final String? assignedDriverName;
  final String? assignedDriverPhone;
  final int activeSchedulesCount;
  final int totalServiceRecordsCount;
  final double totalExpensesCost;

  VehicleDetailModel({
    required super.id,
    required super.organizationId,
    super.assignedDriverId,
    super.vin,
    required super.licensePlate,
    super.registrationProvince = "Punjab",
    required super.make,
    required super.model,
    required super.year,
    required super.fuelType,
    required super.initialOdometerKm,
    required super.currentOdometerKm,
    required super.status,
    super.photoUrl,
    required super.isAdRewarded,
    super.customSpecs = const {},
    this.assignedDriverName,
    this.assignedDriverPhone,
    this.activeSchedulesCount = 0,
    this.totalServiceRecordsCount = 0,
    this.totalExpensesCost = 0.0,
  });

  factory VehicleDetailModel.fromJson(Map<String, dynamic> json) {
    final base = VehicleModel.fromJson(json);
    return VehicleDetailModel(
      id: base.id,
      organizationId: base.organizationId,
      assignedDriverId: base.assignedDriverId,
      vin: base.vin,
      licensePlate: base.licensePlate,
      registrationProvince: base.registrationProvince,
      make: base.make,
      model: base.model,
      year: base.year,
      fuelType: base.fuelType,
      initialOdometerKm: base.initialOdometerKm,
      currentOdometerKm: base.currentOdometerKm,
      status: base.status,
      photoUrl: base.photoUrl,
      isAdRewarded: base.isAdRewarded,
      customSpecs: base.customSpecs,
      assignedDriverName: json['assigned_driver_name'] as String?,
      assignedDriverPhone: json['assigned_driver_phone'] as String?,
      activeSchedulesCount: json['active_schedules_count'] as int? ?? 0,
      totalServiceRecordsCount: json['total_service_records_count'] as int? ?? 0,
      totalExpensesCost: (json['total_expenses_cost'] as num?)?.toDouble() ?? 0.0,
    );
  }
}


