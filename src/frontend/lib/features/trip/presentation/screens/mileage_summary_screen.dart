import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/trip_repository.dart';
import '../../domain/trip_model.dart';

class MileageSummaryScreen extends StatefulWidget {
  final String? vehicleId;
  final String organizationId;

  const MileageSummaryScreen({
    super.key,
    this.vehicleId,
    required this.organizationId,
  });

  @override
  State<MileageSummaryScreen> createState() => _MileageSummaryScreenState();
}

class _MileageSummaryScreenState extends State<MileageSummaryScreen> {
  final TripRepository _repository = TripRepository();

  MileageSummaryModel? _summary;
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchSummaryData();
  }

  Future<void> _fetchSummaryData() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final summary = await _repository.getMileageSummary(
        vehicleId: widget.vehicleId,
        organizationId: widget.organizationId,
      );

      if (mounted) {
        setState(() {
          _summary = summary;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _errorMessage = e.toString().replaceAll('Exception: ', '');
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Mileage & Distance Analytics', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _fetchSummaryData,
          ),
        ],
      ),
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: _fetchSummaryData,
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: VeltricsSpacing.pagePadding,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('SCR-TRIP-002 • Vehicle Mileage Summary & Tax Deductions', style: VeltricsTextStyles.labelSm),
                const SizedBox(height: VeltricsSpacing.xs2),

                if (_errorMessage != null) ...[
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: VeltricsColors.errorLight.withValues(alpha: 0.15),
                      borderRadius: VeltricsRadius.smAll,
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.error_outline, color: VeltricsColors.errorLight),
                        const SizedBox(width: 8),
                        Expanded(child: Text(_errorMessage!, style: const TextStyle(color: VeltricsColors.errorLight))),
                      ],
                    ),
                  ),
                  const SizedBox(height: 16),
                ],

                if (_isLoading)
                  const Center(child: Padding(padding: EdgeInsets.all(48), child: CircularProgressIndicator()))
                else if (_summary != null) ...[
                  // 1. Total Distance & Tax Deduction Metric Card
                  Card(
                    elevation: 3,
                    child: Padding(
                      padding: VeltricsSpacing.cardPaddingMobile,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text('TOTAL DISTANCE LOGGED', style: VeltricsTextStyles.labelSm),
                              Icon(Icons.route, color: theme.colorScheme.primary, size: 20),
                            ],
                          ),
                          const SizedBox(height: 6),
                          Text(
                            '${_summary!.totalDistanceKm.toStringAsFixed(1)} km',
                            style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: theme.colorScheme.primary),
                          ),
                          const SizedBox(height: 12),
                          Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: VeltricsColors.successLight.withValues(alpha: 0.12),
                              borderRadius: VeltricsRadius.smAll,
                            ),
                            child: Row(
                              children: [
                                const Icon(Icons.request_quote, color: VeltricsColors.successLight),
                                const SizedBox(width: 10),
                                Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    const Text('Estimated Tax Deduction', style: TextStyle(fontSize: 11, color: Colors.grey)),
                                    Text(
                                      'Rs. ${_summary!.estimatedTaxDeduction.toStringAsFixed(0)}',
                                      style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: VeltricsColors.successLight),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),

                  // 2. Business vs Personal Breakdown Card
                  Card(
                    child: Padding(
                      padding: VeltricsSpacing.cardPaddingMobile,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('BUSINESS VS PERSONAL BREAKDOWN', style: VeltricsTextStyles.labelSm),
                          const SizedBox(height: 16),

                          // Progress ratio bar
                          ClipRRect(
                            borderRadius: BorderRadius.circular(4),
                            child: LinearProgressIndicator(
                              value: _summary!.totalDistanceKm > 0
                                  ? (_summary!.businessDistanceKm / _summary!.totalDistanceKm)
                                  : 0.5,
                              minHeight: 12,
                              backgroundColor: VeltricsColors.infoLight,
                              valueColor: AlwaysStoppedAnimation<Color>(theme.colorScheme.primary),
                            ),
                          ),
                          const SizedBox(height: 16),

                          Row(
                            children: [
                              Expanded(
                                child: _buildStatItem(
                                  label: 'Business Distance',
                                  value: '${_summary!.businessDistanceKm.toStringAsFixed(1)} km',
                                  subtext: '${_summary!.businessTripsCount} trips',
                                  icon: Icons.work,
                                  color: theme.colorScheme.primary,
                                ),
                              ),
                              Container(height: 40, width: 1, color: Colors.grey.withValues(alpha: 0.3)),
                              Expanded(
                                child: _buildStatItem(
                                  label: 'Personal Distance',
                                  value: '${_summary!.personalDistanceKm.toStringAsFixed(1)} km',
                                  subtext: '${_summary!.personalTripsCount} trips',
                                  icon: Icons.person,
                                  color: VeltricsColors.infoLight,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),

                  // 3. Trip Statistics Grid
                  Card(
                    child: Padding(
                      padding: VeltricsSpacing.cardPaddingMobile,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('TRIP STATISTICAL METRICS', style: VeltricsTextStyles.labelSm),
                          const SizedBox(height: 12),
                          _buildDetailRow('Total Trips Completed:', '${_summary!.totalTripsCount}'),
                          _buildDetailRow('Average Distance per Trip:', '${_summary!.averageTripDistanceKm.toStringAsFixed(1)} km'),
                          _buildDetailRow('Standard Tax Rate:', 'Rs. 0.65 / km'),
                        ],
                      ),
                    ),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildStatItem({
    required String label,
    required String value,
    required String subtext,
    required IconData icon,
    required Color color,
  }) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 16, color: color),
            const SizedBox(width: 4),
            Text(label, style: const TextStyle(fontSize: 11, color: Colors.grey)),
          ],
        ),
        const SizedBox(height: 4),
        Text(value, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: color)),
        Text(subtext, style: const TextStyle(fontSize: 11, color: Colors.grey)),
      ],
    );
  }

  Widget _buildDetailRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 13, color: Colors.grey)),
          Text(value, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}
