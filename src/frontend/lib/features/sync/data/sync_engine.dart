import 'dart:convert';
import 'package:http/http.dart' as http;
import '../domain/sync_model.dart';

class SyncEngine {
  final String baseUrl;
  final List<SyncOperationEnvelopeModel> _pendingQueue = [];
  DateTime? lastSyncTimestamp;

  SyncEngine({this.baseUrl = 'http://localhost:8000/api/v1'});

  List<SyncOperationEnvelopeModel> get pendingQueue => List.unmodifiable(_pendingQueue);

  void enqueueOperation({
    required String opId,
    required String entityType,
    required String action,
    required Map<String, dynamic> payload,
    String? baseUpdatedAt,
  }) {
    final envelope = SyncOperationEnvelopeModel(
      opId: opId,
      entityType: entityType,
      action: action,
      payload: payload,
      baseUpdatedAt: baseUpdatedAt,
      clientTimestamp: DateTime.now().toIso8601String(),
    );
    _pendingQueue.add(envelope);
  }

  Future<SyncBatchResponseModel> performBatchSync({
    required String organizationId,
    String? accessToken,
  }) async {
    if (_pendingQueue.isEmpty) {
      return SyncBatchResponseModel(processedCount: 0, results: []);
    }

    final headers = <String, String>{
      'Content-Type': 'application/json',
    };
    if (accessToken != null) {
      headers['Authorization'] = 'Bearer $accessToken';
    }

    final requestBody = jsonEncode({
      'organization_id': organizationId,
      'operations': _pendingQueue.map((op) => op.toJson()).toList(),
    });

    final response = await http.post(
      Uri.parse('$baseUrl/sync/batch'),
      headers: headers,
      body: requestBody,
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      final batchResp = SyncBatchResponseModel.fromJson(data);

      // Remove successful envelopes from queue
      final successfulOpIds = batchResp.results
          .where((r) => r.status == 'SUCCESS')
          .map((r) => r.opId)
          .toSet();

      _pendingQueue.removeWhere((op) => successfulOpIds.contains(op.opId));
      lastSyncTimestamp = DateTime.now();

      return batchResp;
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Batch sync failed');
    }
  }

  Future<DeltaSyncResponseModel> fetchDeltaSync({
    required String organizationId,
    String? since,
  }) async {
    final queryParams = <String, String>{
      'organization_id': organizationId,
    };
    if (since != null) {
      queryParams['since'] = since;
    }

    final uri = Uri.parse('$baseUrl/sync/delta').replace(queryParameters: queryParams);
    final response = await http.get(uri);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      lastSyncTimestamp = DateTime.now();
      return DeltaSyncResponseModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Delta sync failed');
    }
  }

  Map<String, dynamic> getQueueHealth() {
    return {
      'pending_count': _pendingQueue.length,
      'last_sync': lastSyncTimestamp?.toIso8601String(),
    };
  }
}
