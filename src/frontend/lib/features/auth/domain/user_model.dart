class UserModel {
  final String id;
  final String firebaseUid;
  final String email;
  final String? fullName;
  final String? photoUrl;
  final String authProvider;

  UserModel({
    required this.id,
    required this.firebaseUid,
    required this.email,
    this.fullName,
    this.photoUrl,
    required this.authProvider,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      firebaseUid: json['firebase_uid'] as String,
      email: json['email'] as String,
      fullName: json['full_name'] as String?,
      photoUrl: json['photo_url'] as String?,
      authProvider: json['auth_provider'] as String? ?? 'google',
    );
  }
}

class OrganizationModel {
  final String id;
  final String name;
  final String ownerId;
  final bool isPersonal;
  final int maxVehicles;

  OrganizationModel({
    required this.id,
    required this.name,
    required this.ownerId,
    required this.isPersonal,
    required this.maxVehicles,
  });

  factory OrganizationModel.fromJson(Map<String, dynamic> json) {
    return OrganizationModel(
      id: json['id'] as String,
      name: json['name'] as String,
      ownerId: json['owner_id'] as String,
      isPersonal: json['is_personal'] as bool? ?? true,
      maxVehicles: json['max_vehicles'] as int? ?? 3,
    );
  }
}

class AuthSession {
  final String accessToken;
  final String refreshToken;
  final UserModel user;
  final OrganizationModel organization;

  AuthSession({
    required this.accessToken,
    required this.refreshToken,
    required this.user,
    required this.organization,
  });

  factory AuthSession.fromJson(Map<String, dynamic> json) {
    return AuthSession(
      accessToken: json['access_token'] as String,
      refreshToken: json['refresh_token'] as String,
      user: UserModel.fromJson(json['user'] as Map<String, dynamic>),
      organization: OrganizationModel.fromJson(json['organization'] as Map<String, dynamic>),
    );
  }
}
