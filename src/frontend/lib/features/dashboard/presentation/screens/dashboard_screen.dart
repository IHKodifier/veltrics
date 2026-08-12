import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/dashboard_repository.dart';
import '../../domain/dashboard_model.dart';
import '../../../vehicle/presentation/screens/add_vehicle_screen.dart';

class DashboardScreen extends StatefulWidget {
  final String organizationId;

  const DashboardScreen({
    super.key,
    this.organizationId = "org-demo-101",
  });

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final DashboardRepository _dashboardRepository = DashboardRepository();
  late Future<DashboardSummaryModel> _summaryFuture;

  @override
  void initState() {
    super.initState();
    _loadSummary();
  }

  void _loadSummary() {
    setState(() {
      _summaryFuture = _dashboardRepository.getSummary(organizationId: widget.organizationId);
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Fleet Dashboard',
              style: VeltricsTextStyles.titleLg.copyWith(
                fontWeight: FontWeight.w700,
                color: isDark ? VeltricsColors.neutralD900 : VeltricsColors.neutral900,
              ),
            ),
            Text(
              'Overview & Real-time Metrics',
              style: VeltricsTextStyles.bodySm.copyWith(
                color: isDark ? VeltricsColors.neutralD500 : VeltricsColors.neutral500,
              ),
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Refresh Dashboard',
            onPressed: _loadSummary,
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          _loadSummary();
          await _summaryFuture;
        },
        child: FutureBuilder<DashboardSummaryModel>(
          future: _summaryFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }

            if (snapshot.hasError) {
              return Center(
                child: Padding(
                  padding: const EdgeInsets.all(VeltricsSpacing.md),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.error_outline, size: 48, color: VeltricsColors.errorLight),
                      const SizedBox(height: VeltricsSpacing.xs3),
                      Text(
                        'Failed to load dashboard metrics',
                        style: VeltricsTextStyles.titleMd,
                      ),
                      const SizedBox(height: VeltricsSpacing.xs2),
                      Text(
                        '${snapshot.error}',
                        style: VeltricsTextStyles.bodySm.copyWith(color: VeltricsColors.neutral500),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: VeltricsSpacing.md),
                      ElevatedButton.icon(
                        onPressed: _loadSummary,
                        icon: const Icon(Icons.refresh),
                        label: const Text('Retry'),
                      ),
                    ],
                  ),
                ),
              );
            }

            final summary = snapshot.data!;

            return SingleChildScrollView(
              physics: const AlwaysScrollableScrollPhysics(),
              padding: const EdgeInsets.all(VeltricsSpacing.sm),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Zero Vehicle Empty State Onboarding Card
                  if (summary.totalVehicles == 0) ...[
                    _buildOnboardingCard(context, isDark),
                    const SizedBox(height: VeltricsSpacing.md),
                  ],

                  // Overview Headline Summary
                  Text(
                    'Key Performance Indicators',
                    style: VeltricsTextStyles.titleMd.copyWith(
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  const SizedBox(height: VeltricsSpacing.xs3),

                  // KPI Cards Grid (Responsive 2-column or 1-column layout)
                  LayoutBuilder(
                    builder: (context, constraints) {
                      final crossAxisCount = constraints.maxWidth > 600 ? 2 : 1;
                      return GridView.count(
                        crossAxisCount: crossAxisCount,
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        mainAxisSpacing: VeltricsSpacing.xs3,
                        crossAxisSpacing: VeltricsSpacing.xs3,
                        childAspectRatio: crossAxisCount == 2 ? 1.8 : 2.2,
                        children: [
                          _buildKpiCard(
                            context: context,
                            title: 'Total Vehicles',
                            value: '${summary.totalVehicles}',
                            subtitle: summary.totalVehicles == 1 ? '1 Active Vehicle' : '${summary.totalVehicles} Active Vehicles',
                            icon: Icons.directions_car_rounded,
                            accentColor: VeltricsColors.infoLight,
                            bgColor: VeltricsColors.infoBgLight,
                            isDark: isDark,
                          ),
                          _buildKpiCard(
                            context: context,
                            title: 'Monthly Expenses',
                            value: 'PKR ${summary.monthlyTotalCost.toStringAsFixed(0)}',
                            subtitle: 'Current Month Total Cost',
                            icon: Icons.account_balance_wallet_rounded,
                            accentColor: VeltricsColors.successLight,
                            bgColor: VeltricsColors.successBgLight,
                            isDark: isDark,
                          ),
                          _buildKpiCard(
                            context: context,
                            title: 'Overdue Maintenance',
                            value: '${summary.overdueMaintenanceCount}',
                            subtitle: summary.overdueMaintenanceCount > 0
                                ? 'Immediate Attention Needed'
                                : 'All Schedules Up to Date',
                            icon: Icons.warning_amber_rounded,
                            accentColor: summary.overdueMaintenanceCount > 0
                                ? VeltricsColors.errorLight
                                : VeltricsColors.neutral500,
                            bgColor: summary.overdueMaintenanceCount > 0
                                ? VeltricsColors.errorBgLight
                                : VeltricsColors.neutral100,
                            isDark: isDark,
                            badgeText: summary.overdueMaintenanceCount > 0 ? 'ALERT' : 'OK',
                          ),
                          _buildKpiCard(
                            context: context,
                            title: 'Upcoming Maintenance',
                            value: '${summary.upcomingMaintenanceCount}',
                            subtitle: 'Due within 7 days / 500 km',
                            icon: Icons.build_circle_rounded,
                            accentColor: VeltricsColors.warningLight,
                            bgColor: VeltricsColors.warningBgLight,
                            isDark: isDark,
                          ),
                          _buildKpiCard(
                            context: context,
                            title: 'Active Drivers',
                            value: '${summary.totalDrivers}',
                            subtitle: 'Assigned Drivers',
                            icon: Icons.person_pin_rounded,
                            accentColor: VeltricsColors.proBadgeLight,
                            bgColor: const Color(0xFFEDE9FE),
                            isDark: isDark,
                          ),
                        ],
                      );
                    },
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }

  Widget _buildOnboardingCard(BuildContext context, bool isDark) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(VeltricsSpacing.md),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: isDark
              ? [const Color(0xFF0F766E), const Color(0xFF115E59)]
              : [const Color(0xFF14B8A6), const Color(0xFF0D9488)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: VeltricsRadius.lgAll,
        boxShadow: const [
          BoxShadow(
            color: Colors.black12,
            blurRadius: 10,
            offset: Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(VeltricsSpacing.xs2),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.2),
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.directions_car_filled_rounded,
                  color: Colors.white,
                  size: 28,
                ),
              ),
              const SizedBox(width: VeltricsSpacing.xs3),
              Expanded(
                child: Text(
                  'Welcome to Veltrics!',
                  style: VeltricsTextStyles.titleLg.copyWith(
                    color: Colors.white,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: VeltricsSpacing.xs3),
          Text(
            'You haven\'t registered any vehicles in your active fleet organization yet. Add your first vehicle to enable automated maintenance reminders and expense tracking.',
            style: VeltricsTextStyles.bodyMd.copyWith(
              color: Colors.white.withValues(alpha: 0.9),
            ),
          ),
          const SizedBox(height: VeltricsSpacing.md),
          ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.white,
              foregroundColor: const Color(0xFF0F766E),
              shape: RoundedRectangleBorder(
                borderRadius: VeltricsRadius.pillAll,
              ),
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
            ),
            onPressed: () async {
              await Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => AddVehicleScreen(organizationId: widget.organizationId),
                ),
              );
              _loadSummary();
            },
            icon: const Icon(Icons.add_rounded),
            label: const Text(
              'Add Your First Vehicle',
              style: TextStyle(fontWeight: FontWeight.w700),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildKpiCard({
    required BuildContext context,
    required String title,
    required String value,
    required String subtitle,
    required IconData icon,
    required Color accentColor,
    required Color bgColor,
    required bool isDark,
    String? badgeText,
  }) {
    final cardBg = isDark ? VeltricsColors.neutralD100 : Colors.white;

    return Container(
      padding: const EdgeInsets.all(VeltricsSpacing.sm),
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: VeltricsRadius.mdAll,
        border: Border.all(
          color: isDark ? VeltricsColors.neutralD300 : VeltricsColors.neutral200,
          width: 1,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.03),
            blurRadius: 6,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: isDark ? accentColor.withValues(alpha: 0.2) : bgColor,
                  borderRadius: VeltricsRadius.smAll,
                ),
                child: Icon(icon, color: accentColor, size: 22),
              ),
              if (badgeText != null)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                  decoration: BoxDecoration(
                    color: accentColor.withValues(alpha: 0.15),
                    borderRadius: VeltricsRadius.pillAll,
                  ),
                  child: Text(
                    badgeText,
                    style: VeltricsTextStyles.labelSm.copyWith(
                      color: accentColor,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ),
            ],
          ),
          const SizedBox(height: VeltricsSpacing.xs1),
          Text(
            value,
            style: VeltricsTextStyles.dashboardMetric.copyWith(
              color: isDark ? VeltricsColors.neutralD900 : VeltricsColors.neutral900,
              fontSize: 26,
            ),
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: VeltricsTextStyles.labelLg.copyWith(
                  fontWeight: FontWeight.w600,
                  color: isDark ? VeltricsColors.neutralD900 : VeltricsColors.neutral800,
                ),
              ),
              Text(
                subtitle,
                style: VeltricsTextStyles.bodySm.copyWith(
                  color: isDark ? VeltricsColors.neutralD500 : VeltricsColors.neutral500,
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ],
      ),
    );
  }
}
