import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/trip_repository.dart';

class LogTripScreen extends StatefulWidget {
  final String vehicleId;
  final String organizationId;
  final double currentOdometer;

  const LogTripScreen({
    super.key,
    required this.vehicleId,
    required this.organizationId,
    this.currentOdometer = 0.0,
  });

  @override
  State<LogTripScreen> createState() => _LogTripScreenState();
}

class _LogTripScreenState extends State<LogTripScreen> {
  final _formKey = GlobalKey<FormState>();
  final TripRepository _repository = TripRepository();

  late TextEditingController _startOdometerController;
  late TextEditingController _endOdometerController;
  final TextEditingController _originController = TextEditingController();
  final TextEditingController _destinationController = TextEditingController();
  final TextEditingController _notesController = TextEditingController();

  String _tripPurpose = 'BUSINESS';
  bool _isSubmitting = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _startOdometerController = TextEditingController(text: widget.currentOdometer.toStringAsFixed(0));
    _endOdometerController = TextEditingController(text: (widget.currentOdometer + 10.0).toStringAsFixed(0));
  }

  @override
  void dispose() {
    _startOdometerController.dispose();
    _endOdometerController.dispose();
    _originController.dispose();
    _destinationController.dispose();
    _notesController.dispose();
    super.dispose();
  }

  Future<void> _submitTripLog() async {
    if (!_formKey.currentState!.validate()) return;

    final startOdo = double.parse(_startOdometerController.text.trim());
    final endOdo = double.parse(_endOdometerController.text.trim());

    if (endOdo < startOdo) {
      setState(() {
        _errorMessage = 'End odometer ($endOdo km) must be greater than or equal to start odometer ($startOdo km).';
      });
      return;
    }

    setState(() {
      _isSubmitting = true;
      _errorMessage = null;
    });

    try {
      final trip = await _repository.logManualTrip(
        vehicleId: widget.vehicleId,
        startOdometerKm: startOdo,
        endOdometerKm: endOdo,
        originName: _originController.text.trim().isNotEmpty ? _originController.text.trim() : null,
        destinationName: _destinationController.text.trim().isNotEmpty ? _destinationController.text.trim() : null,
        tripPurpose: _tripPurpose,
        notes: _notesController.text.trim().isNotEmpty ? _notesController.text.trim() : null,
        organizationId: widget.organizationId,
      );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Trip logged successfully (+${trip.distanceKm?.toStringAsFixed(1)} km)'),
            backgroundColor: VeltricsColors.successLight,
          ),
        );
        Navigator.pop(context, trip);
      }
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll('Exception: ', '');
        _isSubmitting = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Log Manual Trip', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: VeltricsSpacing.pagePadding,
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('SCR-TRIP-003 • Trip Recording Entry', style: VeltricsTextStyles.labelSm),
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

                // 1. Trip Purpose Selector
                Card(
                  child: Padding(
                    padding: VeltricsSpacing.cardPaddingMobile,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('TRIP PURPOSE / CLASSIFICATION', style: VeltricsTextStyles.labelSm),
                        const SizedBox(height: 8),
                        Row(
                          children: [
                            Expanded(
                              child: ChoiceChip(
                                label: const Center(child: Text('Business Trip')),
                                selected: _tripPurpose == 'BUSINESS',
                                onSelected: (sel) {
                                  if (sel) setState(() => _tripPurpose = 'BUSINESS');
                                },
                              ),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: ChoiceChip(
                                label: const Center(child: Text('Personal Trip')),
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
                const SizedBox(height: 16),

                // 2. Odometer Readings Card
                Card(
                  child: Padding(
                    padding: VeltricsSpacing.cardPaddingMobile,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('ODOMETER READINGS (KM)', style: VeltricsTextStyles.labelSm),
                        const SizedBox(height: 12),
                        Row(
                          children: [
                            Expanded(
                              child: TextFormField(
                                controller: _startOdometerController,
                                keyboardType: const TextInputType.numberWithOptions(decimal: true),
                                decoration: const InputDecoration(
                                  labelText: 'Start Odometer (km)',
                                  prefixIcon: Icon(Icons.speed),
                                ),
                                validator: (v) {
                                  if (v == null || v.trim().isEmpty) return 'Required';
                                  if (double.tryParse(v.trim()) == null) return 'Invalid number';
                                  return null;
                                },
                              ),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: TextFormField(
                                controller: _endOdometerController,
                                keyboardType: const TextInputType.numberWithOptions(decimal: true),
                                decoration: const InputDecoration(
                                  labelText: 'End Odometer (km)',
                                  prefixIcon: Icon(Icons.flag_outlined),
                                ),
                                validator: (v) {
                                  if (v == null || v.trim().isEmpty) return 'Required';
                                  if (double.tryParse(v.trim()) == null) return 'Invalid number';
                                  return null;
                                },
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // 3. Locations Card
                Card(
                  child: Padding(
                    padding: VeltricsSpacing.cardPaddingMobile,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('ORIGIN & DESTINATION', style: VeltricsTextStyles.labelSm),
                        const SizedBox(height: 12),
                        TextFormField(
                          controller: _originController,
                          decoration: const InputDecoration(
                            labelText: 'Start Location / Origin Name',
                            prefixIcon: Icon(Icons.trip_origin),
                            hintText: 'e.g. Lahore Head Office',
                          ),
                        ),
                        const SizedBox(height: 12),
                        TextFormField(
                          controller: _destinationController,
                          decoration: const InputDecoration(
                            labelText: 'Destination Name',
                            prefixIcon: Icon(Icons.place_outlined),
                            hintText: 'e.g. Islamabad Depot',
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // 4. Notes & Details
                TextFormField(
                  controller: _notesController,
                  maxLines: 2,
                  decoration: const InputDecoration(
                    labelText: 'Notes / Purpose Details (Optional)',
                    prefixIcon: Icon(Icons.notes),
                    hintText: 'e.g. Client delivery & site audit',
                  ),
                ),
                const SizedBox(height: 24),

                // Submit Button
                SizedBox(
                  width: double.infinity,
                  height: 48,
                  child: ElevatedButton(
                    onPressed: _isSubmitting ? null : _submitTripLog,
                    child: _isSubmitting
                        ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                        : const Text('Save & Submit Trip Record', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                  ),
                ),
                const SizedBox(height: 24),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
