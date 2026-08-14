class SyncOperationEnvelopeModel {
  final String opId;
  final String entityType;
  final String action; // CREATE, UPDATE, DELETE
  final Map<String, dynamic> payload;
  final String? baseUpdatedAt;
  final String? clientTimestamp;

  SyncOperationEnvelopeModel({
    required this.opId,
    required this.entityType,
    required this.action,
    required this.payload,
    this.baseUpdatedAt,
    this.clientTimestamp,
  });

  factory SyncOperationEnvelopeModel.fromJson(Map<String, dynamic> json) {
    return SyncOperationEnvelopeModel(
      opId: json['op_id'] as String,
      entityType: json['entity_type'] as String,
      action: json['action'] as String,
      payload: Map<String, dynamic>.from(json['payload'] as Map),
      baseUpdatedAt: json['base_updated_at'] as String?,
      clientTimestamp: json['client_timestamp'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'op_id': opId,
      'entity_type': entityType,
      'action': action,
      'payload': payload,
      if (baseUpdatedAt != null) 'base_updated_at': baseUpdatedAt,
      if (clientTimestamp != null) 'client_timestamp': clientTimestamp,
    };
  }
}

class SyncOperationResultModel {
  final String opId;
  final String status; // SUCCESS, CONFLICT, REJECTED
  final String? entityId;
  final Map<String, dynamic>? serverEntity;
  final String? message;

  SyncOperationResultModel({
    required this.opId,
    required this.status,
    this.entityId,
    this.serverEntity,
    this.message,
  });

  factory SyncOperationResultModel.fromJson(Map<String, dynamic> json) {
    return SyncOperationResultModel(
      opId: json['op_id'] as String,
      status: json['status'] as String,
      entityId: json['entity_id'] as String?,
      serverEntity: json['server_entity'] != null ? Map<String, dynamic>.from(json['server_entity'] as Map) : null,
      message: json['message'] as String?,
    );
  }
}

class SyncBatchResponseModel {
  final int processedCount;
  final List<SyncOperationResultModel> results;

  SyncBatchResponseModel({
    required this.processedCount,
    required this.results,
  });

  factory SyncBatchResponseModel.fromJson(Map<String, dynamic> json) {
    final list = json['results'] as List<dynamic>? ?? [];
    return SyncBatchResponseModel(
      processedCount: json['processed_count'] as int? ?? 0,
      results: list.map((item) => SyncOperationResultModel.fromJson(item as Map<String, dynamic>)).toList(),
    );
  }
}

class DeltaSyncResponseModel {
  final List<Map<String, dynamic>> vehicles;
  final List<Map<String, dynamic>> drivers;
  final List<Map<String, dynamic>> fuelLogs;
  final List<Map<String, dynamic>> maintenanceSchedules;
  final List<Map<String, dynamic>> serviceRecords;
  final List<Map<String, dynamic>> trips;
  final List<Map<String, dynamic>> expenses;
  final Map<String, List<String>> deletedIds;
  final String syncTimestamp;

  DeltaSyncResponseModel({
    required this.vehicles,
    required this.drivers,
    required this.fuelLogs,
    required this.maintenanceSchedules,
    required this.serviceRecords,
    required this.trips,
    required this.expenses,
    required this.deletedIds,
    required this.syncTimestamp,
  });

  factory DeltaSyncResponseModel.fromJson(Map<String, dynamic> json) {
    List<Map<String, dynamic>> parseList(String key) {
      final list = json[key] as List<dynamic>? ?? [];
      return list.map((item) => Map<String, dynamic>.from(item as Map)).toList();
    }

    final deletedMap = <String, List<String>>{};
    if (json['deleted_ids'] != null) {
      (json['deleted_ids'] as Map<String, dynamic>).forEach((k, v) {
        deletedMap[k] = (v as List<dynamic>).map((e) => e.toString()).toList();
      });
    }

    return DeltaSyncResponseModel(
      vehicles: parseList('vehicles'),
      drivers: parseList('drivers'),
      fuelLogs: parseList('fuel_logs'),
      maintenanceSchedules: parseList('maintenance_schedules'),
      serviceRecords: parseList('service_records'),
      trips: parseList('trips'),
      expenses: parseList('expenses'),
      deletedIds: deletedMap,
      syncTimestamp: json['sync_timestamp'] as String? ?? DateTime.now().toIso8601String(),
    );
  }
}
