import 'dart:convert';
import 'package:http/http.dart' as http;
import '../domain/user_model.dart';

class AuthRepository {
  final String baseUrl;

  AuthRepository({this.baseUrl = 'http://127.0.0.1:8000/api/v1'});

  Future<AuthSession> registerWithGoogle({
    required String idToken,
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
      throw Exception('Google Auth Failed: ${response.body}');
    }
  }
}
