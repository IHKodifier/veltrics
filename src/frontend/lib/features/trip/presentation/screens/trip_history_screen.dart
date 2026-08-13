import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/trip_repository.dart';
import '../../domain/trip_model.dart';
import 'log_trip_screen.dart';

class TripHistoryScreen extends StatefulWidget {
  final String vehicleId;
  final String organizationId;
  final String vehicleTitle;
  final double currentOdometer;

  const TripHistoryScreen({
    super.key,
    required this.vehicleId,
    required this.organizationId,
    this.vehicleTitle = 'Vehicle Trip History',
    this.currentOdometer = 0.0,
  });

  @override
  State<TripHistoryScreen> createState() => _TripHistoryScreenState();
}

class _TripHistoryScreenState extends State<TripHistoryScreen> {
  final TripRepository _repository = TripRepository();

  List<TripModel> _trips = [];
  TripSummaryModel? _summary;
  bool _isLoading = true;
  String? _errorMessage;
  String _selectedPurposeFilter = 'ALL'; // ALL, BUSINESS, PERSONAL

  @override
  void initState() {
    super.initState();
    _fetchTripHistory();
  }

  Future<void> _fetchTripHistory() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final trips = await _repository.getTrips(
        vehicleId: widget.vehicleId,
        tripPurpose: _selectedPurposeFilter == 'ALL' ? null : _selectedPurposeFilter,
        organizationId: widget.organizationId,
      );
      TripSummaryModel? summary;
      try {
        summary = await _repository.getTripSummary(
          vehicleId: widget.vehicleId,
          organizationId: widget.organizationId,
        );
      } catch (_) {}

