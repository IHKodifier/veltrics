import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/vehicle_repository.dart';
import '../../domain/vehicle_model.dart';

class AddVehicleScreen extends StatefulWidget {
  final String organizationId;

  const AddVehicleScreen({
    super.key,
    this.organizationId = "org-demo-101",
  });

  @override
  State<AddVehicleScreen> createState() => _AddVehicleScreenState();
}

class _AddVehicleScreenState extends State<AddVehicleScreen> {
  final VehicleRepository _vehicleRepository = VehicleRepository();
  final _formKey = GlobalKey<FormState>();

  final TextEditingController _makeController = TextEditingController();
  final TextEditingController _modelController = TextEditingController();
  final TextEditingController _plateController = TextEditingController(text: "AFR-024");
  final TextEditingController _yearController = TextEditingController(text: "2024");
  final TextEditingController _odometerController = TextEditingController(text: "15000");
  final TextEditingController _photoUrlController = TextEditingController();

  String _selectedFuelType = "Petrol";
  String _selectedProvince = "Punjab";
  bool _isLoading = false;
  bool _isSearchingMakes = false;
  bool _isSearchingModels = false;
  String? _errorMessage;
  VehicleModel? _createdVehicle;

  List<String> _makeSuggestions = [];
  List<VehicleTypeModel> _modelSuggestions = [];

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

  Future<void> _onMakeChanged(String query) async {
    if (query.trim().isEmpty) {
      setState(() {
        _makeSuggestions = [];
      });
      return;
    }

    setState(() {
      _isSearchingMakes = true;
    });

    try {
      final results = await _vehicleRepository.searchVehicleTypes(query: query);
      final uniqueMakes = results.map((e) => e.make).toSet().toList();
      setState(() {
        _makeSuggestions = uniqueMakes;
        _isSearchingMakes = false;
      });
    } catch (_) {
      setState(() {
        _isSearchingMakes = false;
      });
    }
  }

  Future<void> _onModelChanged(String query) async {
    final currentMake = _makeController.text.trim();

    setState(() {
      _isSearchingModels = true;
    });

    try {
      final results = await _vehicleRepository.searchVehicleTypes(
        make: currentMake.isNotEmpty ? currentMake : null,
        query: query.isNotEmpty ? query : null,
      );
      setState(() {
        _modelSuggestions = results;
        _isSearchingModels = false;
      });
    } catch (_) {
      setState(() {
        _isSearchingModels = false;
      });
    }
  }

  void _selectMake(String make) {
    setState(() {
      _makeController.text = make;
      _makeSuggestions = [];
    });
    _onModelChanged("");
  }

  void _selectModel(VehicleTypeModel item) {
    setState(() {
      _makeController.text = item.make;
      _modelController.text = item.model;
      _selectedFuelType = item.defaultFuelType;
      _modelSuggestions = [];
    });
  }

  Future<void> _submitVehicleForm() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final vehicle = await _vehicleRepository.createVehicle(
        organizationId: widget.organizationId,
        licensePlate: _plateController.text.trim(),
        registrationProvince: _selectedProvince,
        make: _makeController.text.trim(),
        model: _modelController.text.trim(),
        year: int.parse(_yearController.text.trim()),
        fuelType: _selectedFuelType,
        initialOdometerKm: double.parse(_odometerController.text.trim()),
        photoUrl: _photoUrlController.text.trim().isNotEmpty ? _photoUrlController.text.trim() : null,
      );

