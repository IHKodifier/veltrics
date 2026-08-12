import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/vehicle_repository.dart';
import '../../domain/vehicle_model.dart';

class EditVehicleScreen extends StatefulWidget {
  final VehicleDetailModel vehicle;

  const EditVehicleScreen({
    super.key,
    required this.vehicle,
  });

  @override
  State<EditVehicleScreen> createState() => _EditVehicleScreenState();
}

class _EditVehicleScreenState extends State<EditVehicleScreen> {
  final VehicleRepository _vehicleRepository = VehicleRepository();
  final _formKey = GlobalKey<FormState>();

  late TextEditingController _makeController;
  late TextEditingController _modelController;
  late TextEditingController _plateController;
  late TextEditingController _yearController;
  late TextEditingController _odometerController;
  late TextEditingController _photoUrlController;

  // Custom Specs Controllers
  late TextEditingController _engineCapacityController;
  late TextEditingController _tirePressureController;
  late TextEditingController _oilTypeController;

  late String _selectedFuelType;
  late String _selectedProvince;
  bool _isSaving = false;
  String? _errorMessage;

  final List<String> _fuelTypes = ["Petrol", "Diesel", "Hybrid", "EV", "CNG"];
  final List<String> _provinces = [
    "Punjab",
    "Sindh",
    "Khyber Pakhtunkhwa",
    "Balochistan",
    "ICT Islamabad",
    "Azad Kashmir",
    "Gilgit-Baltistan",
    "Other"
  ];

  @override
  void initState() {
    super.initState();
    final v = widget.vehicle;
    _makeController = TextEditingController(text: v.make);
    _modelController = TextEditingController(text: v.model);
    _plateController = TextEditingController(text: v.licensePlate);
    _yearController = TextEditingController(text: v.year.toString());
    _odometerController = TextEditingController(text: v.currentOdometerKm.toStringAsFixed(0));
    _photoUrlController = TextEditingController(text: v.photoUrl ?? '');

    final specs = v.customSpecs;
    _engineCapacityController = TextEditingController(
      text: specs['engine_capacity_cc']?.toString() ?? '',
    );
    _tirePressureController = TextEditingController(
      text: specs['tire_pressure_psi']?.toString() ?? '',
    );
    _oilTypeController = TextEditingController(
      text: specs['oil_type']?.toString() ?? '',
    );

    _selectedFuelType = _fuelTypes.contains(v.fuelType) ? v.fuelType : "Petrol";
    _selectedProvince = _provinces.contains(v.registrationProvince) ? v.registrationProvince : "Punjab";
  }

  @override
  void dispose() {
    _makeController.dispose();
    _modelController.dispose();
    _plateController.dispose();
    _yearController.dispose();
    _odometerController.dispose();
    _photoUrlController.dispose();
    _engineCapacityController.dispose();
    _tirePressureController.dispose();
    _oilTypeController.dispose();
    super.dispose();
  }