      setState(() {
        _trips = trips;
        _summary = summary;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll('Exception: ', '');
        _isLoading = false;
      });
    }
  }

  String _formatDate(DateTime dt) {
    final months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    final hour = dt.hour.toString().padLeft(2, '0');
    final min = dt.minute.toString().padLeft(2, '0');
    return '${dt.day} ${months[dt.month - 1]} ${dt.year} • $hour:$min';
  }

  Future<void> _confirmDeleteTrip(TripModel trip) async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Trip Entry'),
        content: Text(
          'Are you sure you want to delete this trip record (${trip.originName ?? 'Origin'} ➔ ${trip.destinationName ?? 'Destination'} • +${trip.distanceKm?.toStringAsFixed(1) ?? '0'} km)?',
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
        await _repository.deleteTrip(
          tripId: trip.id,
          organizationId: widget.organizationId,
        );
        if (mounted) {
          Navigator.pop(context);
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Trip entry deleted successfully')),
          );
          _fetchTripHistory();
        }
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Failed to delete trip: $e')),
          );
        }
      }
    }
  }

  void _showTripDetailDialog(TripModel trip, ThemeData theme) {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(borderRadius: VeltricsRadius.mdAll),
          title: Row(
            children: [
              Icon(
                trip.tripPurpose == 'BUSINESS' ? Icons.work : Icons.person,
                color: theme.colorScheme.primary,
              ),
              const SizedBox(width: 8),
              const Text('Trip Detail Record', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            ],
          ),
          content: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                _buildDetailRow('Start Time:', _formatDate(trip.startTime)),
                if (trip.endTime != null) _buildDetailRow('End Time:', _formatDate(trip.endTime!)),
                _buildDetailRow('Origin:', trip.originName ?? 'Not specified'),
                _buildDetailRow('Destination:', trip.destinationName ?? 'Not specified'),
                _buildDetailRow('Start Odometer:', '${trip.startOdometerKm.toStringAsFixed(0)} km'),
                if (trip.endOdometerKm != null) _buildDetailRow('End Odometer:', '${trip.endOdometerKm!.toStringAsFixed(0)} km'),
                if (trip.distanceKm != null) _buildDetailRow('Distance Traveled:', '${trip.distanceKm!.toStringAsFixed(1)} km'),
                _buildDetailRow('Classification:', trip.tripPurpose),
                _buildDetailRow('Recording Type:', trip.isManual ? 'Manual Entry' : 'GPS Tracked'),
                _buildDetailRow('Status:', trip.status),
                if (trip.notes != null && trip.notes!.isNotEmpty) ...[
                  const SizedBox(height: 8),
                  const Text('Notes:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                  const SizedBox(height: 2),
                  Text(trip.notes!, style: const TextStyle(fontSize: 12, color: Colors.grey)),
                ],
              ],
            ),
          ),
          actions: [
            TextButton.icon(
              icon: const Icon(Icons.delete_outline, color: VeltricsColors.errorLight, size: 18),
              label: const Text('Delete', style: TextStyle(color: VeltricsColors.errorLight)),
              onPressed: () => _confirmDeleteTrip(trip),
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

    final totalDist = _summary?.totalDistanceKm ?? _trips.fold<double>(0.0, (sum, item) => sum + (item.distanceKm ?? 0.0));
    final bizDist = _summary?.businessDistanceKm ?? _trips.where((t) => t.tripPurpose == 'BUSINESS').fold<double>(0.0, (sum, item) => sum + (item.distanceKm ?? 0.0));
    final perDist = _summary?.personalDistanceKm ?? _trips.where((t) => t.tripPurpose == 'PERSONAL').fold<double>(0.0, (sum, item) => sum + (item.distanceKm ?? 0.0));
    final taxDeduction = _summary?.estimatedTaxDeduction ?? (bizDist * 0.65);

    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Trip History & Log', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            Text(widget.vehicleTitle, style: const TextStyle(fontSize: 12, color: Colors.white70)),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Refresh History',
            onPressed: _fetchTripHistory,
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
          final result = await Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => LogTripScreen(
                vehicleId: widget.vehicleId,
                organizationId: widget.organizationId,
                currentOdometer: widget.currentOdometer,
              ),
            ),
          );
          if (result != null) {
            _fetchTripHistory();
          }
        },
        icon: const Icon(Icons.add_road),
        label: const Text('Log Trip'),
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
                          Text('Failed to Load Trip History', style: VeltricsTextStyles.titleLg),
                          const SizedBox(height: VeltricsSpacing.xs3),
                          Text(_errorMessage!, style: VeltricsTextStyles.bodyMd, textAlign: TextAlign.center),
                          const SizedBox(height: VeltricsSpacing.md),
                          ElevatedButton(
                            onPressed: _fetchTripHistory,
                            child: const Text('Retry'),
                          ),
                        ],
                      ),
                    ),
                  )
                : RefreshIndicator(
                    onRefresh: _fetchTripHistory,
                    child: ListView(
                      padding: VeltricsSpacing.pagePadding,
                      children: [
                        Text('SCR-TRIP-001 • Trip Directory & Distance Summary', style: VeltricsTextStyles.labelSm),
                        const SizedBox(height: VeltricsSpacing.xs2),

                        // 1. Distance & Tax Summary Card
                        _buildSummaryMetricsCard(theme, totalDist, bizDist, perDist, taxDeduction),
                        const SizedBox(height: VeltricsSpacing.sm),

                        // 2. Purpose Filter Chips
                        Row(
                          children: [
                            FilterChip(
                              label: const Text('All Trips'),
                              selected: _selectedPurposeFilter == 'ALL',
                              onSelected: (sel) {
                                if (sel) {
                                  setState(() => _selectedPurposeFilter = 'ALL');
                                  _fetchTripHistory();
                                }
                              },
                            ),
                            const SizedBox(width: 8),
                            FilterChip(
                              label: const Text('Business'),
                              selected: _selectedPurposeFilter == 'BUSINESS',
                              onSelected: (sel) {
                                if (sel) {
                                  setState(() => _selectedPurposeFilter = 'BUSINESS');
                                  _fetchTripHistory();
                                }
                              },
                            ),
                            const SizedBox(width: 8),
                            FilterChip(
                              label: const Text('Personal'),
                              selected: _selectedPurposeFilter == 'PERSONAL',
                              onSelected: (sel) {
                                if (sel) {
                                  setState(() => _selectedPurposeFilter = 'PERSONAL');
                                  _fetchTripHistory();
                                }
                              },
                            ),
                          ],
                        ),
                        const SizedBox(height: VeltricsSpacing.sm),

                        // 3. Trips Timeline List
                        if (_trips.isEmpty) ...[
                          const SizedBox(height: 40),
                          Center(
                            child: Column(
                              children: [
                                Icon(Icons.route, size: 48, color: Colors.grey.withValues(alpha: 0.5)),
                                const SizedBox(height: 12),
                                Text('No Trips Logged Yet', style: VeltricsTextStyles.titleLg),
                                const SizedBox(height: 6),
                                Text('Log trips manually or start live GPS tracking.', style: VeltricsTextStyles.bodyMd),
                              ],
                            ),
                          ),
                        ] else ...[
                          ..._trips.map((trip) => InkWell(
                                onTap: () => _showTripDetailDialog(trip, theme),
                                child: _buildTripCard(trip, theme, isDark),
                              )),
                        ],
                        const SizedBox(height: 80),
                      ],
                    ),
                  ),
      ),
    );
  }

  Widget _buildSummaryMetricsCard(
    ThemeData theme,
    double totalDist,
    double bizDist,
    double perDist,
    double taxDeduction,
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
                Text('MILEAGE & TAX DEDUCTIONS', style: VeltricsTextStyles.labelSm),
                Icon(Icons.route, color: theme.colorScheme.primary, size: 20),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: _buildMetricTile(
                    label: 'Total Distance',
                    value: '${totalDist.toStringAsFixed(1)} km',
                    icon: Icons.map,
                    color: VeltricsColors.infoLight,
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: _buildMetricTile(
                    label: 'Business',
                    value: '${bizDist.toStringAsFixed(1)} km',
                    icon: Icons.work,
                    color: VeltricsColors.successLight,
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: _buildMetricTile(
                    label: 'Est. Tax Saved',
                    value: 'Rs. ${taxDeduction.toStringAsFixed(0)}',
                    icon: Icons.savings,
                    color: VeltricsColors.warningLight,
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
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 10),
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

  Widget _buildTripCard(TripModel trip, ThemeData theme, bool isDark) {
    final isBiz = trip.tripPurpose == 'BUSINESS';
    final distance = trip.distanceKm ?? 0.0;

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
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
                    Icon(
                      isBiz ? Icons.work : Icons.person,
                      size: 16,
                      color: isBiz ? VeltricsColors.successLight : VeltricsColors.infoLight,
                    ),
                    const SizedBox(width: 6),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(
                        color: (isBiz ? VeltricsColors.successLight : VeltricsColors.infoLight).withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Text(
                        trip.tripPurpose,
                        style: TextStyle(
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                          color: isBiz ? VeltricsColors.successLight : VeltricsColors.infoLight,
                        ),
                      ),
                    ),
                  ],
                ),
                Text(_formatDate(trip.startTime), style: VeltricsTextStyles.bodySm),
              ],
            ),
            const Divider(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.trip_origin, size: 14, color: Colors.grey),
                          const SizedBox(width: 4),
                          Expanded(
                            child: Text(
                              trip.originName ?? 'Origin not specified',
                              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Row(
                        children: [
                          const Icon(Icons.place_outlined, size: 14, color: Colors.grey),
                          const SizedBox(width: 4),
                          Expanded(
                            child: Text(
                              trip.destinationName ?? 'Destination not specified',
                              style: const TextStyle(fontSize: 12, color: Colors.grey),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text(
                      '+${distance.toStringAsFixed(1)} km',
                      style: VeltricsTextStyles.titleLg.copyWith(color: theme.colorScheme.primary, fontSize: 16),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      '${trip.startOdometerKm.toStringAsFixed(0)} ➔ ${trip.endOdometerKm?.toStringAsFixed(0) ?? '?'} km',
                      style: const TextStyle(fontSize: 10, color: Colors.grey),
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
