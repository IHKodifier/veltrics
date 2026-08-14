import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/vehicle_repository.dart';
import '../../domain/vehicle_model.dart';
import 'add_vehicle_screen.dart';
import 'vehicle_detail_screen.dart';


class VehicleListScreen extends StatefulWidget {
  final String organizationId;

  const VehicleListScreen({
    super.key,
    this.organizationId = "org-demo-101",
  });

  @override
  State<VehicleListScreen> createState() => _VehicleListScreenState();
}

class _VehicleListScreenState extends State<VehicleListScreen> {
  final VehicleRepository _vehicleRepository = VehicleRepository();
  final TextEditingController _searchController = TextEditingController();

  List<VehicleModel> _vehicles = [];
  bool _isLoading = true;
  String? _errorMessage;
  String _selectedStatusFilter = "ALL";

  final List<String> _statusOptions = ["ALL", "ACTIVE", "MAINTENANCE", "INACTIVE"];

  @override
  void initState() {
    super.initState();
    _fetchVehicles();
  }

  Future<void> _fetchVehicles() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final list = await _vehicleRepository.getVehicles(
        organizationId: widget.organizationId,
        status: _selectedStatusFilter,
        search: _searchController.text.trim(),
      );
      setState(() {
        _vehicles = list;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll("Exception: ", "");
        _isLoading = false;
      });
    }
  }

  void _onStatusFilterSelected(String status) {
    setState(() {
      _selectedStatusFilter = status;
    });
    _fetchVehicles();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Fleet Vehicles Directory'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _fetchVehicles,
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
          await Navigator.of(context).push(
            MaterialPageRoute(
              builder: (ctx) => AddVehicleScreen(organizationId: widget.organizationId),
            ),
          );
          _fetchVehicles();
        },
        icon: const Icon(Icons.add_rounded),
        label: const Text('Add Vehicle'),
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Search & Filter Header Section
            Padding(
              padding: VeltricsSpacing.pagePadding,
              child: Column(
                children: [
                  TextField(
                    controller: _searchController,
                    decoration: InputDecoration(
                      hintText: "Search plate, make, or model...",
                      prefixIcon: const Icon(Icons.search),
                      suffixIcon: _searchController.text.isNotEmpty
                          ? IconButton(
                              icon: const Icon(Icons.clear),
                              onPressed: () {
                                _searchController.clear();
                                _fetchVehicles();
                              },
                            )
                          : null,
                    ),
                    onSubmitted: (_) => _fetchVehicles(),
                  ),
                  const SizedBox(height: VeltricsSpacing.xs2),

                  // Status Filter Chips
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: _statusOptions.map((status) {
                        final isSelected = _selectedStatusFilter == status;
                        return Padding(
                          padding: const EdgeInsets.only(right: 8),
                          child: FilterChip(
                            label: Text(status),
                            selected: isSelected,
                            onSelected: (_) => _onStatusFilterSelected(status),
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                ],
              ),
            ),

            // Vehicle List Body
            Expanded(
              child: _isLoading
                  ? const Center(child: CircularProgressIndicator())
                  : _errorMessage != null
                      ? Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Icon(Icons.error_outline, size: 48, color: VeltricsColors.errorLight),
                              const SizedBox(height: VeltricsSpacing.xs2),
                              Text(_errorMessage!, style: VeltricsTextStyles.bodyLg),
                              const SizedBox(height: VeltricsSpacing.sm),
                              ElevatedButton(
                                onPressed: _fetchVehicles,
                                child: const Text("Retry"),
                              ),
                            ],
                          ),
                        )
                      : _vehicles.isEmpty
                          ? Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(
                                    (_selectedStatusFilter != "ALL" || _searchController.text.isNotEmpty)
                                        ? Icons.filter_alt_off_outlined
                                        : Icons.directions_car_outlined,
                                    size: 64,
                                    color: isDark ? VeltricsColors.neutralD500 : VeltricsColors.neutral500,
                                  ),
                                  const SizedBox(height: VeltricsSpacing.sm),
                                  Text(
                                    (_selectedStatusFilter != "ALL" || _searchController.text.isNotEmpty)
                                        ? "No matching vehicles"
                                        : "No vehicles in fleet",
                                    style: VeltricsTextStyles.titleLg,
                                  ),
                                  const SizedBox(height: VeltricsSpacing.xs3),
                                  Padding(
                                    padding: const EdgeInsets.symmetric(horizontal: 32),
                                    child: Text(
                                      (_selectedStatusFilter != "ALL" || _searchController.text.isNotEmpty)
                                          ? "No vehicles match status '$_selectedStatusFilter' or your search. Try clearing filters."
                                          : "Your fleet directory is empty. Add your first vehicle below.",
                                      textAlign: TextAlign.center,
                                      style: VeltricsTextStyles.bodyMd,
                                    ),
                                  ),
                                  const SizedBox(height: VeltricsSpacing.md),
                                  if (_selectedStatusFilter != "ALL" || _searchController.text.isNotEmpty)
                                    OutlinedButton.icon(
                                      onPressed: () {
                                        setState(() {
                                          _selectedStatusFilter = "ALL";
                                          _searchController.clear();
                                        });
                                        _fetchVehicles();
                                      },
                                      icon: const Icon(Icons.filter_alt_off),
                                      label: const Text("Clear Filters"),
                                    )
                                  else
                                    ElevatedButton.icon(
                                      onPressed: () async {
                                        await Navigator.of(context).push(
                                          MaterialPageRoute(
                                            builder: (ctx) => AddVehicleScreen(organizationId: widget.organizationId),
                                          ),
                                        );
                                        _fetchVehicles();
                                      },
                                      icon: const Icon(Icons.add_rounded),
                                      label: const Text("Add First Vehicle"),
                                    ),
                                ],
                              ),
                            )
                          : RefreshIndicator(
                              onRefresh: _fetchVehicles,
                              child: ListView.builder(
                                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                                itemCount: _vehicles.length,
                                itemBuilder: (ctx, index) {
                                  final vehicle = _vehicles[index];
                                  return _buildVehicleCard(vehicle, theme, isDark);
                                },
                              ),
                            ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildVehicleCard(VehicleModel vehicle, ThemeData theme, bool isDark) {
    final isMaintenance = vehicle.status == "MAINTENANCE";
    final isInactive = vehicle.status == "INACTIVE";

    Color stripeColor = const Color(0xFF15803D); // Punjab green default
    if (vehicle.registrationProvince == "Sindh") {
      stripeColor = const Color(0xFFB91C1C);
    } else if (vehicle.registrationProvince == "ICT Islamabad") {
      stripeColor = const Color(0xFF1D4ED8);
    } else if (vehicle.registrationProvince == "Balochistan") {
      stripeColor = const Color(0xFFD97706);
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: InkWell(
        borderRadius: VeltricsRadius.smAll,
        onTap: () async {
          await Navigator.of(context).push(
            MaterialPageRoute(
              builder: (ctx) => VehicleDetailScreen(
                vehicleId: vehicle.id,
                organizationId: widget.organizationId,
              ),
            ),
          );
          _fetchVehicles();
        },
        child: Padding(
          padding: VeltricsSpacing.cardPaddingMobile,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Card Top Header: Vehicle Title & Status Pill
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Text(
                      "${vehicle.make} ${vehicle.model} (${vehicle.year})",
                      style: VeltricsTextStyles.titleLg,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  if (isMaintenance)
                    VeltricsStatusPill.warning(text: "MAINTENANCE", isDark: isDark)
                  else if (isInactive)
                    VeltricsStatusPill.error(text: "INACTIVE", isDark: isDark)
                  else
                    VeltricsStatusPill.healthy(text: "ACTIVE", isDark: isDark),
                ],
              ),
              const SizedBox(height: VeltricsSpacing.xs2),

              // Pakistani Plate Badge & Details
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: stripeColor,
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: Text(
                      vehicle.registrationProvince.toUpperCase(),
                      style: const TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                        fontSize: 10,
                        letterSpacing: 1.0,
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Text(
                    vehicle.licensePlate,
                    style: const TextStyle(
                      fontFamily: 'monospace',
                      fontWeight: FontWeight.w900,
                      fontSize: 16,
                      letterSpacing: 1.2,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: VeltricsSpacing.xs2),

              // Fuel & Odometer Info Line
              Row(
                children: [
                  Icon(
                    vehicle.fuelType == "EV" ? Icons.electric_car : Icons.local_gas_station_outlined,
                    size: 16,
                    color: theme.colorScheme.primary,
                  ),
                  const SizedBox(width: 4),
                  Text("${vehicle.fuelType} • ", style: VeltricsTextStyles.bodyMd),
                  const Icon(Icons.speed, size: 16, color: VeltricsColors.neutral500),
                  const SizedBox(width: 4),
                  Text("${vehicle.currentOdometerKm.toStringAsFixed(0)} km", style: VeltricsTextStyles.bodyMd),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
