import 'package:flutter/material.dart';

import '../../../../theme/app_theme.dart';
import '../../data/maintenance_repository.dart';
import '../../domain/maintenance_model.dart';
import 'log_maintenance_screen.dart';

class ServiceHistoryScreen extends StatefulWidget {
  final String vehicleId;
  final String organizationId;
  final String? vehicleTitle;
  final double currentOdometer;

  const ServiceHistoryScreen({
    super.key,
    required this.vehicleId,
    required this.organizationId,
    this.vehicleTitle,
    this.currentOdometer = 0.0,
  });

  @override
  State<ServiceHistoryScreen> createState() => _ServiceHistoryScreenState();
}

class _ServiceHistoryScreenState extends State<ServiceHistoryScreen> {
  final MaintenanceRepository _repository = MaintenanceRepository();

  List<ServiceRecordModel> _records = [];
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchHistory();
  }

  Future<void> _fetchHistory() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final list = await _repository.getServiceHistory(
        vehicleId: widget.vehicleId,
        organizationId: widget.organizationId,
      );
      if (!mounted) return;
      setState(() {
        _records = list;
        _isLoading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _errorMessage = e.toString().replaceAll('Exception: ', '');
        _isLoading = false;
      });
    }
  }

  double get _totalSpend => _records.fold(0.0, (sum, item) => sum + item.totalCost);

  Widget _buildSummaryHeader(ThemeData theme, bool isDark) {
    return Container(
      margin: const EdgeInsets.fromLTRB(16, 16, 16, 8),
      padding: VeltricsSpacing.cardPaddingMobile,
      decoration: BoxDecoration(
        color: isDark ? VeltricsColors.neutralD100 : VeltricsColors.neutral50,
        borderRadius: VeltricsRadius.mdAll,
        border: Border.all(
          color: isDark ? VeltricsColors.neutral700 : VeltricsColors.neutral200,
        ),
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('TOTAL SPEND', style: VeltricsTextStyles.labelSm),
                const SizedBox(height: 4),
                Text(
                  'PKR ${_totalSpend.toStringAsFixed(0)}',
                  style: VeltricsTextStyles.titleLg.copyWith(
                    color: theme.colorScheme.primary,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
          Container(
            height: 40,
            width: 1,
            color: isDark ? VeltricsColors.neutral700 : VeltricsColors.neutral300,
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.only(left: 16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('SERVICES LOGGED', style: VeltricsTextStyles.labelSm),
                  const SizedBox(height: 4),
                  Text(
                    '${_records.length} records',
                    style: VeltricsTextStyles.titleSm,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRecordCard(ServiceRecordModel record, ThemeData theme, bool isDark) {
    final dateStr =
        '${record.serviceDate.year}-${record.serviceDate.month.toString().padLeft(2, '0')}-${record.serviceDate.day.toString().padLeft(2, '0')}';
    final provider = record.serviceCenterName ?? 'General Maintenance / Self';

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      child: Padding(
        padding: VeltricsSpacing.cardPaddingMobile,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: theme.colorScheme.primary.withValues(alpha: 0.12),
                    shape: BoxShape.circle,
                  ),
                  child: Icon(
                    Icons.build_circle_outlined,
                    color: theme.colorScheme.primary,
                    size: 24,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        provider,
                        style: VeltricsTextStyles.titleSm,
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 2),
                      Text(
                        dateStr,
                        style: VeltricsTextStyles.labelSm.copyWith(
                          color: isDark ? VeltricsColors.neutral400 : VeltricsColors.neutral600,
                        ),
                      ),
                    ],
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: VeltricsColors.successLight.withValues(alpha: 0.15),
                    borderRadius: VeltricsRadius.pillAll,
                  ),
                  child: Text(
                    'PKR ${record.totalCost.toStringAsFixed(0)}',
                    style: VeltricsTextStyles.labelSm.copyWith(
                      color: VeltricsColors.successLight,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                const Icon(Icons.speed, size: 16, color: VeltricsColors.neutral400),
                const SizedBox(width: 6),
                Text(
                  '${record.odometerKm.toStringAsFixed(0)} km',
                  style: VeltricsTextStyles.bodyMd.copyWith(fontWeight: FontWeight.w600),
                ),
                if (record.performedBy != null && record.performedBy!.isNotEmpty) ...[
                  const SizedBox(width: 16),
                  const Icon(Icons.person_outline, size: 16, color: VeltricsColors.neutral400),
                  const SizedBox(width: 6),
                  Text(record.performedBy!, style: VeltricsTextStyles.bodyMd),
                ],
              ],
            ),
            if (record.notes != null && record.notes!.trim().isNotEmpty) ...[
              const SizedBox(height: 8),
              Text(
                record.notes!,
                style: VeltricsTextStyles.bodyMd.copyWith(
                  fontStyle: FontStyle.italic,
                  color: isDark ? VeltricsColors.neutral300 : VeltricsColors.neutral700,
                ),
              ),
            ],
            if (record.invoicePhotoUrl != null && record.invoicePhotoUrl!.isNotEmpty) ...[
              const SizedBox(height: 10),
              Align(
                alignment: Alignment.centerRight,
                child: TextButton.icon(
                  onPressed: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Invoice Photo: ${record.invoicePhotoUrl}')),
                    );
                  },
                  icon: const Icon(Icons.receipt_long, size: 16),
                  label: const Text('View Invoice Attachment'),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.vehicleTitle != null ? '${widget.vehicleTitle} Service History' : 'Service History'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _fetchHistory,
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
          final logged = await Navigator.push<bool>(
            context,
            MaterialPageRoute(
              builder: (_) => LogMaintenanceScreen(
                vehicleId: widget.vehicleId,
                organizationId: widget.organizationId,
                currentOdometer: widget.currentOdometer,
              ),
            ),
          );
          if (!mounted) return;
          if (logged == true) {
            _fetchHistory();
          }
        },
        icon: const Icon(Icons.add),
        label: const Text('Log Service'),
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
                          Text('Error Loading Service History', style: VeltricsTextStyles.titleLg),
                          const SizedBox(height: VeltricsSpacing.xs3),
                          Text(_errorMessage!, style: VeltricsTextStyles.bodyMd, textAlign: TextAlign.center),
                          const SizedBox(height: VeltricsSpacing.md),
                          ElevatedButton(
                            onPressed: _fetchHistory,
                            child: const Text('Retry'),
                          ),
                        ],
                      ),
                    ),
                  )
                : _records.isEmpty
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Icon(Icons.history_toggle_off_outlined, size: 56, color: VeltricsColors.neutral400),
                            const SizedBox(height: VeltricsSpacing.sm),
                            Text('No Service History Found', style: VeltricsTextStyles.titleSm),
                            const SizedBox(height: VeltricsSpacing.xs3),
                            Text(
                              'Log completed oil changes, repairs, or service records\nto build a complete maintenance log for this vehicle.',
                              style: VeltricsTextStyles.bodyMd,
                              textAlign: TextAlign.center,
                            ),
                            const SizedBox(height: VeltricsSpacing.md),
                            ElevatedButton.icon(
                              onPressed: () async {
                                final logged = await Navigator.push<bool>(
                                  context,
                                  MaterialPageRoute(
                                    builder: (_) => LogMaintenanceScreen(
                                      vehicleId: widget.vehicleId,
                                      organizationId: widget.organizationId,
                                      currentOdometer: widget.currentOdometer,
                                    ),
                                  ),
                                );
                                if (!mounted) return;
                                if (logged == true) {
                                  _fetchHistory();
                                }
                              },
                              icon: const Icon(Icons.add_task),
                              label: const Text('Log First Service'),
                            ),
                          ],
                        ),
                      )
                    : RefreshIndicator(
                        onRefresh: _fetchHistory,
                        child: ListView.builder(
                          padding: const EdgeInsets.only(bottom: 80),
                          itemCount: _records.length + 1,
                          itemBuilder: (context, index) {
                            if (index == 0) {
                              return _buildSummaryHeader(theme, isDark);
                            }
                            final record = _records[index - 1];
                            return _buildRecordCard(record, theme, isDark);
                          },
                        ),
                      ),
      ),
    );
  }
}
