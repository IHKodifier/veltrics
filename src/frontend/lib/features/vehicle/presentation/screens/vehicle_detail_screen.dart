import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../../fuel/presentation/screens/fuel_history_screen.dart';
import '../../../fuel/presentation/screens/log_fuel_screen.dart';
import '../../../maintenance/presentation/screens/log_maintenance_screen.dart';
import '../../../maintenance/presentation/screens/maintenance_schedule_screen.dart';
import '../../../maintenance/presentation/screens/service_history_screen.dart';
import '../../data/vehicle_repository.dart';
import '../../domain/vehicle_model.dart';
import 'edit_vehicle_screen.dart';

class VehicleDetailScreen extends StatefulWidget {
  final String vehicleId;
  final String organizationId;

  const VehicleDetailScreen({
    super.key,
    required this.vehicleId,
    required this.organizationId,
  });

  @override
  State<VehicleDetailScreen> createState() => _VehicleDetailScreenState();
}

class _VehicleDetailScreenState extends State<VehicleDetailScreen> {
  final VehicleRepository _vehicleRepository = VehicleRepository();

  VehicleDetailModel? _detail;
  bool _isLoading = true;
  bool _isUpdatingStatus = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchVehicleDetail();
  }

  Future<void> _fetchVehicleDetail() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final detail = await _vehicleRepository.getVehicleDetail(
        vehicleId: widget.vehicleId,
        organizationId: widget.organizationId,
      );
      setState(() {
        _detail = detail;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll("Exception: ", "");
        _isLoading = false;
      });
    }
  }

  Future<void> _handleStatusUpdate(String newStatus) async {
    if (_detail == null || _detail!.status == newStatus) return;

    setState(() {
      _isUpdatingStatus = true;
    });

    try {
      await _vehicleRepository.updateVehicleStatus(
        vehicleId: widget.vehicleId,
        organizationId: widget.organizationId,
        status: newStatus,
      );
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text("Vehicle status updated to $newStatus"),
            backgroundColor: VeltricsColors.successLight,
          ),
        );
      }
      await _fetchVehicleDetail();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text("Failed to update status: ${e.toString().replaceAll('Exception: ', '')}"),
            backgroundColor: VeltricsColors.errorLight,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isUpdatingStatus = false;
        });
      }
    }
  }

  Color _getProvinceStripeColor(String province) {
    switch (province.toLowerCase()) {
      case 'sindh':
        return const Color(0xFFB91C1C);
      case 'ict islamabad':
      case 'islamabad':
        return const Color(0xFF1D4ED8);
      case 'balochistan':
        return const Color(0xFFD97706);
      case 'khyber pakhtunkhwa':
      case 'kpk':
        return const Color(0xFF047857);
      case 'punjab':
      default:
        return const Color(0xFF15803D);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Vehicle Details'),
        actions: [
          if (_detail != null)
            IconButton(
              icon: const Icon(Icons.edit_outlined),
              tooltip: "Edit Vehicle Specifications",
              onPressed: () async {
                final updated = await Navigator.push<bool>(
                  context,
                  MaterialPageRoute(
                    builder: (_) => EditVehicleScreen(vehicle: _detail!),
                  ),
                );
                if (updated == true) {
                  _fetchVehicleDetail();
                }
              },
            ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _fetchVehicleDetail,
          ),
        ],
      ),
      body: SafeArea(
        child: _isLoading
            ? const Center(child: CircularProgressIndicator())
            : _errorMessage != null
                ? Center(
                    child: Padding(
                      padding: VeltricsSpacing.pagePadding,
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.error_outline, size: 48, color: VeltricsColors.errorLight),
                          const SizedBox(height: VeltricsSpacing.xs2),
                          Text(
                            "Error Loading Vehicle Details",
                            style: VeltricsTextStyles.titleLg,
                          ),
                          const SizedBox(height: VeltricsSpacing.xs3),
                          Text(
                            _errorMessage!,
                            style: VeltricsTextStyles.bodyMd,
                            textAlign: TextAlign.center,
                          ),
                          const SizedBox(height: VeltricsSpacing.md),
                          ElevatedButton(
                            onPressed: _fetchVehicleDetail,
                            child: const Text("Retry"),
                          ),
                        ],
                      ),
                    ),
                  )
                : _detail == null
                    ? const Center(child: Text("Vehicle not found."))
                    : RefreshIndicator(
                        onRefresh: _fetchVehicleDetail,
                        child: SingleChildScrollView(
                          padding: VeltricsSpacing.pagePadding,
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              // 1. Vehicle Title & Status Card
                              _buildHeaderCard(theme, isDark),
                              const SizedBox(height: VeltricsSpacing.sm),

                              // 2. Pakistani License Plate Card
                              _buildPlateCard(theme, isDark),
                              const SizedBox(height: VeltricsSpacing.sm),

                              // 3. Key Metrics & Specs Grid
                              _buildSpecsGrid(theme, isDark),
                              const SizedBox(height: VeltricsSpacing.sm),

                              // 4. Activity & Financial Summary Card
                              _buildSummaryStatsCard(theme, isDark),
                              const SizedBox(height: VeltricsSpacing.sm),

                              // 5. Driver Assignment Card
                              _buildDriverCard(theme, isDark),
                              const SizedBox(height: VeltricsSpacing.md),

                              // 6. Quick Status Update Action Bar
                              Text("Update Status", style: VeltricsTextStyles.titleLg),
                              const SizedBox(height: VeltricsSpacing.xs2),
                              _buildStatusActionBar(theme, isDark),
                              const SizedBox(height: VeltricsSpacing.md),

                              // 7. Quick Shortcuts Section
                              Text("Quick Actions", style: VeltricsTextStyles.titleLg),
                              const SizedBox(height: VeltricsSpacing.xs2),
                              _buildQuickShortcuts(theme, isDark),
                              const SizedBox(height: VeltricsSpacing.lg),
                            ],
                          ),
                        ),
                      ),
      ),
    );
  }

  Widget _buildHeaderCard(ThemeData theme, bool isDark) {
    final detail = _detail!;
    final isMaintenance = detail.status == "MAINTENANCE";
    final isInactive = detail.status == "INACTIVE";

    return Card(
      child: Padding(
        padding: VeltricsSpacing.cardPaddingMobile,
        child: Column(
          children: [
            Row(
              children: [
                Container(
                  width: 60,
                  height: 60,
                  decoration: BoxDecoration(
                    color: theme.colorScheme.primary.withValues(alpha: 0.1),
                    borderRadius: VeltricsRadius.smAll,
                  ),
                  child: Icon(
                    detail.fuelType == "EV" ? Icons.electric_car : Icons.directions_car,
                    size: 36,
                    color: theme.colorScheme.primary,
                  ),
                ),
                const SizedBox(width: VeltricsSpacing.sm),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        "${detail.make} ${detail.model}",
                        style: VeltricsTextStyles.titleLg,
                      ),
                      const SizedBox(height: 2),
                      Text(
                        "Year: ${detail.year} • Fuel: ${detail.fuelType}",
                        style: VeltricsTextStyles.bodyMd,
                      ),
                    ],
                  ),
                ),
                if (isMaintenance)
                  VeltricsStatusPill.warning(text: "MAINTENANCE", isDark: isDark)
                else if (isInactive)
                  VeltricsStatusPill.error(text: "INACTIVE", isDark: isDark)
                else
                  VeltricsStatusPill.healthy(text: "ACTIVE", isDark: isDark),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPlateCard(ThemeData theme, bool isDark) {
    final detail = _detail!;
    final stripeColor = _getProvinceStripeColor(detail.registrationProvince);

    return Card(
      color: isDark ? VeltricsColors.neutralD800 : Colors.grey.shade50,
      child: Padding(
        padding: VeltricsSpacing.cardPaddingMobile,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text("LICENSE PLATE", style: VeltricsTextStyles.labelSm),
                const SizedBox(height: 4),
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                      decoration: BoxDecoration(
                        color: stripeColor,
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Text(
                        detail.registrationProvince.toUpperCase(),
                        style: const TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 11,
                          letterSpacing: 1.2,
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Text(
                      detail.licensePlate,
                      style: const TextStyle(
                        fontFamily: 'monospace',
                        fontWeight: FontWeight.w900,
                        fontSize: 22,
                        letterSpacing: 1.5,
                      ),
                    ),
                  ],
                ),
              ],
            ),
            const Icon(Icons.verified_outlined, size: 28, color: VeltricsColors.successLight),
          ],
        ),
      ),
    );
  }

  Widget _buildSpecsGrid(ThemeData theme, bool isDark) {
    final detail = _detail!;

    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      childAspectRatio: 2.2,
      crossAxisSpacing: 12,
      mainAxisSpacing: 12,
      children: [
        _buildMetricItem(
          icon: Icons.speed,
          label: "Current Odometer",
          value: "${detail.currentOdometerKm.toStringAsFixed(0)} km",
          theme: theme,
        ),
        _buildMetricItem(
          icon: Icons.history,
          label: "Initial Odometer",
          value: "${detail.initialOdometerKm.toStringAsFixed(0)} km",
          theme: theme,
        ),
        _buildMetricItem(
          icon: detail.fuelType == "EV" ? Icons.electric_bolt : Icons.local_gas_station,
          label: "Fuel Type",
          value: detail.fuelType,
          theme: theme,
        ),
        _buildMetricItem(
          icon: Icons.fingerprint,
          label: "VIN / Chassis",
          value: detail.vin != null && detail.vin!.isNotEmpty ? detail.vin! : "Not Recorded",
          theme: theme,
        ),
      ],
    );
  }

  Widget _buildMetricItem({
    required IconData icon,
    required String label,
    required String value,
    required ThemeData theme,
  }) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: theme.cardTheme.color,
        borderRadius: VeltricsRadius.smAll,
        border: Border.all(
          color: theme.brightness == Brightness.dark ? VeltricsColors.neutralD700 : VeltricsColors.neutral300,
        ),
      ),
      child: Row(
        children: [
          Icon(icon, size: 24, color: theme.colorScheme.primary),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(label, style: VeltricsTextStyles.labelSm, overflow: TextOverflow.ellipsis),
                const SizedBox(height: 2),
                Text(value, style: VeltricsTextStyles.titleSm, overflow: TextOverflow.ellipsis),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSummaryStatsCard(ThemeData theme, bool isDark) {
    final detail = _detail!;

    return Card(
      child: Padding(
        padding: VeltricsSpacing.cardPaddingMobile,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            _buildStatColumn(
              label: "Schedules",
              value: detail.activeSchedulesCount.toString(),
              icon: Icons.calendar_today,
              color: VeltricsColors.infoLight,
            ),
            Container(width: 1, height: 40, color: isDark ? VeltricsColors.neutralD700 : VeltricsColors.neutral300),
            _buildStatColumn(
              label: "Services",
              value: detail.totalServiceRecordsCount.toString(),
              icon: Icons.build,
              color: VeltricsColors.successLight,
            ),
            Container(width: 1, height: 40, color: isDark ? VeltricsColors.neutralD700 : VeltricsColors.neutral300),
            _buildStatColumn(
              label: "Total Expenses",
              value: "Rs. ${detail.totalExpensesCost.toStringAsFixed(0)}",
              icon: Icons.payments,
              color: VeltricsColors.warningLight,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatColumn({
    required String label,
    required String value,
    required IconData icon,
    required Color color,
  }) {
    return Column(
      children: [
        Icon(icon, size: 20, color: color),
        const SizedBox(height: 4),
        Text(value, style: VeltricsTextStyles.titleLg),
        Text(label, style: VeltricsTextStyles.labelSm),
      ],
    );
  }

  Widget _buildDriverCard(ThemeData theme, bool isDark) {
    final detail = _detail!;
    final hasDriver = detail.assignedDriverName != null && detail.assignedDriverName!.isNotEmpty;

    return Card(
      child: Padding(
        padding: VeltricsSpacing.cardPaddingMobile,
        child: Row(
          children: [
            CircleAvatar(
              backgroundColor: hasDriver ? VeltricsColors.infoLight : VeltricsColors.neutral500,
              child: Icon(hasDriver ? Icons.person : Icons.person_off, color: Colors.white),
            ),
            const SizedBox(width: VeltricsSpacing.sm),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text("Assigned Driver", style: VeltricsTextStyles.labelSm),
                  const SizedBox(height: 2),
                  Text(
                    hasDriver ? detail.assignedDriverName! : "No Driver Assigned",
                    style: VeltricsTextStyles.titleSm,
                  ),
                  if (hasDriver && detail.assignedDriverPhone != null)
                    Text(detail.assignedDriverPhone!, style: VeltricsTextStyles.bodyMd),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusActionBar(ThemeData theme, bool isDark) {
    final currentStatus = _detail?.status ?? "ACTIVE";

    return Row(
      children: [
        Expanded(
          child: ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: currentStatus == "ACTIVE" ? VeltricsColors.successLight : null,
              foregroundColor: currentStatus == "ACTIVE" ? Colors.white : null,
            ),
            onPressed: _isUpdatingStatus ? null : () => _handleStatusUpdate("ACTIVE"),
            icon: const Icon(Icons.check_circle_outline, size: 18),
            label: const Text("Active"),
          ),
        ),
        const SizedBox(width: 8),
        Expanded(
          child: ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: currentStatus == "MAINTENANCE" ? VeltricsColors.warningLight : null,
              foregroundColor: currentStatus == "MAINTENANCE" ? Colors.white : null,
            ),
            onPressed: _isUpdatingStatus ? null : () => _handleStatusUpdate("MAINTENANCE"),
            icon: const Icon(Icons.build_outlined, size: 18),
            label: const Text("Maintenance"),
          ),
        ),
        const SizedBox(width: 8),
        Expanded(
          child: ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: currentStatus == "INACTIVE" ? VeltricsColors.errorLight : null,
              foregroundColor: currentStatus == "INACTIVE" ? Colors.white : null,
            ),
            onPressed: _isUpdatingStatus ? null : () => _handleStatusUpdate("INACTIVE"),
            icon: const Icon(Icons.pause_circle_outline, size: 18),
            label: const Text("Inactive"),
          ),
        ),
      ],
    );
  }

  Widget _buildQuickShortcuts(ThemeData theme, bool isDark) {
    final detail = _detail;
    return Column(
      children: [
        ListTile(
          shape: RoundedRectangleBorder(borderRadius: VeltricsRadius.smAll),
          tileColor: theme.cardTheme.color,
          leading: Icon(Icons.local_gas_station, color: theme.colorScheme.primary),
          title: const Text("Fuel Log History"),
          subtitle: const Text("View fuel fill-ups, efficiency & leak alerts"),
          trailing: const Icon(Icons.chevron_right),
          onTap: detail == null
              ? null
              : () async {
                  await Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => FuelHistoryScreen(
                        vehicleId: widget.vehicleId,
                        organizationId: widget.organizationId,
                        vehicleTitle: "${detail.year} ${detail.make} ${detail.model}",
                        currentOdometer: detail.currentOdometerKm,
                      ),
                    ),
                  );
                  _fetchVehicleDetail();
                },
        ),
        const SizedBox(height: 8),
        ListTile(
          shape: RoundedRectangleBorder(borderRadius: VeltricsRadius.smAll),
          tileColor: theme.cardTheme.color,
          leading: const Icon(Icons.schedule, color: VeltricsColors.infoLight),
          title: const Text("Maintenance Schedule"),
          subtitle: const Text("View pre-populated service reminders"),
          trailing: const Icon(Icons.chevron_right),
          onTap: detail == null
              ? null
              : () async {
                  await Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => MaintenanceScheduleScreen(
                        vehicleId: widget.vehicleId,
                        organizationId: widget.organizationId,
                        currentOdometer: detail.currentOdometerKm,
                      ),
                    ),
                  );
                  _fetchVehicleDetail();
                },
        ),
        const SizedBox(height: 8),
        ListTile(
          shape: RoundedRectangleBorder(borderRadius: VeltricsRadius.smAll),
          tileColor: theme.cardTheme.color,
          leading: const Icon(Icons.add_task, color: VeltricsColors.successLight),
          title: const Text("Log Service Record"),
          subtitle: const Text("Record oil change, repair, or inspection"),
          trailing: const Icon(Icons.chevron_right),
          onTap: detail == null
              ? null
              : () async {
                  final logged = await Navigator.push<bool>(
                    context,
                    MaterialPageRoute(
                      builder: (_) => LogMaintenanceScreen(
                        vehicleId: widget.vehicleId,
                        organizationId: widget.organizationId,
                        currentOdometer: detail.currentOdometerKm,
                      ),
                    ),
                  );
                  if (logged == true) {
                    _fetchVehicleDetail();
                  }
                },
        ),
        const SizedBox(height: 8),
        ListTile(
          shape: RoundedRectangleBorder(borderRadius: VeltricsRadius.smAll),
          tileColor: theme.cardTheme.color,
          leading: const Icon(Icons.history, color: VeltricsColors.warningLight),
          title: const Text("Service History"),
          subtitle: const Text("View past maintenance & repair records"),
          trailing: const Icon(Icons.chevron_right),
          onTap: detail == null
              ? null
              : () async {
                  await Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => ServiceHistoryScreen(
                        vehicleId: widget.vehicleId,
                        organizationId: widget.organizationId,
                        vehicleTitle: "${detail.year} ${detail.make} ${detail.model}",
                        currentOdometer: detail.currentOdometerKm,
                      ),
                    ),
                  );
                  _fetchVehicleDetail();
                },
        ),
      ],
    );
  }

}
