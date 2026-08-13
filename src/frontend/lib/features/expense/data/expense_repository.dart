import 'dart:convert';
import 'package:http/http.dart' as http;
import '../domain/expense_model.dart';

class ExpenseRepository {
  final String baseUrl;

  ExpenseRepository({this.baseUrl = 'http://127.0.0.1:8000/api/v1'});

  Future<ExpenseModel> logExpense({
    required String vehicleId,
    required String category,
    required double amount,
    String currency = 'PKR',
    DateTime? expenseDate,
    String? receiptPhotoUrl,
    String? notes,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/expenses').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final payload = {
      'vehicle_id': vehicleId,
      'category': category.toUpperCase(),
      'amount': amount,
      'currency': currency,
      if (expenseDate != null) 'expense_date': expenseDate.toIso8601String(),
      if (receiptPhotoUrl != null && receiptPhotoUrl.isNotEmpty) 'receipt_photo_url': receiptPhotoUrl,
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
      return ExpenseModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to log expense');
    }
  }

  Future<List<ExpenseModel>> getExpenses({
    String? vehicleId,
    String? category,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (vehicleId != null && vehicleId.isNotEmpty) {
      queryParams['vehicle_id'] = vehicleId;
    }
    if (category != null && category.isNotEmpty) {
      queryParams['category'] = category;
    }
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/expenses').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

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
        return decoded.map((item) => ExpenseModel.fromJson(item as Map<String, dynamic>)).toList();
      } else if (decoded is Map && decoded.containsKey('items')) {
        final List<dynamic> list = decoded['items'];
        return list.map((item) => ExpenseModel.fromJson(item as Map<String, dynamic>)).toList();
      }
      return [];
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch expense logs');
    }
  }

  Future<ExpenseSummaryModel> getExpenseSummary({
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

    final uri = Uri.parse('$baseUrl/expenses/summary').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final response = await http.get(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
    );

    if (response.statusCode == 200) {
      return ExpenseSummaryModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch expense summary metrics');
    }
  }

  Future<ExpenseModel> updateExpense({
    required String expenseId,
    required Map<String, dynamic> data,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/expenses/$expenseId').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final response = await http.patch(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
      body: jsonEncode(data),
    );

    if (response.statusCode == 200) {
      return ExpenseModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to update expense record');
    }
  }

  Future<void> deleteExpense({
    required String expenseId,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/expenses/$expenseId').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final response = await http.delete(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (organizationId != null) 'X-Organization-ID': organizationId,
      },
    );

    if (response.statusCode != 200) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to delete expense record');
    }
  }

  Future<ExpenseModel> quickLogExpense({
    required String vehicleId,
    required String category,
    required double amount,
    String currency = 'PKR',
    String? notes,
    String? organizationId,
  }) async {
    final queryParams = <String, String>{};
    if (organizationId != null && organizationId.isNotEmpty) {
      queryParams['organization_id'] = organizationId;
    }

    final uri = Uri.parse('$baseUrl/expenses/quick').replace(queryParameters: queryParams.isEmpty ? null : queryParams);

    final payload = {
      'vehicle_id': vehicleId,
      'category': category.toUpperCase(),
      'amount': amount,
      'currency': currency,
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
      return ExpenseModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to quick log expense');
    }
  }
}



