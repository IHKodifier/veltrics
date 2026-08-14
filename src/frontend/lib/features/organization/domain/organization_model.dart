class OrganizationModel {
  final String id;
  final String name;
  final String? ownerId;
  final bool isPersonal;
  final int maxVehicles;
  final int maxDrivers;
  final String? address;
  final String? phone;
  final String? taxId;
  final String currency;
  final String? website;
  final String? logoUrl;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  OrganizationModel({
    required this.id,
    required this.name,
    this.ownerId,
    required this.isPersonal,
    required this.maxVehicles,
    required this.maxDrivers,
    this.address,
    this.phone,
    this.taxId,
    this.currency = 'USD',
    this.website,
    this.logoUrl,
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
      address: json['address'] as String?,
      phone: json['phone'] as String?,
      taxId: json['tax_id'] as String?,
      currency: (json['currency'] as String?) ?? 'USD',
      website: json['website'] as String?,
      logoUrl: json['logo_url'] as String?,
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
      'address': address,
      'phone': phone,
      'tax_id': taxId,
      'currency': currency,
      'website': website,
      'logo_url': logoUrl,
      'created_at': createdAt?.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
    };
  }
}
