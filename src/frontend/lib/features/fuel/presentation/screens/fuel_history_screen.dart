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
      setState(() {
        _fuelLogs = logs;
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
    final validEfficiencies = _fuelLogs
        .where((log) => log.isFullTank && log.calculatedEfficiencyKpl != null)
        .map((log) => log.calculatedEfficiencyKpl!)
        .toList();
    if (validEfficiencies.isEmpty) return 0.0;
    return validEfficiencies.reduce((a, b) => a + b) / validEfficiencies.length;
  }

  double _calculateTotalCost() {
    if (_fuelLogs.isEmpty) return 0.0;
    return _fuelLogs.fold(0.0, (sum, item) => sum + item.totalCost);
  }

  double _calculateTotalLiters() {
    if (_fuelLogs.isEmpty) return 0.0;
    return _fuelLogs.fold(0.0, (sum, item) => sum + item.quantityLiters);
  }

  String _formatDate(DateTime dt) {
    final months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    final hour = dt.hour.toString().padLeft(2, '0');
    final min = dt.minute.toString().padLeft(2, '0');
    return '${dt.day} ${months[dt.month - 1]} ${dt.year} • $hour:$min';
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    final avgEfficiency = _calculateAverageEfficiency();
    final totalCost = _calculateTotalCost();
    final totalLiters = _calculateTotalLiters();
    final leakAlertCount = _fuelLogs.where((l) => l.isLeakAlert).length;

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
                              Text('SCR-FUEL-001 • Fuel Log History & Efficiency', style: VeltricsTextStyles.labelSm),
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
                              _buildSummaryMetricsCard(theme, isDark, avgEfficiency, totalCost, totalLiters),
                              const SizedBox(height: VeltricsSpacing.md),

                              Text('Fill-Up Log Timeline (${_fuelLogs.length})', style: VeltricsTextStyles.titleLg),
                              const SizedBox(height: VeltricsSpacing.xs2),

                              // 4. Fuel Log Cards List
                              ..._fuelLogs.map((log) => _buildFuelLogCard(log, theme, isDark)),
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
  ) {
    return Card(
      child: Padding(
        padding: VeltricsSpacing.cardPaddingMobile,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('EFFICIENCY OVERVIEW', style: VeltricsTextStyles.labelSm),
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
            if (hasEfficiency || hasDistance || isLeak) ...[
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
                    if (isLeak)
                      const Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(Icons.warning_amber, size: 14, color: VeltricsColors.errorLight),
                          SizedBox(width: 4),
                          Text(
                            'Leak Alert (>30% drop)',
                            style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: VeltricsColors.errorLight),
                          ),
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
