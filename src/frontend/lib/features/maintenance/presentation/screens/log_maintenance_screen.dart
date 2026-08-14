import 'package:flutter/material.dart';

import '../../../../theme/app_theme.dart';
import '../../data/maintenance_repository.dart';
import '../../domain/maintenance_model.dart';

class LogMaintenanceScreen extends StatefulWidget {
  final String vehicleId;
  final String organizationId;
  final double currentOdometer;
  final MaintenanceScheduleModel? schedule;

  const LogMaintenanceScreen({
    super.key,
    required this.vehicleId,
    required this.organizationId,
    this.currentOdometer = 0.0,
    this.schedule,
  });

  @override
  State<LogMaintenanceScreen> createState() => _LogMaintenanceScreenState();
}

class _LogMaintenanceScreenState extends State<LogMaintenanceScreen> {
  final _formKey = GlobalKey<FormState>();
  final MaintenanceRepository _repository = MaintenanceRepository();

  late TextEditingController _serviceTypeController;
  late TextEditingController _costController;
  late TextEditingController _odometerController;
  late TextEditingController _providerController;
  late TextEditingController _notesController;

  DateTime _selectedDate = DateTime.now();
  bool _isSubmitting = false;

  final List<String> _commonServices = [
    'Engine Oil & Filter Change',
    'Air Filter Replacement',
    'Tire Rotation & Wheel Balancing',
    'Brake Pad Inspection & Service',
    'Transmission Fluid Service',
    'Spark Plug Replacement',
    'Battery & Electrical Check',
    'AC Filter & Gas Topup',
    'General Tuning & Inspection',
  ];

  @override
  void initState() {
    super.initState();
    final initialService = widget.schedule?.taskName ?? _commonServices.first;
    _serviceTypeController = TextEditingController(text: initialService);
    _costController = TextEditingController(text: '5000');
    _odometerController = TextEditingController(
      text: widget.currentOdometer > 0
          ? widget.currentOdometer.toStringAsFixed(0)
          : '10000',
    );
    _providerController = TextEditingController(text: 'Toyota Authorized Service');
    _notesController = TextEditingController();
  }

  @override
  void dispose() {
    _serviceTypeController.dispose();
    _costController.dispose();
    _odometerController.dispose();
    _providerController.dispose();
    _notesController.dispose();
    super.dispose();
  }

