import 'dart:convert';
import 'package:http/http.dart' as http;
import '../domain/vehicle_model.dart';
import '../domain/vehicle_document_model.dart';

class VehicleRepository {
  final String baseUrl;

  VehicleRepository({this.baseUrl = 'http://localhost:8000/api/v1'});

  Future<List<VehicleTypeModel>> searchVehicleTypes({String? query, String? make}) async {
    final queryParams = <String, String>{};
    if (query != null && query.isNotEmpty) queryParams['q'] = query;
    if (make != null && make.isNotEmpty) queryParams['make'] = make;

    final uri = Uri.parse('$baseUrl/vehicles/types').replace(queryParameters: queryParams);
    final response = await http.get(uri);

    if (response.statusCode == 200) {
      final List<dynamic> list = jsonDecode(response.body);
      return list.map((json) => VehicleTypeModel.fromJson(json as Map<String, dynamic>)).toList();
    } else {
      throw Exception('Failed to fetch vehicle types: ${response.body}');
    }
  }

  Future<VehicleModel> createVehicle({
    required String organizationId,
    required String licensePlate,
    String registrationProvince = "Punjab",
    required String make,
    required String model,
    required int year,
    required String fuelType,
    required double initialOdometerKm,
    String? vin,
    String? photoUrl,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/vehicles'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'organization_id': organizationId,
        'license_plate': licensePlate,
        'registration_province': registrationProvince,
        'make': make,
        'model': model,
        'year': year,
        'fuel_type': fuelType,
        'initial_odometer_km': initialOdometerKm,
        'current_odometer_km': initialOdometerKm,
        'vin': vin,
        'photo_url': photoUrl,
      }),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return VehicleModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to register vehicle');
    }
  }

  Future<List<VehicleModel>> getVehicles({
    required String organizationId,
    String? status,
    String? search,
    String? province,
    String? fuelType,
  }) async {
    final queryParams = <String, String>{'organization_id': organizationId};
    if (status != null && status.isNotEmpty && status.toUpperCase() != 'ALL') {
      queryParams['status'] = status;
    }
    if (search != null && search.isNotEmpty) queryParams['search'] = search;
    if (province != null && province.isNotEmpty) queryParams['province'] = province;
    if (fuelType != null && fuelType.isNotEmpty) queryParams['fuel_type'] = fuelType;

    final uri = Uri.parse('$baseUrl/vehicles').replace(queryParameters: queryParams);
    final response = await http.get(uri);

    if (response.statusCode == 200) {
      final List<dynamic> list = jsonDecode(response.body);
      return list.map((json) => VehicleModel.fromJson(json as Map<String, dynamic>)).toList();
    } else {
      throw Exception('Failed to fetch vehicles: ${response.body}');
    }
  }

  Future<VehicleDetailModel> getVehicleDetail({
    required String vehicleId,
    required String organizationId,
  }) async {
    final uri = Uri.parse('$baseUrl/vehicles/$vehicleId').replace(queryParameters: {
      'organization_id': organizationId,
    });
    final response = await http.get(uri);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return VehicleDetailModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch vehicle detail');
    }
  }

  Future<VehicleModel> updateVehicleStatus({
    required String vehicleId,
    required String organizationId,
    required String status,
  }) async {
    final uri = Uri.parse('$baseUrl/vehicles/$vehicleId/status').replace(queryParameters: {
      'organization_id': organizationId,
    });
    final response = await http.patch(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'status': status}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return VehicleModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to update vehicle status');
    }
  }

  Future<VehicleModel> updateVehicle({
    required String vehicleId,
    required String organizationId,
    String? licensePlate,
    String? registrationProvince,
    String? make,
    String? model,
    int? year,
    String? fuelType,
    double? currentOdometerKm,
    String? photoUrl,
    Map<String, dynamic>? customSpecs,
  }) async {
    final uri = Uri.parse('$baseUrl/vehicles/$vehicleId').replace(queryParameters: {
      'organization_id': organizationId,
    });

    final payload = <String, dynamic>{};
    if (licensePlate != null) payload['license_plate'] = licensePlate;
    if (registrationProvince != null) payload['registration_province'] = registrationProvince;
    if (make != null) payload['make'] = make;
    if (model != null) payload['model'] = model;
    if (year != null) payload['year'] = year;
    if (fuelType != null) payload['fuel_type'] = fuelType;
    if (currentOdometerKm != null) payload['current_odometer_km'] = currentOdometerKm;
    if (photoUrl != null) payload['photo_url'] = photoUrl;
    if (customSpecs != null) payload['custom_specs'] = customSpecs;

    final response = await http.patch(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(payload),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return VehicleModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to update vehicle details');
    }
  }

  Future<void> deleteVehicle({
    required String vehicleId,
    required String organizationId,
    String? userId,
  }) async {
    final uri = Uri.parse('$baseUrl/vehicles/$vehicleId').replace(queryParameters: {
      'organization_id': organizationId,
    });

    final headers = <String, String>{
      'Content-Type': 'application/json',
    };
    if (userId != null) headers['X-User-ID'] = userId;

    final response = await http.delete(uri, headers: headers);

    if (response.statusCode != 200 && response.statusCode != 204) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to soft delete vehicle');
    }
  }

  Future<VehicleModel> updateOdometer({
    required String vehicleId,
    required String organizationId,
    required double currentOdometerKm,
    bool isCorrection = false,
    String? userId,
  }) async {
    final uri = Uri.parse('$baseUrl/vehicles/$vehicleId/odometer').replace(queryParameters: {
      'organization_id': organizationId,
    });

    final headers = <String, String>{
      'Content-Type': 'application/json',
    };
    if (userId != null) headers['X-User-ID'] = userId;

    final response = await http.post(
      uri,
      headers: headers,
      body: jsonEncode({
        'current_odometer_km': currentOdometerKm,
        'is_correction': isCorrection,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return VehicleModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to update odometer reading');
    }
  }

  Future<VehicleDocumentModel> uploadDocument({
    required String vehicleId,
    required String organizationId,
    required String documentType,
    required String documentUrl,
    String? fileName,
    DateTime? expirationDate,
  }) async {
    final uri = Uri.parse('$baseUrl/vehicles/$vehicleId/documents').replace(queryParameters: {
      'organization_id': organizationId,
    });

    final response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'document_type': documentType,
        'document_url': documentUrl,
        'file_name': fileName,
        'expiration_date': expirationDate?.toIso8601String(),
      }),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return VehicleDocumentModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to upload vehicle document');
    }
  }

  Future<List<VehicleDocumentModel>> getVehicleDocuments({
    required String vehicleId,
    required String organizationId,
  }) async {
    final uri = Uri.parse('$baseUrl/vehicles/$vehicleId/documents').replace(queryParameters: {
      'organization_id': organizationId,
    });

    final response = await http.get(uri);

    if (response.statusCode == 200) {
      final List<dynamic> list = jsonDecode(response.body);
      return list.map((json) => VehicleDocumentModel.fromJson(json as Map<String, dynamic>)).toList();
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch vehicle documents');
    }
  }

  Future<VehicleModel> restoreVehicle({
    required String vehicleId,
    required String organizationId,
    String? userId,
  }) async {
    final uri = Uri.parse('$baseUrl/vehicles/$vehicleId/restore').replace(queryParameters: {
      'organization_id': organizationId,
    });

    final headers = <String, String>{
      'Content-Type': 'application/json',
    };
    if (userId != null) headers['X-User-ID'] = userId;

    final response = await http.post(uri, headers: headers);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return VehicleModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to restore vehicle');
    }
  }

  Future<VehicleModel> assignDriver({
    required String vehicleId,
    required String organizationId,
    required String driverId,
    String? userId,
  }) async {
    final uri = Uri.parse('$baseUrl/vehicles/$vehicleId/assign-driver').replace(queryParameters: {
      'organization_id': organizationId,
    });

    final headers = <String, String>{
      'Content-Type': 'application/json',
    };
    if (userId != null) headers['X-User-ID'] = userId;

    final response = await http.post(
      uri,
      headers: headers,
      body: jsonEncode({'driver_id': driverId}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return VehicleModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to assign driver');
    }
  }

  Future<VehicleModel> unassignDriver({
    required String vehicleId,
    required String organizationId,
    String? userId,
  }) async {
    final uri = Uri.parse('$baseUrl/vehicles/$vehicleId/unassign-driver').replace(queryParameters: {
      'organization_id': organizationId,
    });

    final headers = <String, String>{
      'Content-Type': 'application/json',
    };
    if (userId != null) headers['X-User-ID'] = userId;

    final response = await http.post(uri, headers: headers);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return VehicleModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to unassign driver');
    }
  }
}
