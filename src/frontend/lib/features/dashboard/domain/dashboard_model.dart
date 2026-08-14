class DashboardSummaryModel {
  final int totalVehicles;
  final int totalDrivers;
  final double monthlyTotalCost;
  final int upcomingMaintenanceCount;
  final int overdueMaintenanceCount;

  DashboardSummaryModel({
    required this.totalVehicles,
    required this.totalDrivers,
    required this.monthlyTotalCost,
    required this.upcomingMaintenanceCount,
    required this.overdueMaintenanceCount,
  });

  factory DashboardSummaryModel.fromJson(Map<String, dynamic> json) {
    return DashboardSummaryModel(
      totalVehicles: (json['total_vehicles'] as num?)?.toInt() ?? 0,
      totalDrivers: (json['total_drivers'] as num?)?.toInt() ?? 0,
      monthlyTotalCost: (json['monthly_total_cost'] as num?)?.toDouble() ?? 0.0,
      upcomingMaintenanceCount: (json['upcoming_maintenance_count'] as num?)?.toInt() ?? 0,
      overdueMaintenanceCount: (json['overdue_maintenance_count'] as num?)?.toInt() ?? 0,
    );
  }
}
