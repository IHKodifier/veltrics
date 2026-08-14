import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../../fuel/presentation/screens/log_fuel_screen.dart';
import '../../../trip/presentation/widgets/quick_log_trip_dialog.dart';
import '../../../expense/presentation/widgets/quick_log_expense_dialog.dart';

class VeltricsQuickActionsFab extends StatefulWidget {
  final String vehicleId;
  final String organizationId;
  final VoidCallback? onLogComplete;

  const VeltricsQuickActionsFab({
    super.key,
    required this.vehicleId,
    required this.organizationId,
    this.onLogComplete,
  });

  @override
  State<VeltricsQuickActionsFab> createState() => _VeltricsQuickActionsFabState();
}

class _VeltricsQuickActionsFabState extends State<VeltricsQuickActionsFab> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _expandAnimation;
  bool _isOpen = false;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      value: _isOpen ? 1.0 : 0.0,
      duration: const Duration(milliseconds: 250),
      vsync: this,
    );
    _expandAnimation = CurvedAnimation(
      curve: Curves.fastOutSlowIn,
      reverseCurve: Curves.easeOutQuad,
      parent: _controller,
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _toggle() {
    setState(() {
      _isOpen = !_isOpen;
      if (_isOpen) {
        _controller.forward();
      } else {
        _controller.reverse();
      }
    });
  }

  Future<void> _openQuickLogFuel() async {
    _toggle();
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => LogFuelScreen(
          vehicleId: widget.vehicleId,
          organizationId: widget.organizationId,
        ),
      ),
    );
    if (result != null && mounted && widget.onLogComplete != null) {
      widget.onLogComplete!();
    }
  }

  Future<void> _openQuickLogTrip() async {
    _toggle();
    final result = await showDialog(
      context: context,
      builder: (_) => QuickLogTripDialog(
        vehicleId: widget.vehicleId,
        organizationId: widget.organizationId,
      ),
    );
    if (result != null && mounted && widget.onLogComplete != null) {
      widget.onLogComplete!();
    }
  }

  Future<void> _openQuickLogExpense() async {
    _toggle();
    final result = await showDialog(
      context: context,
      builder: (_) => QuickLogExpenseDialog(
        vehicleId: widget.vehicleId,
        organizationId: widget.organizationId,
      ),
    );
    if (result != null && mounted && widget.onLogComplete != null) {
      widget.onLogComplete!();
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.end,
      children: [
        if (_isOpen) ...[
          _buildActionButton(
            label: 'Quick Log Fuel',
            icon: Icons.local_gas_station,
            color: VeltricsColors.warningLight,
            onTap: _openQuickLogFuel,
          ),
          const SizedBox(height: 12),
          _buildActionButton(
            label: 'Quick Log Trip',
            icon: Icons.directions_car,
            color: VeltricsColors.infoLight,
            onTap: _openQuickLogTrip,
          ),
          const SizedBox(height: 12),
          _buildActionButton(
            label: 'Quick Log Expense',
            icon: Icons.payments,
            color: VeltricsColors.successLight,
            onTap: _openQuickLogExpense,
          ),
          const SizedBox(height: 12),
        ],
        FloatingActionButton(
          heroTag: 'quick_actions_fab',
          onPressed: _toggle,
          backgroundColor: theme.colorScheme.primary,
          child: AnimatedIcon(
            icon: AnimatedIcons.menu_close,
            progress: _expandAnimation,
            color: Colors.white,
          ),
        ),
      ],
    );
  }

  Widget _buildActionButton({
    required String label,
    required IconData icon,
    required Color color,
    required VoidCallback onTap,
  }) {
    return ScaleTransition(
      scale: _expandAnimation,
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
            decoration: BoxDecoration(
              color: Colors.black87,
              borderRadius: BorderRadius.circular(6),
            ),
            child: Text(
              label,
              style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
            ),
          ),
          const SizedBox(width: 8),
          FloatingActionButton.small(
            heroTag: label,
            onPressed: onTap,
            backgroundColor: color,
            child: Icon(icon, color: Colors.white),
          ),
        ],
      ),
    );
  }
}
