class OrganizationModel {
  final String id;
  final String name;
  final String? ownerId;
  final bool isPersonal;
  final int maxVehicles;
  final int maxDrivers;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  OrganizationModel({
    required this.id,
    required this.name,
    this.ownerId,
    required this.isPersonal,
    required this.maxVehicles,
    required this.maxDrivers,
    this.createdAt,
    this.updatedAt,
  });

  factory OrganizationModel.fromJson(Map<String, dynamic> json) {
    return OrganizationModel(
      id: json['id'] as String,
      name: json['name'] as String,
      ownerId: json['owner_id'] as String?,
      isPersonal: json['is_personal'] as bool? ?? false,
      maxVehicles: json['max_vehicles'] as int? ?? 3,
      maxDrivers: json['max_drivers'] as int? ?? 3,
      createdAt: json['created_at'] != null ? DateTime.parse(json['created_at']) : null,
      updatedAt: json['updated_at'] != null ? DateTime.parse(json['updated_at']) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'owner_id': ownerId,
      'is_personal': isPersonal,
      'max_vehicles': maxVehicles,
      'max_drivers': maxDrivers,
      'created_at': createdAt?.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
    };
  }
}
