class ExpenseModel {
  final String id;
  final String organizationId;
  final String vehicleId;
  final String? fuelLogId;
  final String category;
  final double amount;
  final String currency;
  final DateTime expenseDate;
  final String? receiptPhotoUrl;
  final String? notes;
  final DateTime createdAt;
  final DateTime updatedAt;

  ExpenseModel({
    required this.id,
    required this.organizationId,
    required this.vehicleId,
    this.fuelLogId,
    required this.category,
    required this.amount,
    required this.currency,
    required this.expenseDate,
    this.receiptPhotoUrl,
    this.notes,
    required this.createdAt,
    required this.updatedAt,
  });

  factory ExpenseModel.fromJson(Map<String, dynamic> json) {
    return ExpenseModel(
      id: json['id'] as String,
      organizationId: json['organization_id'] as String,
      vehicleId: json['vehicle_id'] as String,
      fuelLogId: json['fuel_log_id'] as String?,
      category: json['category'] as String? ?? 'OTHER',
      amount: (json['amount'] as num).toDouble(),
      currency: json['currency'] as String? ?? 'PKR',
      expenseDate: DateTime.parse(json['expense_date'] as String),
      receiptPhotoUrl: json['receipt_photo_url'] as String?,
      notes: json['notes'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'organization_id': organizationId,
      'vehicle_id': vehicleId,
      'fuel_log_id': fuelLogId,
      'category': category,
      'amount': amount,
      'currency': currency,
      'expense_date': expenseDate.toIso8601String(),
      'receipt_photo_url': receiptPhotoUrl,
      'notes': notes,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}

class ExpenseSummaryModel {
  final String? vehicleId;
  final double totalExpenseAmount;
  final int totalExpensesCount;
  final Map<String, double> categoryBreakdown;

  ExpenseSummaryModel({
    this.vehicleId,
    required this.totalExpenseAmount,
    required this.totalExpensesCount,
    required this.categoryBreakdown,
  });

  factory ExpenseSummaryModel.fromJson(Map<String, dynamic> json) {
    final map = <String, double>{};
    if (json['category_breakdown'] != null && json['category_breakdown'] is Map) {
      (json['category_breakdown'] as Map).forEach((k, v) {
        map[k.toString()] = (v as num).toDouble();
      });
    }

    return ExpenseSummaryModel(
      vehicleId: json['vehicle_id'] as String?,
      totalExpenseAmount: (json['total_expense_amount'] as num).toDouble(),
      totalExpensesCount: json['total_expenses_count'] as int,
      categoryBreakdown: map,
    );
  }
}

