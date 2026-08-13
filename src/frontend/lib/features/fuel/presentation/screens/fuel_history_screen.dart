import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/fuel_repository.dart';
import '../../domain/fuel_log_model.dart';
import 'log_fuel_screen.dart';

class FuelHistoryScreen extends StatefulWidget {
  final String vehicleId;
  final String organizationId;
  final String vehicleTitle;
  final double currentOdometer;

  const FuelHistoryScreen({
    super.key,
    required this.vehicleId,
    required this.organizationId,
    this.vehicleTitle = 'Vehicle Fuel History',
    this.currentOdometer = 0.0,
  });

  @override
  State<FuelHistoryScreen> createState() => _FuelHistoryScreenState();
}

class _FuelHistoryScreenState extends State<FuelHistoryScreen> {
  final FuelRepository _repository = FuelRepository();

  List<FuelLogModel> _fuelLogs = [];
  FuelTrendsModel? _trends;
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchFuelHistory();
  }

  Future<void> _fetchFuelHistory() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final logs = await _repository.getFuelLogs(
        vehicleId: widget.vehicleId,
        organizationId: widget.organizationId,
      );
      FuelTrendsModel? trends;
      try {
        trends = await _repository.getFuelTrends(
          vehicleId: widget.vehicleId,
          organizationId: widget.organizationId,
        );
      } catch (_) {}

      setState(() {
        _fuelLogs = logs;
        _trends = trends;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll('Exception: ', '');
        _isLoading = false;
      });
    }
  }

  double _calculateAverageEfficiency() {
    if (_trends != null && _trends!.vehicleAvgEfficiencyKpl != null && _trends!.vehicleAvgEfficiencyKpl! > 0) {
      return _trends!.vehicleAvgEfficiencyKpl!;
    }
    final validEfficiencies = _fuelLogs
        .where((log) => log.isFullTank && log.calculatedEfficiencyKpl != null)
        .map((log) => log.calculatedEfficiencyKpl!)
        .toList();
    if (validEfficiencies.isEmpty) return 0.0;
    return validEfficiencies.reduce((a, b) => a + b) / validEfficiencies.length;
  }

  double _calculateTotalCost() {
    if (_trends != null && _trends!.totalCost > 0) {
      return _trends!.totalCost;
    }
    if (_fuelLogs.isEmpty) return 0.0;
    return _fuelLogs.fold(0.0, (sum, item) => sum + item.totalCost);
  }

  double _calculateTotalLiters() {
    if (_trends != null && _trends!.totalLiters > 0) {
      return _trends!.totalLiters;
    }
    if (_fuelLogs.isEmpty) return 0.0;
    return _fuelLogs.fold(0.0, (sum, item) => sum + item.quantityLiters);
  }

  String _formatDate(DateTime dt) {
    final months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    final hour = dt.hour.toString().padLeft(2, '0');
    final min = dt.minute.toString().padLeft(2, '0');
    return '${dt.day} ${months[dt.month - 1]} ${dt.year} • $hour:$min';
  }

  Future<void> _confirmDeleteLog(FuelLogModel log) async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Fuel Fill-Up Log'),
        content: Text(
          'Are you sure you want to delete this fill-up entry (${log.odometerKm.toStringAsFixed(0)} km • ${log.quantityLiters.toStringAsFixed(1)} L)? This will recalculate the fuel efficiency chain.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: VeltricsColors.errorLight),
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Delete'),
          ),
        ],
      ),
    );

    if (confirm == true) {
      try {
        await _repository.deleteFuelLog(
          fuelLogId: log.id,
          organizationId: widget.organizationId,
        );
        if (mounted) {
          Navigator.pop(context); // Close detail dialog
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Fuel log entry deleted successfully')),
          );
          _fetchFuelHistory();
        }
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Failed to delete log: $e')),
          );
        }
      }
    }
  }

  void _showLogDetailDialog(FuelLogModel log, ThemeData theme, bool isDark) {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(borderRadius: VeltricsRadius.mdAll),
          title: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Icon(Icons.local_gas_station, color: theme.colorScheme.primary),
                  const SizedBox(width: 8),
                  const Text('Fuel Fill-Up Detail', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                ],
              ),
            ],
          ),
          content: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                _buildDetailRow('Fill-Up Date:', _formatDate(log.logDate)),
                _buildDetailRow('Odometer:', '${log.odometerKm.toStringAsFixed(0)} km'),
                _buildDetailRow('Fuel Quantity:', '${log.quantityLiters.toStringAsFixed(1)} L (${log.fuelType})'),
                _buildDetailRow('Rate:', 'Rs. ${log.pricePerLiter.toStringAsFixed(1)} / L'),
                _buildDetailRow('Total Cost:', 'Rs. ${log.totalCost.toStringAsFixed(0)} ${log.currency}'),
                _buildDetailRow('Tank Fill Type:', log.isFullTank ? 'Full Tank' : 'Partial Fill'),
                if (log.calculatedEfficiencyKpl != null)
                  _buildDetailRow('Calculated Efficiency:', '${log.calculatedEfficiencyKpl!.toStringAsFixed(1)} km/L'),
                if (log.distanceKm != null)
                  _buildDetailRow('Distance Traveled:', '+${log.distanceKm!.toStringAsFixed(1)} km'),
                if (log.stationName != null && log.stationName!.isNotEmpty)
                  _buildDetailRow('Station Name:', log.stationName!),
                if (log.isLeakAlert) ...[
                  const SizedBox(height: 8),
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: VeltricsColors.errorLight.withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: const Row(
                      children: [
                        Icon(Icons.warning_amber, color: VeltricsColors.errorLight, size: 16),
                        SizedBox(width: 6),
                        Expanded(
                          child: Text(
                            'Fuel Leak Alert: Efficiency >30% below vehicle baseline.',
                            style: TextStyle(fontSize: 11, color: VeltricsColors.errorLight, fontWeight: FontWeight.bold),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
                if (log.receiptPhotoUrl != null && log.receiptPhotoUrl!.isNotEmpty) ...[
                  const SizedBox(height: 12),
                  const Text('Receipt Image Attachment:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                  const SizedBox(height: 6),
                  Container(
                    width: double.infinity,
                    height: 160,
                    decoration: BoxDecoration(
                      color: isDark ? VeltricsColors.neutralD800 : Colors.grey.shade200,
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.grey.withValues(alpha: 0.3)),
                    ),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(8),
                      child: Image.network(
                        log.receiptPhotoUrl!,
                        fit: BoxFit.cover,
                        errorBuilder: (context, error, stackTrace) => const Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.receipt_long, size: 36, color: Colors.grey),
                              SizedBox(height: 4),
                              Text('Receipt attachment present', style: TextStyle(fontSize: 11, color: Colors.grey)),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ],
            ),
          ),
          actions: [
            TextButton.icon(
              icon: const Icon(Icons.delete_outline, color: VeltricsColors.errorLight, size: 18),
              label: const Text('Delete', style: TextStyle(color: VeltricsColors.errorLight)),
              onPressed: () => _confirmDeleteLog(log),
            ),
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Close'),
            ),
          ],
        );
      },
    );
  }

  Widget _buildDetailRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 12, color: Colors.grey)),
          Text(value, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    final avgEfficiency = _calculateAverageEfficiency();
    final totalCost = _calculateTotalCost();
    final totalLiters = _calculateTotalLiters();
    final leakAlertCount = _fuelLogs.where((l) => l.isLeakAlert).length;
    final fleetAvg = _trends?.fleetAvgEfficiencyKpl ?? 0.0;

    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Fuel Log History', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            Text(widget.vehicleTitle, style: const TextStyle(fontSize: 12, color: Colors.white70)),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Refresh History',
            onPressed: _fetchFuelHistory,
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
          final result = await Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => LogFuelScreen(
                vehicleId: widget.vehicleId,
                organizationId: widget.organizationId,
                currentOdometer: widget.currentOdometer,
              ),
            ),
          );
          if (result != null) {
            _fetchFuelHistory();
          }
        },
        icon: const Icon(Icons.add),
        label: const Text('Log Fuel Entry'),
        backgroundColor: theme.colorScheme.primary,
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
                          Text('Failed to Load Fuel Log History', style: VeltricsTextStyles.titleLg),
                          const SizedBox(height: VeltricsSpacing.xs3),
                          Text(_errorMessage!, style: VeltricsTextStyles.bodyMd, textAlign: TextAlign.center),
                          const SizedBox(height: VeltricsSpacing.md),
                          ElevatedButton(
                            onPressed: _fetchFuelHistory,
                            child: const Text('Retry'),
                          ),
                        ],
                      ),
                    ),
                  )
                : RefreshIndicator(
                    onRefresh: _fetchFuelHistory,
                    child: _fuelLogs.isEmpty
                        ? ListView(
                            padding: VeltricsSpacing.pagePadding,
                            children: [
                              const SizedBox(height: 60),
                              Center(
                                child: Column(
                                  children: [
                                    Container(
                                      width: 80,
                                      height: 80,
                                      decoration: BoxDecoration(
                                        color: theme.colorScheme.primary.withValues(alpha: 0.1),
                                        shape: BoxShape.circle,
                                      ),
                                      child: Icon(Icons.local_gas_station, size: 40, color: theme.colorScheme.primary),
                                    ),
                                    const SizedBox(height: 16),
                                    Text('No Fuel Entries Yet', style: VeltricsTextStyles.titleLg),
                                    const SizedBox(height: 8),
                                    Text(
                                      'Log fuel fill-ups to automatically calculate vehicle fuel efficiency (km/L) and track costs.',
                                      style: VeltricsTextStyles.bodyMd,
                                      textAlign: TextAlign.center,
                                    ),
                                    const SizedBox(height: 24),
                                    ElevatedButton.icon(
                                      onPressed: () async {
                                        final result = await Navigator.push(
                                          context,
                                          MaterialPageRoute(
                                            builder: (_) => LogFuelScreen(
                                              vehicleId: widget.vehicleId,
                                              organizationId: widget.organizationId,
                                              currentOdometer: widget.currentOdometer,
                                            ),
                                          ),
                                        );
                                        if (result != null) _fetchFuelHistory();
                                      },
                                      icon: const Icon(Icons.local_gas_station),
                                      label: const Text('Log First Fill-Up'),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          )
                        : ListView(
                            padding: VeltricsSpacing.pagePadding,
                            children: [
                              // 1. Ticket identifier caption
                              Text('SCR-FUEL-001 • Fuel Log History & Efficiency Trends', style: VeltricsTextStyles.labelSm),
                              const SizedBox(height: VeltricsSpacing.xs2),

                              // 2. Fuel Anomaly Banner if alerts exist
                              if (leakAlertCount > 0) ...[
                                Container(
                                  padding: const EdgeInsets.all(12),
                                  decoration: BoxDecoration(
                                    color: VeltricsColors.errorLight.withValues(alpha: 0.15),
                                    borderRadius: VeltricsRadius.smAll,
                                    border: Border.all(color: VeltricsColors.errorLight.withValues(alpha: 0.5)),
                                  ),
                                  child: Row(
                                    children: [
                                      const Icon(Icons.warning_amber_rounded, color: VeltricsColors.errorLight, size: 28),
                                      const SizedBox(width: 12),
                                      Expanded(
                                        child: Column(
                                          crossAxisAlignment: CrossAxisAlignment.start,
                                          children: [
                                            Text(
                                              'Potential Fuel Anomaly / Leak Detected',
                                              style: VeltricsTextStyles.titleSm.copyWith(color: VeltricsColors.errorLight, fontWeight: FontWeight.bold),
                                            ),
                                            const SizedBox(height: 2),
                                            Text(
                                              '$leakAlertCount fuel fill-up record(s) flagged with efficiency >30% below vehicle baseline average.',
                                              style: VeltricsTextStyles.bodySm,
                                            ),
                                          ],
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                                const SizedBox(height: VeltricsSpacing.sm),
                              ],

                              // 3. Overall Fuel Efficiency Metrics Summary Card
                              _buildSummaryMetricsCard(theme, isDark, avgEfficiency, totalCost, totalLiters, fleetAvg),
                              const SizedBox(height: VeltricsSpacing.sm),

                              // 4. Monthly Spend & Efficiency Breakdown Card (UC-048)
                              if (_trends != null && _trends!.monthlyTrends.isNotEmpty) ...[
                                _buildMonthlyTrendsCard(theme, isDark),
                                const SizedBox(height: VeltricsSpacing.md),
                              ],

                              Text('Fill-Up Log Timeline (${_fuelLogs.length})', style: VeltricsTextStyles.titleLg),
                              const SizedBox(height: VeltricsSpacing.xs2),

                              // 5. Fuel Log Cards List
                              ..._fuelLogs.map((log) => InkWell(
                                    onTap: () => _showLogDetailDialog(log, theme, isDark),
                                    child: _buildFuelLogCard(log, theme, isDark),
                                  )),
                              const SizedBox(height: 80),
                            ],
                          ),
                  ),
      ),
    );
  }

  Widget _buildSummaryMetricsCard(
    ThemeData theme,
    bool isDark,
    double avgEfficiency,
    double totalCost,
    double totalLiters,
    double fleetAvg,
  ) {
    final hasFleetBenchmark = fleetAvg > 0;
    final isBetterThanFleet = hasFleetBenchmark && avgEfficiency >= fleetAvg;
    final diffPct = hasFleetBenchmark && fleetAvg > 0
        ? (((avgEfficiency - fleetAvg) / fleetAvg) * 100).abs().toStringAsFixed(1)
        : '0.0';

    return Card(
      child: Padding(
        padding: VeltricsSpacing.cardPaddingMobile,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('EFFICIENCY & FLEET BENCHMARK', style: VeltricsTextStyles.labelSm),
                Icon(Icons.analytics_outlined, color: theme.colorScheme.primary, size: 20),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: _buildMetricTile(
                    label: 'Avg. Efficiency',
                    value: avgEfficiency > 0 ? '${avgEfficiency.toStringAsFixed(1)} km/L' : 'N/A',
                    icon: Icons.speed,
                    color: avgEfficiency > 10.0 ? VeltricsColors.successLight : VeltricsColors.infoLight,
                    theme: theme,
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: _buildMetricTile(
                    label: 'Total Liters',
                    value: '${totalLiters.toStringAsFixed(1)} L',
                    icon: Icons.local_gas_station,
                    color: VeltricsColors.warningLight,
                    theme: theme,
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: _buildMetricTile(
                    label: 'Total Spent',
                    value: 'Rs. ${totalCost.toStringAsFixed(0)}',
                    icon: Icons.payments,
                    color: VeltricsColors.infoLight,
                    theme: theme,
                  ),
                ),
              ],
            ),
            if (hasFleetBenchmark) ...[
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                decoration: BoxDecoration(
                  color: isBetterThanFleet
                      ? VeltricsColors.successLight.withValues(alpha: 0.12)
                      : VeltricsColors.warningLight.withValues(alpha: 0.12),
                  borderRadius: VeltricsRadius.smAll,
                  border: Border.all(
                    color: isBetterThanFleet
                        ? VeltricsColors.successLight.withValues(alpha: 0.3)
                        : VeltricsColors.warningLight.withValues(alpha: 0.3),
                  ),
                ),
                child: Row(
                  children: [
                    Icon(
                      isBetterThanFleet ? Icons.trending_up : Icons.trending_down,
                      size: 18,
                      color: isBetterThanFleet ? VeltricsColors.successLight : VeltricsColors.warningLight,
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        'Fleet Aggregate Avg: ${fleetAvg.toStringAsFixed(1)} km/L (${isBetterThanFleet ? '+' : '-'}$diffPct% vs fleet)',
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: isBetterThanFleet ? VeltricsColors.successLight : VeltricsColors.warningLight,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildMonthlyTrendsCard(ThemeData theme, bool isDark) {
    final trends = _trends!.monthlyTrends;
    final maxCost = trends.fold(0.0, (max, item) => item.totalCost > max ? item.totalCost : max);

    return Card(
      child: Padding(
        padding: VeltricsSpacing.cardPaddingMobile,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('MONTHLY SPEND & EFFICIENCY TRENDS', style: VeltricsTextStyles.labelSm),
                const Icon(Icons.bar_chart, color: VeltricsColors.infoLight, size: 20),
              ],
            ),
            const SizedBox(height: 12),
            ...trends.map((m) {
              final pct = maxCost > 0 ? (m.totalCost / maxCost) : 0.0;
              return Padding(
                padding: const EdgeInsets.only(bottom: 8.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(m.month, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                        Text(
                          'Rs. ${m.totalCost.toStringAsFixed(0)} • ${m.totalLiters.toStringAsFixed(1)} L${m.avgEfficiencyKpl != null ? ' (${m.avgEfficiencyKpl!.toStringAsFixed(1)} km/L)' : ''}',
                          style: const TextStyle(fontSize: 11, color: Colors.grey),
                        ),
                      ],
                    ),
                    const SizedBox(height: 4),
                    ClipRRect(
                      borderRadius: BorderRadius.circular(4),
                      child: LinearProgressIndicator(
                        value: pct.clamp(0.05, 1.0),
                        minHeight: 8,
                        backgroundColor: isDark ? VeltricsColors.neutralD800 : Colors.grey.shade200,
                        color: theme.colorScheme.primary,
                      ),
                    ),
                  ],
                ),
              );
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildMetricTile({
    required String label,
    required String value,
    required IconData icon,
    required Color color,
    required ThemeData theme,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 10),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: VeltricsRadius.smAll,
        border: Border.all(color: color.withValues(alpha: 0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, size: 14, color: color),
              const SizedBox(width: 4),
              Expanded(
                child: Text(label, style: VeltricsTextStyles.labelSm.copyWith(fontSize: 10), overflow: TextOverflow.ellipsis),
              ),
            ],
          ),
          const SizedBox(height: 4),
          Text(value, style: VeltricsTextStyles.titleSm.copyWith(fontWeight: FontWeight.bold, fontSize: 13), overflow: TextOverflow.ellipsis),
        ],
      ),
    );
  }

  Widget _buildFuelLogCard(FuelLogModel log, ThemeData theme, bool isDark) {
    final hasEfficiency = log.calculatedEfficiencyKpl != null;
    final hasDistance = log.distanceKm != null && log.distanceKm! > 0;
    final isLeak = log.isLeakAlert;

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(
        borderRadius: VeltricsRadius.smAll,
        side: isLeak
            ? const BorderSide(color: VeltricsColors.errorLight, width: 1.5)
            : BorderSide.none,
      ),
      child: Padding(
        padding: VeltricsSpacing.cardPaddingMobile,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Card Top Bar: Odometer & Fill Date
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    const Icon(Icons.speed, size: 18, color: VeltricsColors.infoLight),
                    const SizedBox(width: 6),
                    Text(
                      '${log.odometerKm.toStringAsFixed(0)} km',
                      style: VeltricsTextStyles.titleLg.copyWith(fontSize: 16),
                    ),
                  ],
                ),
                Text(
                  _formatDate(log.logDate),
                  style: VeltricsTextStyles.bodySm,
                ),
              ],
            ),
            const Divider(height: 16),

            // Card Body: Details Grid
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Quantity: ${log.quantityLiters.toStringAsFixed(1)} L (${log.fuelType})', style: VeltricsTextStyles.bodyMd),
                      const SizedBox(height: 2),
                      Text('Rate: Rs. ${log.pricePerLiter.toStringAsFixed(1)}/L', style: VeltricsTextStyles.bodySm),
                      if (log.stationName != null && log.stationName!.isNotEmpty) ...[
                        const SizedBox(height: 2),
                        Row(
                          children: [
                            const Icon(Icons.place_outlined, size: 12, color: Colors.grey),
                            const SizedBox(width: 2),
                            Expanded(
                              child: Text(
                                log.stationName!,
                                style: VeltricsTextStyles.bodySm,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                          ],
                        ),
                      ],
                    ],
                  ),
                ),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text(
                      'Rs. ${log.totalCost.toStringAsFixed(0)}',
                      style: VeltricsTextStyles.titleLg.copyWith(color: theme.colorScheme.primary),
                    ),
                    const SizedBox(height: 4),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: log.isFullTank
                            ? VeltricsColors.successLight.withValues(alpha: 0.15)
                            : VeltricsColors.infoLight.withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Text(
                        log.isFullTank ? 'FULL TANK' : 'PARTIAL FILL',
                        style: TextStyle(
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                          color: log.isFullTank ? VeltricsColors.successLight : VeltricsColors.infoLight,
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),

            // Efficiency & Distance badges section
            if (hasEfficiency || hasDistance || isLeak || log.receiptPhotoUrl != null) ...[
              const SizedBox(height: 12),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                decoration: BoxDecoration(
                  color: isLeak
                      ? VeltricsColors.errorLight.withValues(alpha: 0.1)
                      : (isDark ? VeltricsColors.neutralD800 : Colors.grey.shade100),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Wrap(
                  alignment: WrapAlignment.spaceBetween,
                  crossAxisAlignment: WrapCrossAlignment.center,
                  spacing: 8,
                  runSpacing: 6,
                  children: [
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        if (hasDistance) ...[
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                            decoration: BoxDecoration(
                              color: VeltricsColors.infoLight.withValues(alpha: 0.2),
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: Row(
                              children: [
                                const Icon(Icons.add_road, size: 12, color: VeltricsColors.infoLight),
                                const SizedBox(width: 4),
                                Text(
                                  '+${log.distanceKm!.toStringAsFixed(1)} km',
                                  style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: VeltricsColors.infoLight),
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(width: 8),
                        ],
                        if (hasEfficiency) ...[
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                            decoration: BoxDecoration(
                              color: isLeak
                                  ? VeltricsColors.errorLight
                                  : VeltricsColors.successLight,
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: Row(
                              children: [
                                Icon(
                                  isLeak ? Icons.trending_down : Icons.bolt,
                                  size: 12,
                                  color: Colors.white,
                                ),
                                const SizedBox(width: 4),
                                Text(
                                  '${log.calculatedEfficiencyKpl!.toStringAsFixed(1)} km/L',
                                  style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.white),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ],
                    ),
                    if (log.receiptPhotoUrl != null && log.receiptPhotoUrl!.isNotEmpty)
                      const Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(Icons.receipt, size: 12, color: VeltricsColors.infoLight),
                          SizedBox(width: 2),
                          Text('Receipt Attached', style: TextStyle(fontSize: 11, color: VeltricsColors.infoLight)),
                        ],
                      ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
