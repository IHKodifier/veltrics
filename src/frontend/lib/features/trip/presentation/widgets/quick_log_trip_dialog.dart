import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/trip_repository.dart';

class QuickLogTripDialog extends StatefulWidget {
  final String vehicleId;
  final String organizationId;

  const QuickLogTripDialog({
    super.key,
    required this.vehicleId,
    required this.organizationId,
  });

  @override
  State<QuickLogTripDialog> createState() => _QuickLogTripDialogState();
}

class _QuickLogTripDialogState extends State<QuickLogTripDialog> {
  final _formKey = GlobalKey<FormState>();
  final TripRepository _repository = TripRepository();

  final TextEditingController _distanceController = TextEditingController();
  final TextEditingController _destinationController = TextEditingController();

  String _tripPurpose = 'BUSINESS';
  bool _isSubmitting = false;
  String? _errorMessage;

  @override
  void dispose() {
    _distanceController.dispose();
    _destinationController.dispose();
    super.dispose();
  }

  Future<void> _submitQuickTrip() async {
    if (!_formKey.currentState!.validate()) return;

    final distance = double.parse(_distanceController.text.trim());
    setState(() {
      _isSubmitting = true;
      _errorMessage = null;
    });

    try {
      final trip = await _repository.quickLogTrip(
        vehicleId: widget.vehicleId,
        distanceKm: distance,
        destinationName: _destinationController.text.trim().isNotEmpty ? _destinationController.text.trim() : 'Quick Destination',
        tripPurpose: _tripPurpose,
        organizationId: widget.organizationId,
      );

      if (mounted) {
        Navigator.pop(context, trip);
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _errorMessage = e.toString().replaceAll('Exception: ', '');
          _isSubmitting = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: VeltricsRadius.mdAll),
      title: Row(
        children: [
          Icon(Icons.directions_car, color: theme.colorScheme.primary),
          const SizedBox(width: 8),
          const Text('Quick-Log Trip', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        ],
      ),
      content: SingleChildScrollView(
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('UC-056 • 1-Tap Dashboard Trip Shortcut', style: VeltricsTextStyles.labelSm),
              const SizedBox(height: 12),

              if (_errorMessage != null) ...[
                Text(_errorMessage!, style: const TextStyle(color: VeltricsColors.errorLight, fontSize: 12)),
                const SizedBox(height: 8),
              ],

              TextFormField(
                controller: _distanceController,
                keyboardType: const TextInputType.numberWithOptions(decimal: true),
                autofocus: true,
                decoration: const InputDecoration(
                  labelText: 'Distance Traveled (km)',
                  prefixIcon: Icon(Icons.route),
                  suffixText: 'km',
                ),
                validator: (v) {
                  if (v == null || v.trim().isEmpty) return 'Enter trip distance';
                  final val = double.tryParse(v.trim());
                  if (val == null || val <= 0) return 'Distance must be > 0';
                  return null;
                },
              ),
              const SizedBox(height: 12),

              TextFormField(
                controller: _destinationController,
                decoration: const InputDecoration(
                  labelText: 'Destination (Optional)',
                  prefixIcon: Icon(Icons.location_on),
                  hintText: 'e.g. Client Office / Depot B',
                ),
              ),
              const SizedBox(height: 12),

              Row(
                children: [
                  Expanded(
                    child: ChoiceChip(
                      label: const Text('Business'),
                      avatar: const Icon(Icons.work, size: 16),
                      selected: _tripPurpose == 'BUSINESS',
                      onSelected: (sel) {
                        if (sel) setState(() => _tripPurpose = 'BUSINESS');
                      },
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: ChoiceChip(
                      label: const Text('Personal'),
                      avatar: const Icon(Icons.person, size: 16),
                      selected: _tripPurpose == 'PERSONAL',
                      onSelected: (sel) {
                        if (sel) setState(() => _tripPurpose = 'PERSONAL');
                      },
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('Cancel'),
        ),
        ElevatedButton(
          onPressed: _isSubmitting ? null : _submitQuickTrip,
          child: _isSubmitting
              ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
              : const Text('Save Quick Trip'),
        ),
      ],
    );
  }
}
