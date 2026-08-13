class FuelLogModel {
  final String id;
  final String organizationId;
  final String vehicleId;
  final String? driverId;
  final DateTime logDate;
  final double odometerKm;
  final String fuelType;
  final double quantityLiters;
  final double pricePerLiter;
  final double totalCost;
  final String currency;
  final String? stationName;
  final String? receiptPhotoUrl;
  final bool isFullTank;
  final double? calculatedEfficiencyKpl;
  final double? distanceKm;
  final bool isLeakAlert;
  final bool anomalyDetected;
  final String? anomalyReason;
  final bool isVerified;
  final DateTime createdAt;

  FuelLogModel({
    required this.id,
    required this.organizationId,
    required this.vehicleId,
    this.driverId,
    required this.logDate,
    required this.odometerKm,
    required this.fuelType,
    required this.quantityLiters,
    required this.pricePerLiter,
    required this.totalCost,
    required this.currency,
    this.stationName,
    this.receiptPhotoUrl,
    required this.isFullTank,
    this.calculatedEfficiencyKpl,
    this.distanceKm,
    this.isLeakAlert = false,
    this.anomalyDetected = false,
    this.anomalyReason,
    this.isVerified = false,
    required this.createdAt,
  });

  factory FuelLogModel.fromJson(Map<String, dynamic> json) {
    return FuelLogModel(
      id: json['id'] as String,
      organizationId: json['organization_id'] as String,
      vehicleId: json['vehicle_id'] as String,
      driverId: json['driver_id'] as String?,
      logDate: DateTime.parse(json['log_date'] as String),
      odometerKm: (json['odometer_km'] as num).toDouble(),
      fuelType: json['fuel_type'] as String? ?? 'Petrol',
      quantityLiters: (json['quantity_liters'] as num).toDouble(),
      pricePerLiter: (json['price_per_liter'] as num).toDouble(),
      totalCost: (json['total_cost'] as num).toDouble(),
      currency: json['currency'] as String? ?? 'PKR',
      stationName: json['station_name'] as String?,
      receiptPhotoUrl: json['receipt_photo_url'] as String?,
      isFullTank: json['is_full_tank'] as bool? ?? true,
      calculatedEfficiencyKpl: json['calculated_efficiency_kpl'] != null
          ? (json['calculated_efficiency_kpl'] as num).toDouble()
          : null,
      distanceKm: json['distance_km'] != null
          ? (json['distance_km'] as num).toDouble()
          : null,
      isLeakAlert: json['is_leak_alert'] as bool? ?? false,
      anomalyDetected: json['anomaly_detected'] as bool? ?? false,
      anomalyReason: json['anomaly_reason'] as String?,
      isVerified: json['is_verified'] as bool? ?? false,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'vehicle_id': vehicleId,
      'odometer_km': odometerKm,
      'quantity_liters': quantityLiters,
      'total_cost': totalCost,
      'fuel_type': fuelType,
      'log_date': logDate.toIso8601String(),
      'is_full_tank': isFullTank,
      if (driverId != null) 'driver_id': driverId,
      if (stationName != null) 'station_name': stationName,
      if (receiptPhotoUrl != null) 'receipt_photo_url': receiptPhotoUrl,
    };
  }
}

class FuelMonthlyTrendModel {
  final String month;
  final double totalCost;
  final double totalLiters;
  final double? avgEfficiencyKpl;

  FuelMonthlyTrendModel({
    required this.month,
    required this.totalCost,
    required this.totalLiters,
    this.avgEfficiencyKpl,
  });

  factory FuelMonthlyTrendModel.fromJson(Map<String, dynamic> json) {
    return FuelMonthlyTrendModel(
      month: json['month'] as String,
      totalCost: (json['total_cost'] as num).toDouble(),
      totalLiters: (json['total_liters'] as num).toDouble(),
      avgEfficiencyKpl: json['avg_efficiency_kpl'] != null
          ? (json['avg_efficiency_kpl'] as num).toDouble()
          : null,
    );
  }
}

class FuelTrendsModel {
  final String? vehicleId;
  final double? vehicleAvgEfficiencyKpl;
  final double fleetAvgEfficiencyKpl;
  final double totalCost;
  final double totalLiters;
  final int totalLogsCount;
  final List<FuelMonthlyTrendModel> monthlyTrends;

  FuelTrendsModel({
    this.vehicleId,
    this.vehicleAvgEfficiencyKpl,
    required this.fleetAvgEfficiencyKpl,
    required this.totalCost,
    required this.totalLiters,
    required this.totalLogsCount,
    required this.monthlyTrends,
  });

  factory FuelTrendsModel.fromJson(Map<String, dynamic> json) {
    return FuelTrendsModel(
      vehicleId: json['vehicle_id'] as String?,
      vehicleAvgEfficiencyKpl: json['vehicle_avg_efficiency_kpl'] != null
          ? (json['vehicle_avg_efficiency_kpl'] as num).toDouble()
          : null,
      fleetAvgEfficiencyKpl: (json['fleet_avg_efficiency_kpl'] as num? ?? 0.0).toDouble(),
      totalCost: (json['total_cost'] as num? ?? 0.0).toDouble(),
      totalLiters: (json['total_liters'] as num? ?? 0.0).toDouble(),
      totalLogsCount: (json['total_logs_count'] as num? ?? 0).toInt(),
      monthlyTrends: (json['monthly_trends'] as List<dynamic>?)
              ?.map((item) => FuelMonthlyTrendModel.fromJson(item as Map<String, dynamic>))
              .toList() ??
          [],
    );
  }
}

