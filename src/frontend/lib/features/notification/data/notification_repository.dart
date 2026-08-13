import 'dart:convert';
import 'package:http/http.dart' as http;
import '../domain/notification_model.dart';

class NotificationRepository {
  final String baseUrl;

  NotificationRepository({this.baseUrl = 'http://localhost:8000/api/v1'});

  Future<void> registerDeviceToken({
    required String userId,
    required String deviceToken,
    String deviceType = 'ANDROID',
  }) async {
    final uri = Uri.parse('$baseUrl/notifications/devices');
    final payload = {
      'user_id': userId,
      'device_token': deviceToken,
      'device_type': deviceType,
    };

    final response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(payload),
    );

    if (response.statusCode != 201) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to register FCM device token');
    }
  }

  Future<NotificationPaginatedModel> getNotifications({
    required String userId,
    String? organizationId,
    bool unreadOnly = false,
  }) async {
    final queryParams = <String, String>{
      'user_id': userId,
      'unread_only': unreadOnly.toString(),
      if (organizationId != null && organizationId.isNotEmpty) 'organization_id': organizationId,
    };

    final uri = Uri.parse('$baseUrl/notifications').replace(queryParameters: queryParams);
    final response = await http.get(
      uri,
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return NotificationPaginatedModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch notifications');
    }
  }

  Future<NotificationModel> markAsRead({
    required String userId,
    required String notificationId,
  }) async {
    final uri = Uri.parse('$baseUrl/notifications/$notificationId/read?user_id=$userId');
    final response = await http.patch(
      uri,
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return NotificationModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to mark notification as read');
    }
  }

  Future<void> markAllAsRead({
    required String userId,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{
      'user_id': userId,
      if (organizationId != null && organizationId.isNotEmpty) 'organization_id': organizationId,
    };

    final uri = Uri.parse('$baseUrl/notifications/mark-all-read').replace(queryParameters: queryParams);
    final response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode != 200) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to mark all notifications as read');
    }
  }

  Future<void> updatePreferences({
    required String userId,
    required bool maintenanceReminders,
    required bool documentExpirations,
    required bool quotaAlerts,
    required bool systemNews,
  }) async {
    final uri = Uri.parse('$baseUrl/notifications/preferences');
    final payload = {
      'user_id': userId,
      'maintenance_reminders': maintenanceReminders,
      'document_expirations': documentExpirations,
      'quota_alerts': quotaAlerts,
      'system_news': systemNews,
    };

    final response = await http.patch(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(payload),
    );

    if (response.statusCode != 200) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to update notification preferences');
    }
  }
}
