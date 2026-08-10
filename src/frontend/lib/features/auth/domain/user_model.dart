class UserModel {
  final String id;
  final String firebaseUid;
  final String email;
  final String? fullName;
  final String? photoUrl;
  final String authProvider;
  final List<String> linkedProviders;

  UserModel({
    required this.id,
    required this.firebaseUid,
    required this.email,
    this.fullName,
    this.photoUrl,
    required this.authProvider,
    this.linkedProviders = const [],
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    final rawLinked = json['linked_providers'] as List<dynamic>?;
    return UserModel(
      id: json['id'] as String,
      firebaseUid: json['firebase_uid'] as String,
      email: json['email'] as String,
      fullName: json['full_name'] as String?,
      photoUrl: json['photo_url'] as String?,
      authProvider: json['auth_provider'] as String? ?? 'google',
      linkedProviders: rawLinked != null
          ? rawLinked.map((e) => e.toString()).toList()
          : const [],
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

class RefreshTokenTokens {
  final String accessToken;
  final String refreshToken;
  final String tokenType;

  RefreshTokenTokens({
    required this.accessToken,
    required this.refreshToken,
    this.tokenType = 'bearer',
  });

  factory RefreshTokenTokens.fromJson(Map<String, dynamic> json) {
    return RefreshTokenTokens(
      accessToken: json['access_token'] as String,
      refreshToken: json['refresh_token'] as String,
      tokenType: json['token_type'] as String? ?? 'bearer',
    );
  }
}

