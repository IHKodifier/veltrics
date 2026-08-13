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
    required String vehicleId,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{'vehicle_id': vehicleId};
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/fuel').replace(queryParameters: queryParams);

    final response = await http.get(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> list = jsonDecode(response.body);
      return list.map((item) => FuelLogModel.fromJson(item as Map<String, dynamic>)).toList();
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch fuel logs');
    }
  }
}
