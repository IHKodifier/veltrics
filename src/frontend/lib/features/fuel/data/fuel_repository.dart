import 'dart:convert';
import 'package:http/http.dart' as http;
import '../domain/fuel_log_model.dart';

class FuelRepository {
  final String baseUrl;

  FuelRepository({this.baseUrl = 'http://localhost:8000/api/v1'});

  Future<FuelLogModel> createFuelLog({
    required String vehicleId,
    required double odometerKm,
    required double quantityLiters,
    required double totalCost,
    required String fuelType,
    required DateTime logDate,
    required bool isFullTank,
    String? driverId,
    String? stationName,
    String? receiptPhotoUrl,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/fuel').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final payload = {
      'vehicle_id': vehicleId,
      'odometer_km': odometerKm,
      'quantity_liters': quantityLiters,
      'total_cost': totalCost,
      'fuel_type': fuelType,
      'log_date': logDate.toIso8601String(),
      'is_full_tank': isFullTank,
      if (driverId != null) 'driver_id': driverId,
      if (stationName != null) 'station_name': stationName,
      if (receiptPhotoUrl != null) 'receipt_photo_url': receiptPhotoUrl,
    };

    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
      body: jsonEncode(payload),
    );

    if (response.statusCode == 201 || response.statusCode == 200) {
      return FuelLogModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to log fuel fill-up entry');
    }
  }

  Future<List<FuelLogModel>> getFuelLogs({
    String? vehicleId,
    String? organizationId,
    int? page,
    int? limit,
  }) async {
    final queryParams = <String, String>{};
    if (vehicleId != null && vehicleId.isNotEmpty) {
      queryParams['vehicle_id'] = vehicleId;
    }
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }
    if (page != null) {
      queryParams['page'] = page.toString();
    }
    if (limit != null) {
      queryParams['limit'] = limit.toString();
    }

    final uri = Uri.parse('$baseUrl/fuel').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final response = await http.get(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
    );

    if (response.statusCode == 200) {
      final decoded = jsonDecode(response.body);
      if (decoded is List) {
        return decoded.map((item) => FuelLogModel.fromJson(item as Map<String, dynamic>)).toList();
      } else if (decoded is Map && decoded.containsKey('items')) {
        final List<dynamic> list = decoded['items'];
        return list.map((item) => FuelLogModel.fromJson(item as Map<String, dynamic>)).toList();
      } else {
        return [];
      }
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch fuel logs');
    }
  }

  Future<FuelTrendsModel> getFuelTrends({
    String? vehicleId,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (vehicleId != null && vehicleId.isNotEmpty) {
      queryParams['vehicle_id'] = vehicleId;
    }
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/fuel/trends').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final response = await http.get(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
    );

    if (response.statusCode == 200) {
      return FuelTrendsModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch fuel efficiency trends');
    }
  }

  Future<List<FuelLogModel>> getFuelAnomalies({
    String? organizationId,
    bool unverifiedOnly = true,
  }) async {
    final queryParams = <String, String>{
      'unverified_only': unverifiedOnly.toString(),
      if (organizationId != null && organizationId.isNotEmpty) 'organization_id': organizationId,
    };

    final uri = Uri.parse('$baseUrl/fuel/anomalies').replace(queryParameters: queryParams);
    final response = await http.get(
      uri,
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      final list = jsonDecode(response.body) as List;
      return list.map((i) => FuelLogModel.fromJson(i as Map<String, dynamic>)).toList();
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch fuel anomalies');
    }
  }

  Future<FuelLogModel> verifyFuelAnomaly(String fuelLogId) async {
    final uri = Uri.parse('$baseUrl/fuel/$fuelLogId/verify-anomaly');
    final response = await http.patch(
      uri,
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return FuelLogModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to verify fuel anomaly');
    }
  }

  Future<FuelLogModel> updateFuelLog({
    required String fuelLogId,
    required Map<String, dynamic> data,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/fuel/$fuelLogId').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final response = await http.patch(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
      body: jsonEncode(data),
    );

    if (response.statusCode == 200) {
      return FuelLogModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to update fuel log entry');
    }
  }

  Future<void> deleteFuelLog({
    required String fuelLogId,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/fuel/$fuelLogId').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final response = await http.delete(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
    );

    if (response.statusCode != 200) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to delete fuel log entry');
    }
  }
}