  Future<void> _pickDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate,
      firstDate: DateTime(2020),
      lastDate: DateTime.now().add(const Duration(days: 1)),
    );
    if (picked != null) {
      setState(() {
        _selectedDate = picked;
      });
    }
  }

  Future<void> _submitForm() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isSubmitting = true;
    });

    final cost = double.tryParse(_costController.text.trim()) ?? 0.0;
    final odo = double.tryParse(_odometerController.text.trim()) ?? 0.0;

    final payload = <String, dynamic>{
      'vehicle_id': widget.vehicleId,
      'maintenance_schedule_id': widget.schedule?.id,
      'service_type': _serviceTypeController.text.trim(),
      'cost': cost,
      'service_date': _selectedDate.toIso8601String().split('T').first,
      'odometer_reading': odo,
      'service_provider_name': _providerController.text.trim().isNotEmpty
          ? _providerController.text.trim()
          : null,
      'notes': _notesController.text.trim().isNotEmpty
          ? _notesController.text.trim()
          : null,
    };

    try {
      await _repository.logMaintenance(
        payload: payload,
        organizationId: widget.organizationId,
      );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Maintenance record logged successfully!'),
            backgroundColor: VeltricsColors.successLight,
          ),
        );
        Navigator.pop(context, true);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to log service: ${e.toString().replaceAll('Exception: ', '')}'),
            backgroundColor: VeltricsColors.errorLight,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isSubmitting = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Log Maintenance Task'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: VeltricsSpacing.pagePadding,
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (widget.schedule != null) ...[
                  Card(
                    color: isDark ? VeltricsColors.neutralD800 : theme.colorScheme.primaryContainer,
                    child: Padding(
                      padding: VeltricsSpacing.cardPaddingMobile,
                      child: Row(
                        children: [
                          Icon(Icons.stars, color: theme.colorScheme.primary),
                          const SizedBox(width: VeltricsSpacing.xs2),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text('LINKED SCHEDULE ITEM', style: VeltricsTextStyles.labelSm),
                                Text(widget.schedule!.taskName, style: VeltricsTextStyles.titleSm),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: VeltricsSpacing.sm),
                ],

                Text('Service Details', style: VeltricsTextStyles.titleLg),
                const SizedBox(height: VeltricsSpacing.xs2),

                // Service Type Dropdown/Input
                DropdownButtonFormField<String>(
                  initialValue: _commonServices.contains(_serviceTypeController.text)
                      ? _serviceTypeController.text
                      : null,
                  decoration: const InputDecoration(
                    labelText: 'Service Task Type *',
                    prefixIcon: Icon(Icons.build_outlined),
                  ),
                  items: _commonServices
                      .map((s) => DropdownMenuItem(value: s, child: Text(s)))
                      .toList(),
                  onChanged: (val) {
                    if (val != null) {
                      setState(() {
                        _serviceTypeController.text = val;
                      });
                    }
                  },
                  validator: (val) {
                    if (_serviceTypeController.text.trim().isEmpty) {
                      return 'Service type is required';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: VeltricsSpacing.sm),

                // Total Cost Input
                TextFormField(
                  controller: _costController,
                  keyboardType: const TextInputType.numberWithOptions(decimal: true),
                  decoration: const InputDecoration(
                    labelText: 'Total Cost (PKR) *',
                    prefixIcon: Icon(Icons.payments_outlined),
                  ),
                  validator: (val) {
                    if (val == null || val.trim().isEmpty) {
                      return 'Cost is required';
                    }
                    final numCost = double.tryParse(val.trim());
                    if (numCost == null) {
                      return 'Enter a valid cost number';
                    }
                    if (numCost < 0) {
                      return 'Cost cannot be negative';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: VeltricsSpacing.sm),

                // Odometer Reading Input
                TextFormField(
                  controller: _odometerController,
                  keyboardType: const TextInputType.numberWithOptions(decimal: true),
                  decoration: const InputDecoration(
                    labelText: 'Odometer Reading (km) *',
                    prefixIcon: Icon(Icons.speed_outlined),
                  ),
                  validator: (val) {
                    if (val == null || val.trim().isEmpty) {
                      return 'Odometer reading is required';
                    }
                    final numOdo = double.tryParse(val.trim());
                    if (numOdo == null) {
                      return 'Enter a valid odometer number';
                    }
                    if (numOdo < 0) {
                      return 'Odometer reading cannot be negative';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: VeltricsSpacing.sm),

                // Service Date Picker
                InkWell(
                  onTap: _pickDate,
                  borderRadius: VeltricsRadius.smAll,
                  child: InputDecorator(
                    decoration: const InputDecoration(
                      labelText: 'Service Date *',
                      prefixIcon: Icon(Icons.calendar_today_outlined),
                    ),
                    child: Text(
                      '${_selectedDate.year}-${_selectedDate.month.toString().padLeft(2, '0')}-${_selectedDate.day.toString().padLeft(2, '0')}',
                      style: VeltricsTextStyles.bodyLg,
                    ),
                  ),
                ),
                const SizedBox(height: VeltricsSpacing.sm),

                // Provider / Service Center
                TextFormField(
                  controller: _providerController,
                  decoration: const InputDecoration(
                    labelText: 'Service Provider / Workshop Name',
                    prefixIcon: Icon(Icons.storefront_outlined),
                  ),
                ),
                const SizedBox(height: VeltricsSpacing.sm),

                // Notes
                TextFormField(
                  controller: _notesController,
                  maxLines: 3,
                  decoration: const InputDecoration(
                    labelText: 'Service Notes / Parts Replaced',
                    prefixIcon: Icon(Icons.notes_outlined),
                  ),
                ),
                const SizedBox(height: VeltricsSpacing.lg),

                // Submit Button
                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: ElevatedButton.icon(
                    onPressed: _isSubmitting ? null : _submitForm,
                    icon: _isSubmitting
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                          )
                        : const Icon(Icons.save_outlined),
                    label: Text(_isSubmitting ? 'Saving Record...' : 'Log Service Record'),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
