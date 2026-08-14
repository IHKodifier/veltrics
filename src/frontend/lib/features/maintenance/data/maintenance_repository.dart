import 'dart:convert';
import 'package:http/http.dart' as http;
import '../domain/maintenance_model.dart';

class MaintenanceRepository {
  final String baseUrl;

  MaintenanceRepository({this.baseUrl = 'http://localhost:8000/api/v1'});

  Future<List<MaintenanceScheduleModel>> getSchedules({
    required String vehicleId,
    required String organizationId,
  }) async {
    final uri = Uri.parse('$baseUrl/maintenance/schedules').replace(queryParameters: {
      'vehicle_id': vehicleId,
    });

    final response = await http.get(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-Organization-ID': organizationId,
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> list = jsonDecode(response.body);
      return list.map((json) => MaintenanceScheduleModel.fromJson(json as Map<String, dynamic>)).toList();
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch maintenance schedules');
    }
  }

  Future<List<ServiceRecordModel>> getServiceHistory({
    required String vehicleId,
    required String organizationId,
    int limit = 50,
    int offset = 0,
  }) async {
    final uri = Uri.parse('$baseUrl/maintenance/records').replace(queryParameters: {
      'vehicle_id': vehicleId,
      'limit': limit.toString(),
      'offset': offset.toString(),
    });

    final response = await http.get(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-Organization-ID': organizationId,
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> list = jsonDecode(response.body);
      return list.map((json) => ServiceRecordModel.fromJson(json as Map<String, dynamic>)).toList();
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch service history records');
    }
  }


  Future<ServiceRecordModel> logMaintenance({
    required Map<String, dynamic> payload,
    required String organizationId,
  }) async {
    final uri = Uri.parse('$baseUrl/maintenance');

    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-Organization-ID': organizationId,
      },
      body: jsonEncode(payload),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return ServiceRecordModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      if (error is Map && error.containsKey('detail')) {
        if (error['detail'] is List) {
          final first = error['detail'][0];
          throw Exception(first['msg'] ?? 'Validation error logging maintenance');
        }
        throw Exception(error['detail']);
      }
      throw Exception('Failed to log maintenance record');
    }
  }

  Future<MaintenanceScheduleModel> createSchedule({
    required Map<String, dynamic> payload,
    required String organizationId,
  }) async {
    final uri = Uri.parse('$baseUrl/maintenance/schedules');

    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-Organization-ID': organizationId,
      },
      body: jsonEncode(payload),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return MaintenanceScheduleModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      if (error is Map && error.containsKey('detail')) {
        if (error['detail'] is List) {
          final first = error['detail'][0];
          throw Exception(first['msg'] ?? 'Validation error creating schedule');
        }
        throw Exception(error['detail']);
      }
      throw Exception('Failed to create maintenance schedule');
    }
  }

  Future<MaintenanceScheduleModel> updateSchedule({
    required String scheduleId,
    required Map<String, dynamic> payload,
    required String organizationId,
  }) async {
    final uri = Uri.parse('$baseUrl/maintenance/schedules/$scheduleId');

    final response = await http.patch(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-Organization-ID': organizationId,
      },
      body: jsonEncode(payload),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return MaintenanceScheduleModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      if (error is Map && error.containsKey('detail')) {
        if (error['detail'] is List) {
          final first = error['detail'][0];
          throw Exception(first['msg'] ?? 'Validation error updating schedule');
        }
        throw Exception(error['detail']);
      }
      throw Exception('Failed to update maintenance schedule');
    }
  }

  Future<void> deleteSchedule({
    required String scheduleId,
    required String organizationId,
  }) async {
    final uri = Uri.parse('$baseUrl/maintenance/schedules/$scheduleId');

    final response = await http.delete(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-Organization-ID': organizationId,
      },
    );

    if (response.statusCode != 200) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to delete maintenance schedule');
    }
  }

  Future<List<MaintenanceScheduleModel>> bulkAcceptSchedules({
    required String vehicleId,
    required String organizationId,
    List<String>? scheduleIds,
  }) async {
    final uri = Uri.parse('$baseUrl/maintenance/schedules/bulk-accept');

    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-Organization-ID': organizationId,
      },
      body: jsonEncode({
        'vehicle_id': vehicleId,
        'schedule_ids': scheduleIds ?? [],
      }),
    );

    if (response.statusCode == 200) {
      final List<dynamic> list = jsonDecode(response.body);
      return list.map((json) => MaintenanceScheduleModel.fromJson(json as Map<String, dynamic>)).toList();
    } else {
      final error = jsonDecode(response.body);
      if (error is Map && error.containsKey('detail')) {
        if (error['detail'] is List) {
          final first = error['detail'][0];
          throw Exception(first['msg'] ?? 'Validation error bulk accepting schedules');
        }
        throw Exception(error['detail']);
      }
      throw Exception('Failed to bulk accept maintenance schedules');
    }
  }
}