  Future<void> _handleSave() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isSaving = true;
      _errorMessage = null;
    });

    try {
      final double odometer = double.parse(_odometerController.text.trim());
      final int year = int.parse(_yearController.text.trim());

      final Map<String, dynamic> customSpecs = Map<String, dynamic>.from(widget.vehicle.customSpecs);

      if (_engineCapacityController.text.trim().isNotEmpty) {
        customSpecs['engine_capacity_cc'] = int.tryParse(_engineCapacityController.text.trim()) ??
            double.tryParse(_engineCapacityController.text.trim());
      }
      if (_tirePressureController.text.trim().isNotEmpty) {
        customSpecs['tire_pressure_psi'] = int.tryParse(_tirePressureController.text.trim()) ??
            double.tryParse(_tirePressureController.text.trim());
      }
      if (_oilTypeController.text.trim().isNotEmpty) {
        customSpecs['oil_type'] = _oilTypeController.text.trim();
      }

      await _vehicleRepository.updateVehicle(
        vehicleId: widget.vehicle.id,
        organizationId: widget.vehicle.organizationId,
        licensePlate: _plateController.text.trim(),
        registrationProvince: _selectedProvince,
        make: _makeController.text.trim(),
        model: _modelController.text.trim(),
        year: year,
        fuelType: _selectedFuelType,
        currentOdometerKm: odometer,
        photoUrl: _photoUrlController.text.trim().isEmpty ? null : _photoUrlController.text.trim(),
        customSpecs: customSpecs,
      );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("Vehicle updated successfully!"),
            backgroundColor: VeltricsColors.successLight,
          ),
        );
        Navigator.pop(context, true);
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _errorMessage = e.toString().replaceAll("Exception: ", "");
          _isSaving = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Edit Vehicle Specifications'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20.0),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                if (_errorMessage != null) ...[
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: VeltricsColors.errorLight.withAlpha(25),
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: VeltricsColors.errorLight),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.error_outline, color: VeltricsColors.errorLight),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            _errorMessage!,
                            style: const TextStyle(color: VeltricsColors.errorLight, fontSize: 13),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 20),
                ],

                // Section 1: Registration Details
                Text(
                  "Registration Details",
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _plateController,
                  decoration: const InputDecoration(
                    labelText: "License Plate *",
                    hintText: "e.g. LEA-1027",
                    prefixIcon: Icon(Icons.pin),
                    filled: true,
                  ),
                  textCapitalization: TextCapitalization.characters,
                  validator: (value) {
                    if (value == null || value.trim().isEmpty) {
                      return "License plate is required";
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 14),
                DropdownButtonFormField<String>(
                  initialValue: _selectedProvince,
                  decoration: const InputDecoration(
                    labelText: "Registration Province / Territory *",
                    prefixIcon: Icon(Icons.map_outlined),
                    filled: true,
                  ),
                  items: _provinces.map((province) {
                    return DropdownMenuItem(
                      value: province,
                      child: Text(province),
                    );
                  }).toList(),
                  onChanged: (val) {
                    if (val != null) setState(() => _selectedProvince = val);
                  },
                ),

                const SizedBox(height: 24),

                // Section 2: Vehicle Identity & Specs
                Text(
                  "Vehicle Identity",
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 12),
                Row(
                  children: [
                    Expanded(
                      child: TextFormField(
                        controller: _makeController,
                        decoration: const InputDecoration(
                          labelText: "Make *",
                          hintText: "e.g. Honda",
                          filled: true,
                        ),
                        validator: (v) => (v == null || v.trim().isEmpty) ? "Required" : null,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: TextFormField(
                        controller: _modelController,
                        decoration: const InputDecoration(
                          labelText: "Model *",
                          hintText: "e.g. Civic",
                          filled: true,
                        ),
                        validator: (v) => (v == null || v.trim().isEmpty) ? "Required" : null,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 14),
                Row(
                  children: [
                    Expanded(
                      child: TextFormField(
                        controller: _yearController,
                        keyboardType: TextInputType.number,
                        decoration: const InputDecoration(
                          labelText: "Year *",
                          hintText: "e.g. 2023",
                          filled: true,
                        ),
                        validator: (v) {
                          if (v == null || v.trim().isEmpty) return "Required";
                          final yr = int.tryParse(v.trim());
                          if (yr == null || yr < 1950 || yr > 2030) return "Invalid year";
                          return null;
                        },
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: DropdownButtonFormField<String>(
                        initialValue: _selectedFuelType,
                        decoration: const InputDecoration(
                          labelText: "Fuel Type *",
                          filled: true,
                        ),
                        items: _fuelTypes.map((fuel) {
                          return DropdownMenuItem(
                            value: fuel,
                            child: Text(fuel),
                          );
                        }).toList(),
                        onChanged: (val) {
                          if (val != null) setState(() => _selectedFuelType = val);
                        },
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 24),

                // Section 3: Telematics & Specifications
                Text(
                  "Odometer & Technical Specs",
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _odometerController,
                  keyboardType: const TextInputType.numberWithOptions(decimal: true),
                  decoration: InputDecoration(
                    labelText: "Current Odometer (km) *",
                    hintText: "e.g. 18500",
                    prefixIcon: const Icon(Icons.speed),
                    helperText: "Initial odometer was ${widget.vehicle.initialOdometerKm.toStringAsFixed(0)} km",
                    filled: true,
                  ),
                  validator: (v) {
                    if (v == null || v.trim().isEmpty) return "Odometer reading is required";
                    final odo = double.tryParse(v.trim());
                    if (odo == null || odo < 0) return "Must be a valid positive number";
                    return null;
                  },
                ),
                const SizedBox(height: 14),
                Row(
                  children: [
                    Expanded(
                      child: TextFormField(
                        controller: _engineCapacityController,
                        keyboardType: TextInputType.number,
                        decoration: const InputDecoration(
                          labelText: "Engine Size (cc)",
                          hintText: "e.g. 1500",
                          filled: true,
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: TextFormField(
                        controller: _tirePressureController,
                        keyboardType: TextInputType.number,
                        decoration: const InputDecoration(
                          labelText: "Tire Spec (PSI)",
                          hintText: "e.g. 32",
                          filled: true,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 14),
                TextFormField(
                  controller: _oilTypeController,
                  decoration: const InputDecoration(
                    labelText: "Recommended Oil Type",
                    hintText: "e.g. 0W-20 Synthetic",
                    prefixIcon: Icon(Icons.oil_barrel_outlined),
                    filled: true,
                  ),
                ),
                const SizedBox(height: 14),
                TextFormField(
                  controller: _photoUrlController,
                  decoration: const InputDecoration(
                    labelText: "Vehicle Photo URL (Optional)",
                    hintText: "https://...",
                    prefixIcon: Icon(Icons.image_outlined),
                    filled: true,
                  ),
                ),

                const SizedBox(height: 32),

                // Submit Button
                ElevatedButton(
                  onPressed: _isSaving ? null : _handleSave,
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    backgroundColor: theme.colorScheme.primary,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: _isSaving
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2.5,
                            color: Colors.white,
                          ),
                        )
                      : const Text(
                          "Save Vehicle Specification Updates",
                          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
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
