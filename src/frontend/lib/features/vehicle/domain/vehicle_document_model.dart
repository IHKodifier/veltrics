class VehicleDocumentModel {
  final String id;
  final String vehicleId;
  final String organizationId;
  final String documentType;
  final String documentUrl;
  final String? fileName;
  final DateTime? expirationDate;
  final DateTime? createdAt;

  VehicleDocumentModel({
    required this.id,
    required this.vehicleId,
    required this.organizationId,
    required this.documentType,
    required this.documentUrl,
    this.fileName,
    this.expirationDate,
    this.createdAt,
  });

  factory VehicleDocumentModel.fromJson(Map<String, dynamic> json) {
    return VehicleDocumentModel(
      id: json['id'] as String,
      vehicleId: json['vehicle_id'] as String,
      organizationId: json['organization_id'] as String,
      documentType: json['document_type'] as String,
      documentUrl: json['document_url'] as String,
      fileName: json['file_name'] as String?,
      expirationDate: json['expiration_date'] != null ? DateTime.parse(json['expiration_date']) : null,
      createdAt: json['created_at'] != null ? DateTime.parse(json['created_at']) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'vehicle_id': vehicleId,
      'organization_id': organizationId,
      'document_type': documentType,
      'document_url': documentUrl,
      'file_name': fileName,
      'expiration_date': expirationDate?.toIso8601String(),
      'created_at': createdAt?.toIso8601String(),
    };
  }
}
