import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/dashboard_repository.dart';
import '../../domain/cost_breakdown_model.dart';

class CostBreakdownCard extends StatefulWidget {
  final String organizationId;
  final String? vehicleId;

  const CostBreakdownCard({
    super.key,
    required this.organizationId,
    this.vehicleId,
  });

  @override
  State<CostBreakdownCard> createState() => _CostBreakdownCardState();
}

class _CostBreakdownCardState extends State<CostBreakdownCard> {
  final DashboardRepository _repository = DashboardRepository();

  CostBreakdownModel? _data;
  bool _isLoading = true;
  String? _errorMessage;
  String _selectedTimeframe = '6m';

  final List<Map<String, String>> _timeframes = [
    {'code': '1m', 'label': '30d'},
    {'code': '3m', 'label': '90d'},
    {'code': '6m', 'label': '6 Months'},
    {'code': '1y', 'label': '1 Year'},
  ];

  @override
  void initState() {
    super.initState();
    _fetchBreakdown();
  }

  Future<void> _fetchBreakdown() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final res = await _repository.getCostBreakdown(
        organizationId: widget.organizationId,
        vehicleId: widget.vehicleId,
        timeframe: _selectedTimeframe,
      );

      if (mounted) {
        setState(() {
          _data = res;
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

    return Card(
      elevation: 2,
      child: Padding(
        padding: VeltricsSpacing.cardPaddingMobile,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    Icon(Icons.pie_chart, color: theme.colorScheme.primary, size: 20),
                    const SizedBox(width: 8),
                    const Text('Cost Breakdown Analytics', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                  ],
                ),
                // Timeframe Choice Chips
                Row(
                  children: _timeframes.map((tf) {
                    final isSel = _selectedTimeframe == tf['code'];
                    return Padding(
                      padding: const EdgeInsets.only(left: 4),
                      child: InkWell(
                        onTap: () {
                          if (_selectedTimeframe != tf['code']) {
                            setState(() => _selectedTimeframe = tf['code']!);
                            _fetchBreakdown();
                          }
                        },
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                          decoration: BoxDecoration(
                            color: isSel ? theme.colorScheme.primary : Colors.grey.withValues(alpha: 0.15),
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: Text(
                            tf['label']!,
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: isSel ? FontWeight.bold : FontWeight.normal,
                              color: isSel ? Colors.white : Colors.black87,
                            ),
                          ),
                        ),
                      ),
                    );
                  }).toList(),
                ),
              ],
            ),
            const SizedBox(height: 12),

            if (_errorMessage != null) ...[
              Text(_errorMessage!, style: const TextStyle(color: VeltricsColors.errorLight, fontSize: 12)),
              const SizedBox(height: 8),
            ],

            if (_isLoading)
              const Center(child: Padding(padding: EdgeInsets.all(24), child: CircularProgressIndicator()))
            else if (_data != null) ...[
              // Total Spend Metrics
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Grand Total Spend:', style: TextStyle(fontSize: 13, color: Colors.grey)),
                  Text(
                    'Rs. ${_data!.grandTotalCost.toStringAsFixed(0)}',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: theme.colorScheme.primary),
                  ),
                ],
              ),
              const SizedBox(height: 12),

              // Stacked Progress Bar (Fuel vs Maintenance vs Expenses)
              if (_data!.grandTotalCost > 0) ...[
                ClipRRect(
                  borderRadius: BorderRadius.circular(4),
                  child: SizedBox(
                    height: 12,
                    child: Row(
                      children: [
                        if (_data!.totalFuelCost > 0)
                          Expanded(
                            flex: (_data!.totalFuelCost / _data!.grandTotalCost * 100).round(),
                            child: Container(color: VeltricsColors.warningLight),
                          ),
                        if (_data!.totalMaintenanceCost > 0)
                          Expanded(
                            flex: (_data!.totalMaintenanceCost / _data!.grandTotalCost * 100).round(),
                            child: Container(color: VeltricsColors.infoLight),
                          ),
                        if (_data!.totalOtherExpenseCost > 0)
                          Expanded(
                            flex: (_data!.totalOtherExpenseCost / _data!.grandTotalCost * 100).round(),
                            child: Container(color: VeltricsColors.successLight),
                          ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 12),
              ],

              // Category Legend Grid
              Row(
                children: [
                  Expanded(
                    child: _buildCategoryLegend(
                      label: 'Fuel',
                      amount: _data!.totalFuelCost,
                      color: VeltricsColors.warningLight,
                      icon: Icons.local_gas_station,
                    ),
                  ),
                  Expanded(
                    child: _buildCategoryLegend(
                      label: 'Maintenance',
                      amount: _data!.totalMaintenanceCost,
                      color: VeltricsColors.infoLight,
                      icon: Icons.build,
                    ),
                  ),
                  Expanded(
                    child: _buildCategoryLegend(
                      label: 'Expenses',
                      amount: _data!.totalOtherExpenseCost,
                      color: VeltricsColors.successLight,
                      icon: Icons.payments,
                    ),
                  ),
                ],
              ),

              if (_data!.items.isNotEmpty) ...[
                const Divider(height: 24),
                const Text('Monthly Cost Trends', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                const SizedBox(height: 8),
                ..._data!.items.take(4).map((item) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 4),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(item.period, style: const TextStyle(fontSize: 12, color: Colors.grey)),
                        Text(
                          'Rs. ${item.totalCost.toStringAsFixed(0)}',
                          style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                  );
                }),
              ],
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildCategoryLegend({
    required String label,
    required double amount,
    required Color color,
    required IconData icon,
  }) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 14, color: color),
            const SizedBox(width: 4),
            Text(label, style: const TextStyle(fontSize: 11, color: Colors.grey)),
          ],
        ),
        const SizedBox(height: 2),
        Text(
          'Rs. ${amount.toStringAsFixed(0)}',
          style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: color),
        ),
      ],
    );
  }
}
