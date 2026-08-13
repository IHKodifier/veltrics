import 'dart:convert';
import 'package:http/http.dart' as http;
import '../domain/dashboard_model.dart';
import '../domain/cost_breakdown_model.dart';

class DashboardRepository {
  final String baseUrl;

  DashboardRepository({this.baseUrl = 'http://localhost:8000/api/v1'});

  Future<DashboardSummaryModel> getSummary({required String organizationId}) async {
    final uri = Uri.parse('$baseUrl/dashboard/summary');
    final response = await http.get(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-Organization-ID': organizationId,
      },
    );

    if (response.statusCode == 200) {
      final Map<String, dynamic> data = jsonDecode(response.body);
      return DashboardSummaryModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch dashboard summary');
    }
  }

  Future<CostBreakdownModel> getCostBreakdown({
    required String organizationId,
    String? vehicleId,
    String timeframe = '6m',
  }) async {
    final queryParams = <String, String>{
      'timeframe': timeframe,
      if (vehicleId != null && vehicleId.isNotEmpty) 'vehicle_id': vehicleId,
    };

    final uri = Uri.parse('$baseUrl/dashboard/cost-breakdown').replace(queryParameters: queryParams);
    final response = await http.get(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-Organization-ID': organizationId,
      },
    );

    if (response.statusCode == 200) {
      final Map<String, dynamic> data = jsonDecode(response.body);
      return CostBreakdownModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch cost breakdown');
    }
  }
}

