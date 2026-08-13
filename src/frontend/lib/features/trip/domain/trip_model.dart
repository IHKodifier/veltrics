class TripModel {
  final String id;
  final String organizationId;
  final String vehicleId;
  final String? driverId;
  final DateTime startTime;
  final DateTime? endTime;
  final String? originName;
  final String? destinationName;
  final double startOdometerKm;
  final double? endOdometerKm;
  final double? distanceKm;
  final String tripPurpose;
  final bool isManual;
  final String status;
  final String? gpsPolylineJson;
  final String? notes;
  final DateTime createdAt;
  final DateTime updatedAt;

  TripModel({
    required this.id,
    required this.organizationId,
    required this.vehicleId,
    this.driverId,
    required this.startTime,
    this.endTime,
    this.originName,
    this.destinationName,
    required this.startOdometerKm,
    this.endOdometerKm,
    this.distanceKm,
    required this.tripPurpose,
    required this.isManual,
    required this.status,
    this.gpsPolylineJson,
    this.notes,
    required this.createdAt,
    required this.updatedAt,
  });

  factory TripModel.fromJson(Map<String, dynamic> json) {
    return TripModel(
      id: json['id'] as String,
      organizationId: json['organization_id'] as String,
      vehicleId: json['vehicle_id'] as String,
      driverId: json['driver_id'] as String?,
      startTime: DateTime.parse(json['start_time'] as String),
      endTime: json['end_time'] != null ? DateTime.parse(json['end_time'] as String) : null,
      originName: json['origin_name'] as String?,
      destinationName: json['destination_name'] as String?,
      startOdometerKm: (json['start_odometer_km'] as num).toDouble(),
      endOdometerKm: json['end_odometer_km'] != null ? (json['end_odometer_km'] as num).toDouble() : null,
      distanceKm: json['distance_km'] != null ? (json['distance_km'] as num).toDouble() : null,
      tripPurpose: json['trip_purpose'] as String? ?? 'BUSINESS',
      isManual: json['is_manual'] as bool? ?? false,
      status: json['status'] as String? ?? 'IN_PROGRESS',
      gpsPolylineJson: json['gps_polyline_json'] as String?,
      notes: json['notes'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'organization_id': organizationId,
      'vehicle_id': vehicleId,
      'driver_id': driverId,
      'start_time': startTime.toIso8601String(),
      'end_time': endTime?.toIso8601String(),
      'origin_name': originName,
      'destination_name': destinationName,
      'start_odometer_km': startOdometerKm,
      'end_odometer_km': endOdometerKm,
      'distance_km': distanceKm,
      'trip_purpose': tripPurpose,
      'is_manual': isManual,
      'status': status,
      'gps_polyline_json': gpsPolylineJson,
      'notes': notes,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}

class TripSummaryModel {
  final String? vehicleId;
  final double totalDistanceKm;
  final double businessDistanceKm;
  final double personalDistanceKm;
  final int totalTripsCount;
  final double estimatedTaxDeduction;

  TripSummaryModel({
    this.vehicleId,
    required this.totalDistanceKm,
    required this.businessDistanceKm,
    required this.personalDistanceKm,
    required this.totalTripsCount,
    required this.estimatedTaxDeduction,
  });

  factory TripSummaryModel.fromJson(Map<String, dynamic> json) {
    return TripSummaryModel(
      vehicleId: json['vehicle_id'] as String?,
      totalDistanceKm: (json['total_distance_km'] as num).toDouble(),
      businessDistanceKm: (json['business_distance_km'] as num).toDouble(),
      personalDistanceKm: (json['personal_distance_km'] as num).toDouble(),
      totalTripsCount: json['total_trips_count'] as int,
      estimatedTaxDeduction: (json['estimated_tax_deduction'] as num).toDouble(),
    );
  }
}

class MileageSummaryModel {
  final String? vehicleId;
  final double totalDistanceKm;
  final double businessDistanceKm;
  final double personalDistanceKm;
  final int totalTripsCount;
  final int businessTripsCount;
  final int personalTripsCount;
  final double averageTripDistanceKm;
  final double estimatedTaxDeduction;

  MileageSummaryModel({
    this.vehicleId,
    required this.totalDistanceKm,
    required this.businessDistanceKm,
    required this.personalDistanceKm,
    required this.totalTripsCount,
    required this.businessTripsCount,
    required this.personalTripsCount,
    required this.averageTripDistanceKm,
    required this.estimatedTaxDeduction,
  });

  factory MileageSummaryModel.fromJson(Map<String, dynamic> json) {
    return MileageSummaryModel(
      vehicleId: json['vehicle_id'] as String?,
      totalDistanceKm: (json['total_distance_km'] as num).toDouble(),
      businessDistanceKm: (json['business_distance_km'] as num).toDouble(),
      personalDistanceKm: (json['personal_distance_km'] as num).toDouble(),
      totalTripsCount: json['total_trips_count'] as int,
      businessTripsCount: json['business_trips_count'] as int? ?? 0,
      personalTripsCount: json['personal_trips_count'] as int? ?? 0,
      averageTripDistanceKm: (json['average_trip_distance_km'] as num? ?? 0.0).toDouble(),
      estimatedTaxDeduction: (json['estimated_tax_deduction'] as num).toDouble(),
    );
  }
}


