import 'dart:convert';
import 'package:http/http.dart' as http;
import '../domain/trip_model.dart';

class TripRepository {
  final String baseUrl;

  TripRepository({this.baseUrl = 'http://127.0.0.1:8000/api/v1'});

  Future<TripModel> startTrip({
    required String vehicleId,
    required double startOdometerKm,
    String? originName,
    String tripPurpose = 'BUSINESS',
    String? driverId,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/trips/start').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final payload = {
      'vehicle_id': vehicleId,
      'start_odometer_km': startOdometerKm,
      if (originName != null) 'origin_name': originName,
      'trip_purpose': tripPurpose,
      if (driverId != null) 'driver_id': driverId,
    };

    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
      body: jsonEncode(payload),
    );

    if (response.statusCode == 201) {
      return TripModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to start trip session');
    }
  }

  Future<TripModel> stopTrip({
    required String tripId,
    required double endOdometerKm,
    String? destinationName,
    String? gpsPolylineJson,
    String? notes,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/trips/$tripId/stop').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final payload = {
      'end_odometer_km': endOdometerKm,
      if (destinationName != null) 'destination_name': destinationName,
      if (gpsPolylineJson != null) 'gps_polyline_json': gpsPolylineJson,
      if (notes != null) 'notes': notes,
    };

    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
      body: jsonEncode(payload),
    );

    if (response.statusCode == 200) {
      return TripModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to stop trip session');
    }
  }

  Future<TripModel> logManualTrip({
    required String vehicleId,
    required double startOdometerKm,
    required double endOdometerKm,
    String? originName,
    String? destinationName,
    String tripPurpose = 'BUSINESS',
    String? notes,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/trips').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final payload = {
      'vehicle_id': vehicleId,
      'start_odometer_km': startOdometerKm,
      'end_odometer_km': endOdometerKm,
      if (originName != null) 'origin_name': originName,
      if (destinationName != null) 'destination_name': destinationName,
      'trip_purpose': tripPurpose,
      'is_manual': true,
      if (notes != null) 'notes': notes,
    };

    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
      body: jsonEncode(payload),
    );

    if (response.statusCode == 201) {
      return TripModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to log trip');
    }
  }

  Future<List<TripModel>> getTrips({
    String? vehicleId,
    String? tripPurpose,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (vehicleId != null && vehicleId.isNotEmpty) {
      queryParams['vehicle_id'] = vehicleId;
    }
    if (tripPurpose != null && tripPurpose.isNotEmpty) {
      queryParams['trip_purpose'] = tripPurpose;
    }
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/trips').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

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
        return decoded.map((item) => TripModel.fromJson(item as Map<String, dynamic>)).toList();
      } else if (decoded is Map && decoded.containsKey('items')) {
        final List<dynamic> list = decoded['items'];
        return list.map((item) => TripModel.fromJson(item as Map<String, dynamic>)).toList();
      }
      return [];
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch trip logs');
    }
  }

  Future<TripSummaryModel> getTripSummary({
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

    final uri = Uri.parse('$baseUrl/trips/summary').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final response = await http.get(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
    );

    if (response.statusCode == 200) {
      return TripSummaryModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch trip summary metrics');
    }
  }

  Future<TripModel> updateTrip({
    required String tripId,
    required Map<String, dynamic> data,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/trips/$tripId').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final response = await http.patch(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
      body: jsonEncode(data),
    );

    if (response.statusCode == 200) {
      return TripModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to update trip record');
    }
  }

  Future<void> deleteTrip({
    required String tripId,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/trips/$tripId').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final response = await http.delete(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
    );

    if (response.statusCode != 200) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to delete trip record');
    }
  }

  Future<TripModel> quickLogTrip({
    required String vehicleId,
    required double distanceKm,
    String? originName,
    String? destinationName,
    String tripPurpose = 'BUSINESS',
    String? notes,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/trips/quick').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final payload = {
      'vehicle_id': vehicleId,
      'distance_km': distanceKm,
      if (originName != null && originName.isNotEmpty) 'origin_name': originName,
      if (destinationName != null && destinationName.isNotEmpty) 'destination_name': destinationName,
      'trip_purpose': tripPurpose.toUpperCase(),
      if (notes != null && notes.isNotEmpty) 'notes': notes,
    };

    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
      body: jsonEncode(payload),
    );

    if (response.statusCode == 201) {
      return TripModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to quick log trip');
    }
  }

  Future<MileageSummaryModel> getMileageSummary({
    String? vehicleId,
    DateTime? startDate,
    DateTime? endDate,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (vehicleId != null && vehicleId.isNotEmpty) {
      queryParams['vehicle_id'] = vehicleId;
    }
    if (startDate != null) {
      queryParams['start_date'] = startDate.toIso8601String();
    }
    if (endDate != null) {
      queryParams['end_date'] = endDate.toIso8601String();
    }
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/trips/mileage-summary').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final response = await http.get(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
    );

    if (response.statusCode == 200) {
      return MileageSummaryModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch mileage summary metrics');
    }
  }
}




