class OrganizationInvitationModel {
  final String id;
  final String organizationId;
  final String email;
  final String role;
  final String token;
  final String status;
  final String? invitedByUserId;
  final DateTime? expiresAt;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  OrganizationInvitationModel({
    required this.id,
    required this.organizationId,
    required this.email,
    required this.role,
    required this.token,
    required this.status,
    this.invitedByUserId,
    this.expiresAt,
    this.createdAt,
    this.updatedAt,
  });

  factory OrganizationInvitationModel.fromJson(Map<String, dynamic> json) {
    return OrganizationInvitationModel(
      id: json['id'] as String,
      organizationId: json['organization_id'] as String,
      email: json['email'] as String,
      role: json['role'] as String,
      token: json['token'] as String,
      status: json['status'] as String? ?? 'PENDING',
      invitedByUserId: json['invited_by_user_id'] as String?,
      expiresAt: json['expires_at'] != null ? DateTime.parse(json['expires_at']) : null,
      createdAt: json['created_at'] != null ? DateTime.parse(json['created_at']) : null,
      updatedAt: json['updated_at'] != null ? DateTime.parse(json['updated_at']) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'organization_id': organizationId,
      'email': email,
      'role': role,
      'token': token,
      'status': status,
      'invited_by_user_id': invitedByUserId,
      'expires_at': expiresAt?.toIso8601String(),
      'created_at': createdAt?.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
    };
  }
}