      setState(() {
        _createdVehicle = vehicle;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll("Exception: ", "");
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Register New Vehicle'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: VeltricsSpacing.pagePadding,
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: VeltricsSpacing.sm),
                Text(
                  "Add Vehicle to Fleet",
                  style: VeltricsTextStyles.titleLg,
                ),
                Text(
                  "Select Province/Region and enter Pakistani License Plate details.",
                  style: VeltricsTextStyles.bodyMd.copyWith(
                    color: isDark ? VeltricsColors.neutralD500 : VeltricsColors.neutral500,
                  ),
                ),
                const SizedBox(height: VeltricsSpacing.md),

                // Make Input Field (Typeahead for Makes)
                TextFormField(
                  controller: _makeController,
                  decoration: InputDecoration(
                    labelText: "Make (e.g. Toyota, Honda, Suzuki)",
                    prefixIcon: const Icon(Icons.directions_car),
                    suffixIcon: _isSearchingMakes
                        ? const Padding(
                            padding: EdgeInsets.all(12),
                            child: SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2)),
                          )
                        : const Icon(Icons.search),
                  ),
                  onChanged: _onMakeChanged,
                  validator: (v) => v == null || v.trim().isEmpty ? "Make is required" : null,
                ),

                // Make Suggestions Cards
                if (_makeSuggestions.isNotEmpty) ...[
                  Card(
                    color: isDark ? VeltricsColors.neutralD100 : Colors.white,
                    margin: const EdgeInsets.only(top: 4, bottom: 8),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                          child: Text(
                            "Select Make (Limits Model choices):",
                            style: VeltricsTextStyles.labelSm.copyWith(color: theme.colorScheme.primary),
                          ),
                        ),
                        const Divider(height: 1),
                        Wrap(
                          spacing: 8,
                          runSpacing: 4,
                          children: _makeSuggestions.map((make) {
                            return Padding(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                              child: ChoiceChip(
                                label: Text(make),
                                selected: _makeController.text == make,
                                onSelected: (_) => _selectMake(make),
                              ),
                            );
                          }).toList(),
                        ),
                      ],
                    ),
                  ),
                ],

                const SizedBox(height: VeltricsSpacing.sm),

                // Model Input Field (Typeahead for Models matching selected Make)
                TextFormField(
                  controller: _modelController,
                  decoration: InputDecoration(
                    labelText: "Model (e.g. Corolla, Civic, Alto)",
                    prefixIcon: const Icon(Icons.directions_car_outlined),
                    suffixIcon: _isSearchingModels
                        ? const Padding(
                            padding: EdgeInsets.all(12),
                            child: SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2)),
                          )
                        : null,
                  ),
                  onTap: () => _onModelChanged(_modelController.text),
                  onChanged: _onModelChanged,
                  validator: (v) => v == null || v.trim().isEmpty ? "Model is required" : null,
                ),

                // Model Suggestions List Card
                if (_modelSuggestions.isNotEmpty) ...[
                  Card(
                    color: isDark ? VeltricsColors.neutralD100 : Colors.white,
                    margin: const EdgeInsets.only(top: 4, bottom: 8),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                          child: Text(
                            "Matching Models for '${_makeController.text.isEmpty ? 'All Makes' : _makeController.text}' (Tap to Autocomplete):",
                            style: VeltricsTextStyles.labelSm.copyWith(color: theme.colorScheme.primary),
                          ),
                        ),
                        const Divider(height: 1),
                        ..._modelSuggestions.map((item) {
                          return ListTile(
                            dense: true,
                            leading: Icon(Icons.auto_awesome, size: 18, color: theme.colorScheme.primary),
                            title: Text("${item.make} ${item.model}", style: VeltricsTextStyles.titleSm),
                            subtitle: Text("${item.category} • ${item.defaultFuelType} • Oil Change @ ${item.recommendedOilIntervalKm} km"),
                            trailing: const Icon(Icons.arrow_forward_ios, size: 12),
                            onTap: () => _selectModel(item),
                          );
                        }),
                      ],
                    ),
                  ),
                ],

                const SizedBox(height: VeltricsSpacing.sm),

                // Registration Province & License Plate Row
                Row(
                  children: [
                    Expanded(
                      flex: 5,
                      child: DropdownButtonFormField<String>(
                        initialValue: _selectedProvince,
                        decoration: const InputDecoration(
                          labelText: "Registration Region",
                          prefixIcon: Icon(Icons.map_outlined),
                        ),
                        items: _provinces.map((prov) {
                          return DropdownMenuItem(value: prov, child: Text(prov));
                        }).toList(),
                        onChanged: (val) {
                          if (val != null) setState(() => _selectedProvince = val);
                        },
                      ),
                    ),
                    const SizedBox(width: VeltricsSpacing.xs3),
                    Expanded(
                      flex: 5,
                      child: TextFormField(
                        controller: _plateController,
                        decoration: const InputDecoration(
                          labelText: "Plate No. (e.g. AFR-024)",
                          prefixIcon: Icon(Icons.badge_outlined),
                        ),
                        onChanged: (_) => setState(() {}),
                        validator: (v) => v == null || v.trim().isEmpty ? "Plate required" : null,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: VeltricsSpacing.sm),

                // Live Pakistani License Plate Preview Widget
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                  decoration: BoxDecoration(
                    color: isDark ? const Color(0xFF1E262B) : const Color(0xFFF1F5F9),
                    borderRadius: VeltricsRadius.smAll,
                    border: Border.all(color: Colors.grey.shade400, width: 1.5),
                  ),
                  child: Row(
                    children: [
                      // Province Stripe Badge
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
                        decoration: BoxDecoration(
                          color: _selectedProvince == "Punjab"
                              ? const Color(0xFF15803D)
                              : _selectedProvince == "Sindh"
                                  ? const Color(0xFFB91C1C)
                                  : _selectedProvince == "ICT Islamabad"
                                      ? const Color(0xFF1D4ED8)
                                      : const Color(0xFF0F172A),
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(
                          _selectedProvince.toUpperCase(),
                          style: const TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 12,
                            letterSpacing: 1.1,
                          ),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              "REGISTRATION PLATE PREVIEW",
                              style: TextStyle(
                                fontSize: 9,
                                fontWeight: FontWeight.w600,
                                color: isDark ? Colors.grey.shade400 : Colors.grey.shade600,
                                letterSpacing: 1.0,
                              ),
                            ),
                            Text(
                              _plateController.text.isEmpty ? "AFR-024" : _plateController.text.toUpperCase(),
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.w900,
                                letterSpacing: 2.0,
                                color: isDark ? Colors.white : Colors.black87,
                                fontFamily: 'monospace',
                              ),
                            ),
                          ],
                        ),
                      ),
                      const Icon(Icons.verified_outlined, color: Colors.green, size: 24),
                    ],
                  ),
                ),
                const SizedBox(height: VeltricsSpacing.sm),

                Row(
                  children: [
                    Expanded(
                      child: DropdownButtonFormField<String>(
                        initialValue: _selectedFuelType,
                        decoration: const InputDecoration(
                          labelText: "Fuel Type",
                          prefixIcon: Icon(Icons.local_gas_station_outlined),
                        ),
                        items: _fuelTypes.map((fuel) {
                          return DropdownMenuItem(value: fuel, child: Text(fuel));
                        }).toList(),
                        onChanged: (val) {
                          if (val != null) setState(() => _selectedFuelType = val);
                        },
                      ),
                    ),
                    const SizedBox(width: VeltricsSpacing.xs3),
                    Expanded(
                      child: TextFormField(
                        controller: _yearController,
                        keyboardType: TextInputType.number,
                        decoration: const InputDecoration(
                          labelText: "Year",
                          prefixIcon: Icon(Icons.calendar_today),
                        ),
                        validator: (v) => v == null || v.trim().isEmpty ? "Year required" : null,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: VeltricsSpacing.sm),

                Row(
                  children: [
                    Expanded(
                      child: TextFormField(
                        controller: _odometerController,
                        keyboardType: TextInputType.number,
                        decoration: const InputDecoration(
                          labelText: "Odometer (km)",
                          prefixIcon: Icon(Icons.speed),
                        ),
                        validator: (v) => v == null || v.trim().isEmpty ? "Odometer required" : null,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: VeltricsSpacing.sm),

                TextFormField(
                  controller: _photoUrlController,
                  decoration: const InputDecoration(
                    labelText: "Vehicle Photo URL (Optional)",
                    prefixIcon: Icon(Icons.image_outlined),
                  ),
                ),
                const SizedBox(height: VeltricsSpacing.md),

                if (_errorMessage != null) ...[
                  Container(
                    padding: const EdgeInsets.all(VeltricsSpacing.xs3),
                    decoration: BoxDecoration(
                      color: VeltricsColors.errorBgLight,
                      borderRadius: VeltricsRadius.smAll,
                    ),
                    child: Text(
                      _errorMessage!,
                      style: VeltricsTextStyles.bodySm.copyWith(color: VeltricsColors.errorLight),
                    ),
                  ),
                  const SizedBox(height: VeltricsSpacing.md),
                ],

                ElevatedButton.icon(
                  onPressed: _isLoading ? null : _submitVehicleForm,
                  icon: _isLoading
                      ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2.5))
                      : const Icon(Icons.add_rounded),
                  label: Text(_isLoading ? "Saving Vehicle..." : "Save Vehicle"),
                ),
                const SizedBox(height: VeltricsSpacing.md),

                if (_createdVehicle != null) ...[
                  Card(
                    child: Padding(
                      padding: VeltricsSpacing.cardPaddingMobile,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                "${_createdVehicle!.make} ${_createdVehicle!.model} (${_createdVehicle!.year})",
                                style: VeltricsTextStyles.titleLg,
                              ),
                              VeltricsStatusPill.healthy(),
                            ],
                          ),
                          const SizedBox(height: VeltricsSpacing.xs2),
                          Text("Region: ${_createdVehicle!.registrationProvince}", style: VeltricsTextStyles.bodyLg),
                          Text("Plate: ${_createdVehicle!.licensePlate}", style: VeltricsTextStyles.bodyLg),
                          Text("Odometer: ${_createdVehicle!.currentOdometerKm} km", style: VeltricsTextStyles.bodyMd),
                          Text("Fuel: ${_createdVehicle!.fuelType}", style: VeltricsTextStyles.bodyMd),
                          const SizedBox(height: VeltricsSpacing.xs3),
                          Text(
                            "Vehicle ID: ${_createdVehicle!.id}",
                            style: VeltricsTextStyles.bodySm.copyWith(color: theme.colorScheme.primary),
                          ),
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
}
