class CostBreakdownItemModel {
  final String period;
  final double fuelCost;
  final double maintenanceCost;
  final double otherExpenseCost;
  final double totalCost;

  CostBreakdownItemModel({
    required this.period,
    required this.fuelCost,
    required this.maintenanceCost,
    required this.otherExpenseCost,
    required this.totalCost,
  });

  factory CostBreakdownItemModel.fromJson(Map<String, dynamic> json) {
    return CostBreakdownItemModel(
      period: json['period'] as String,
      fuelCost: (json['fuel_cost'] as num).toDouble(),
      maintenanceCost: (json['maintenance_cost'] as num).toDouble(),
      otherExpenseCost: (json['other_expense_cost'] as num).toDouble(),
      totalCost: (json['total_cost'] as num).toDouble(),
    );
  }
}

class CostBreakdownModel {
  final String timeframe;
  final String? vehicleId;
  final double totalFuelCost;
  final double totalMaintenanceCost;
  final double totalOtherExpenseCost;
  final double grandTotalCost;
  final List<CostBreakdownItemModel> items;

  CostBreakdownModel({
    required this.timeframe,
    this.vehicleId,
    required this.totalFuelCost,
    required this.totalMaintenanceCost,
    required this.totalOtherExpenseCost,
    required this.grandTotalCost,
    required this.items,
  });

  factory CostBreakdownModel.fromJson(Map<String, dynamic> json) {
    final list = json['items'] as List? ?? [];
    return CostBreakdownModel(
      timeframe: json['timeframe'] as String,
      vehicleId: json['vehicle_id'] as String?,
      totalFuelCost: (json['total_fuel_cost'] as num).toDouble(),
      totalMaintenanceCost: (json['total_maintenance_cost'] as num).toDouble(),
      totalOtherExpenseCost: (json['total_other_expense_cost'] as num).toDouble(),
      grandTotalCost: (json['grand_total_cost'] as num).toDouble(),
      items: list.map((i) => CostBreakdownItemModel.fromJson(i as Map<String, dynamic>)).toList(),
    );
  }
}
