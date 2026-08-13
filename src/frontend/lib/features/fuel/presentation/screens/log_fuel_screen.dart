import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/fuel_repository.dart';
import '../../domain/fuel_log_model.dart';

class LogFuelScreen extends StatefulWidget {
  final String vehicleId;
  final String organizationId;
  final double currentOdometer;

  const LogFuelScreen({
    super.key,
    required this.vehicleId,
    required this.organizationId,
    this.currentOdometer = 0.0,
  });

  @override
  State<LogFuelScreen> createState() => _LogFuelScreenState();
}

class _LogFuelScreenState extends State<LogFuelScreen> {
  final _formKey = GlobalKey<FormState>();
  final FuelRepository _repository = FuelRepository();

  late TextEditingController _odometerController;
  late TextEditingController _litersController;
  late TextEditingController _costController;
  late TextEditingController _stationController;
  late TextEditingController _receiptPhotoController;

  String _selectedFuelType = 'Petrol';
  DateTime _selectedDate = DateTime.now();
  bool _isFullTank = true;
  bool _isSubmitting = false;

  final List<String> _fuelTypes = ['Petrol', 'Diesel', 'CNG', 'Hybrid', 'Electric'];

  @override
  void initState() {
    super.initState();
    _odometerController = TextEditingController(
      text: widget.currentOdometer > 0 ? widget.currentOdometer.toStringAsFixed(0) : '10000',
    );
    _litersController = TextEditingController(text: '35.0');
    _costController = TextEditingController(text: '9800');
    _stationController = TextEditingController(text: 'TotalParco / Shell');
    _receiptPhotoController = TextEditingController();
  }

  @override
  void dispose() {
    _odometerController.dispose();
    _litersController.dispose();
    _costController.dispose();
    _stationController.dispose();
    _receiptPhotoController.dispose();
    super.dispose();
  }

  Future<void> _submitFuelLog() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isSubmitting = true);

    try {
      final odometer = double.parse(_odometerController.text.trim());
      final liters = double.parse(_litersController.text.trim());
      final cost = double.parse(_costController.text.trim());

      final fuelLog = await _repository.createFuelLog(
        vehicleId: widget.vehicleId,
        organizationId: widget.organizationId,
        odometerKm: odometer,
        quantityLiters: liters,
        totalCost: cost,
        fuelType: _selectedFuelType,
        logDate: _selectedDate,
        isFullTank: _isFullTank,
        stationName: _stationController.text.trim().isNotEmpty ? _stationController.text.trim() : null,
        receiptPhotoUrl: _receiptPhotoController.text.trim().isNotEmpty ? _receiptPhotoController.text.trim() : null,
      );

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            fuelLog.calculatedEfficiencyKpl != null
                ? 'Fuel fill-up logged! Calculated efficiency: ${fuelLog.calculatedEfficiencyKpl!.toStringAsFixed(1)} km/L'
                : 'Fuel fill-up log saved successfully & expense created!',
          ),
          backgroundColor: VeltricsColors.successLight,
        ),
      );

      Navigator.of(context).pop(fuelLog);
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error: ${e.toString().replaceAll('Exception: ', '')}'),
          backgroundColor: VeltricsColors.errorLight,
        ),
      );
    } finally {
      if (mounted) setState(() => _isSubmitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Log Fuel Fill-Up', style: TextStyle(fontWeight: FontWeight.w700)),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: VeltricsSpacing.pagePadding.copyWith(top: 16, bottom: 24),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('SCR-FUEL-002 • Fuel Logging Entry', style: VeltricsTextStyles.labelSm),
              const SizedBox(height: 16),

              // Odometer Field
              TextFormField(
                controller: _odometerController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'Current Odometer (km)',
                  prefixIcon: const Icon(Icons.speed, color: VeltricsColors.warningLight),
                  border: OutlineInputBorder(borderRadius: VeltricsRadius.smAll),
                ),
                validator: (val) {
                  if (val == null || val.isEmpty) return 'Enter odometer reading';
                  final numVal = double.tryParse(val);
                  if (numVal == null || numVal < 0) return 'Enter valid odometer number';
                  if (widget.currentOdometer > 0 && numVal < widget.currentOdometer) {
                    return 'Odometer cannot be lower than current (${widget.currentOdometer.toStringAsFixed(0)} km)';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // Fuel Liters & Total Cost Row
              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: _litersController,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      decoration: InputDecoration(
                        labelText: 'Quantity (Liters)',
                        prefixIcon: const Icon(Icons.local_gas_station, color: VeltricsColors.infoLight),
                        border: OutlineInputBorder(borderRadius: VeltricsRadius.smAll),
                      ),
                      validator: (val) {
                        if (val == null || val.isEmpty) return 'Required';
                        final numVal = double.tryParse(val);
                        if (numVal == null || numVal <= 0) return 'Must be > 0';
                        return null;
                      },
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: TextFormField(
                      controller: _costController,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      decoration: InputDecoration(
                        labelText: 'Total Cost (PKR)',
                        prefixIcon: const Icon(Icons.attach_money, color: VeltricsColors.successLight),
                        border: OutlineInputBorder(borderRadius: VeltricsRadius.smAll),
                      ),
                      validator: (val) {
                        if (val == null || val.isEmpty) return 'Required';
                        final numVal = double.tryParse(val);
                        if (numVal == null || numVal <= 0) return 'Must be > 0';
                        return null;
                      },
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),

              // Fuel Type Dropdown
              DropdownButtonFormField<String>(
                value: _selectedFuelType,
                decoration: InputDecoration(
                  labelText: 'Fuel Category',
                  prefixIcon: const Icon(Icons.category),
                  border: OutlineInputBorder(borderRadius: VeltricsRadius.smAll),
                ),
                items: _fuelTypes.map((type) => DropdownMenuItem(value: type, child: Text(type))).toList(),
                onChanged: (val) {
                  if (val != null) setState(() => _selectedFuelType = val);
                },
              ),
              const SizedBox(height: 16),

              // Gas Station / Pump Name
              TextFormField(
                controller: _stationController,
                decoration: InputDecoration(
                  labelText: 'Fuel Station / Pump Name (Optional)',
                  prefixIcon: const Icon(Icons.place),
                  border: OutlineInputBorder(borderRadius: VeltricsRadius.smAll),
                ),
              ),
              const SizedBox(height: 16),

              // Full Tank Switch
              Container(
                decoration: BoxDecoration(
                  color: isDark ? VeltricsColors.neutralD100 : Colors.grey.shade50,
                  borderRadius: VeltricsRadius.smAll,
                  border: Border.all(
                    color: isDark ? VeltricsColors.neutralD300 : VeltricsColors.neutral200,
                  ),
                ),
                child: SwitchListTile(
                  title: Text('Full Tank Refill', style: VeltricsTextStyles.titleSm),
                  subtitle: Text('Enables km/L fuel efficiency calculation', style: VeltricsTextStyles.bodySm),
                  value: _isFullTank,
                  activeColor: VeltricsColors.successLight,
                  onChanged: (val) => setState(() => _isFullTank = val),
                ),
              ),
              const SizedBox(height: 24),

              // Submit Button
              SizedBox(
                width: double.infinity,
                height: 52,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: theme.colorScheme.primary,
                    shape: RoundedRectangleBorder(borderRadius: VeltricsRadius.pillAll),
                  ),
                  onPressed: _isSubmitting ? null : _submitFuelLog,
                  child: _isSubmitting
                      ? const CircularProgressIndicator(color: Colors.white)
                      : Text('Save Fuel Entry', style: VeltricsTextStyles.labelLg.copyWith(color: Colors.white)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
