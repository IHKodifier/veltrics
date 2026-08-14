import 'dart:convert';
import 'package:http/http.dart' as http;
import '../domain/user_model.dart';

class AuthRepository {
  final String baseUrl;

  AuthRepository({this.baseUrl = 'http://localhost:8000/api/v1'});

  Future<AuthSession> registerWithGoogle({
    required String idToken,
    String? email,
    String? fullName,
    String? photoUrl,
    String? firebaseUid,
  }) async {
    return _register(
      idToken: idToken,
      authProvider: 'google',
      email: email,
      fullName: fullName,
      photoUrl: photoUrl,
      firebaseUid: firebaseUid,
    );
  }

  Future<AuthSession> registerWithFacebook({
    required String idToken,
    String? email,
    String? fullName,
    String? photoUrl,
    String? firebaseUid,
  }) async {
    return _register(
      idToken: idToken,
      authProvider: 'facebook',
      email: email,
      fullName: fullName,
      photoUrl: photoUrl,
      firebaseUid: firebaseUid,
    );
  }

  Future<AuthSession> registerWithEmail({
    required String email,
    required String password,
    String? fullName,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'auth_provider': 'email',
        'email': email,
        'password': password,
        'full_name': fullName,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return AuthSession.fromJson(data);
    } else {
      throw Exception('Auth Failed (email): ${response.body}');
    }
  }

  Future<AuthSession> loginWithEmail({
    required String email,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return AuthSession.fromJson(data);
    } else {
      final errorMap = jsonDecode(response.body);
      final detail = errorMap is Map ? errorMap['detail'] : response.body;
      throw Exception(detail ?? 'Login Failed');
    }
  }

  // Unified Sign In Wrappers (UC-005)
  Future<AuthSession> signInWithGoogle({
    required String idToken,
    String? email,
    String? fullName,
    String? photoUrl,
    String? firebaseUid,
  }) => registerWithGoogle(
    idToken: idToken,
    email: email,
    fullName: fullName,
    photoUrl: photoUrl,
    firebaseUid: firebaseUid,
  );

  Future<AuthSession> signInWithFacebook({
    required String idToken,
    String? email,
    String? fullName,
    String? photoUrl,
    String? firebaseUid,
  }) => registerWithFacebook(
    idToken: idToken,
    email: email,
    fullName: fullName,
    photoUrl: photoUrl,
    firebaseUid: firebaseUid,
  );

  Future<AuthSession> signInWithEmail({
    required String email,
    required String password,
  }) => loginWithEmail(
    email: email,
    password: password,
  );

  Future<Map<String, dynamic>> forgotPassword({required String email}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/forgot-password'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body) as Map<String, dynamic>;
    } else {
      final errorMap = jsonDecode(response.body);
      final detail = errorMap is Map ? errorMap['detail'] : response.body;
      throw Exception(detail ?? 'Forgot Password Request Failed');
    }
  }

  Future<Map<String, dynamic>> resetPassword({
    required String token,
    required String newPassword,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/reset-password'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'token': token,
        'new_password': newPassword,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body) as Map<String, dynamic>;
    } else {
      final errorMap = jsonDecode(response.body);
      final detail = errorMap is Map ? errorMap['detail'] : response.body;
      throw Exception(detail ?? 'Reset Password Failed');
    }
  }

  Future<Map<String, dynamic>> getProfile({required String userId}) async {
    final response = await http.get(
      Uri.parse('$baseUrl/users/me'),
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId,
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body) as Map<String, dynamic>;
    } else {
      throw Exception('Failed to fetch profile: ${response.body}');
    }
  }

  Future<Map<String, dynamic>> updateProfile({
    required String userId,
    String? fullName,
    String? phoneNumber,
    String? city,
    String? jobRole,
    String? avatarUrl,
  }) async {
    final response = await http.patch(
      Uri.parse('$baseUrl/users/me'),
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId,
      },
      body: jsonEncode({
        if (fullName != null) 'full_name': fullName,
        if (phoneNumber != null) 'phone_number': phoneNumber,
        if (city != null) 'city': city,
        if (jobRole != null) 'job_role': jobRole,
        if (avatarUrl != null) 'avatar_url': avatarUrl,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body) as Map<String, dynamic>;
    } else {
      final errorMap = jsonDecode(response.body);
      final detail = errorMap is Map ? errorMap['detail'] : response.body;
      throw Exception(detail ?? 'Failed to update profile');
    }
  }

  Future<AuthSession> completeProfile({
    required String userId,
    String? fullName,
    String? phoneNumber,
    String? city,
    String? jobRole,
    String? avatarUrl,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/users/me/complete-profile'),
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId,
      },
      body: jsonEncode({
        if (fullName != null) 'full_name': fullName,
        if (phoneNumber != null) 'phone_number': phoneNumber,
        if (city != null) 'city': city,
        if (jobRole != null) 'job_role': jobRole,
        if (avatarUrl != null) 'avatar_url': avatarUrl,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return AuthSession.fromJson(data);
    } else {
      final errorMap = jsonDecode(response.body);
      final detail = errorMap is Map ? errorMap['detail'] : response.body;
      throw Exception(detail ?? 'Failed to complete profile');
    }
  }




  Future<AuthSession> _register({
    required String idToken,
    required String authProvider,
    String? email,
    String? fullName,
    String? photoUrl,
    String? firebaseUid,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'id_token': idToken,
        'auth_provider': authProvider,
        'email': email,
        'full_name': fullName,
        'photo_url': photoUrl,
        'firebase_uid': firebaseUid,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return AuthSession.fromJson(data);
    } else {
      throw Exception('Auth Failed ($authProvider): ${response.body}');
    }
  }

  Future<RefreshTokenTokens> refreshToken({required String refreshToken}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/refresh'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'refresh_token': refreshToken}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return RefreshTokenTokens.fromJson(data);
    } else {
      final errorMap = jsonDecode(response.body);
      final detail = errorMap is Map ? errorMap['detail'] : response.body;
      throw Exception(detail ?? 'Token Refresh Failed');
    }
  }

  Future<RefreshTokenTokens> silentRefresh({required String refreshToken}) =>
      this.refreshToken(refreshToken: refreshToken);

  Future<void> logout({required String refreshToken}) async {
    try {
      await http.post(
        Uri.parse('$baseUrl/auth/logout'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'refresh_token': refreshToken}),
      );
    } catch (_) {
      // Network failure during API logout -> Client forces local credential purge regardless.
    }
  }

  Future<void> deleteAccount({required String userId}) async {
    final response = await http.delete(
      Uri.parse('$baseUrl/users/me'),
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId,
      },
    );

    if (response.statusCode == 200) {
      return;
    } else {
      final errorMap = jsonDecode(response.body);
      final detail = errorMap is Map ? errorMap['detail'] : response.body;
      throw Exception(detail ?? 'Failed to delete account');
    }
  }
}


