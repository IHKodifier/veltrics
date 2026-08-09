class MaintenanceScheduleModel {
  final String id;
  final String organizationId;
  final String vehicleId;
  final String taskName;
  final int intervalKm;
  final int intervalDays;
  final double lastPerformedKm;
  final DateTime? lastPerformedDate;
  final double nextDueKm;
  final DateTime? nextDueDate;
  final bool isActive;
  final DateTime createdAt;
  final DateTime updatedAt;

  MaintenanceScheduleModel({
    required this.id,
    required this.organizationId,
    required this.vehicleId,
    required this.taskName,
    required this.intervalKm,
    required this.intervalDays,
    required this.lastPerformedKm,
    this.lastPerformedDate,
    required this.nextDueKm,
    this.nextDueDate,
    required this.isActive,
    required this.createdAt,
    required this.updatedAt,
  });

  factory MaintenanceScheduleModel.fromJson(Map<String, dynamic> json) {
    return MaintenanceScheduleModel(
      id: json['id'] as String,
      organizationId: json['organization_id'] as String,
      vehicleId: json['vehicle_id'] as String,
      taskName: json['task_name'] as String,
      intervalKm: json['interval_km'] as int,
      intervalDays: json['interval_days'] as int,
      lastPerformedKm: (json['last_performed_km'] as num).toDouble(),
      lastPerformedDate: json['last_performed_date'] != null
          ? DateTime.parse(json['last_performed_date'] as String)
          : null,
      nextDueKm: (json['next_due_km'] as num).toDouble(),
      nextDueDate: json['next_due_date'] != null
          ? DateTime.parse(json['next_due_date'] as String)
          : null,
      isActive: json['is_active'] as bool? ?? true,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }
}

class ServiceRecordModel {
  final String id;
  final String organizationId;
  final String vehicleId;
  final String? maintenanceScheduleId;
  final DateTime serviceDate;
  final double odometerKm;
  final double totalCost;
  final String? serviceCenterName;
  final String? notes;
  final String? performedBy;
  final String? invoicePhotoUrl;
  final DateTime createdAt;
  final DateTime updatedAt;

  ServiceRecordModel({
    required this.id,
    required this.organizationId,
    required this.vehicleId,
    this.maintenanceScheduleId,
    required this.serviceDate,
    required this.odometerKm,
    required this.totalCost,
    this.serviceCenterName,
    this.notes,
    this.performedBy,
    this.invoicePhotoUrl,
    required this.createdAt,
    required this.updatedAt,
  });

  factory ServiceRecordModel.fromJson(Map<String, dynamic> json) {
    return ServiceRecordModel(
      id: json['id'] as String,
      organizationId: json['organization_id'] as String,
      vehicleId: json['vehicle_id'] as String,
      maintenanceScheduleId: json['maintenance_schedule_id'] as String?,
      serviceDate: DateTime.parse(json['service_date'] as String),
      odometerKm: (json['odometer_km'] as num).toDouble(),
      totalCost: (json['total_cost'] as num).toDouble(),
      serviceCenterName: json['service_center_name'] as String?,
      notes: json['notes'] as String?,
      performedBy: json['performed_by'] as String?,
      invoicePhotoUrl: json['invoice_photo_url'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }
}
