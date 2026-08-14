import 'package:flutter/material.dart';

class FleetManagerDashboardScreen extends StatefulWidget {
  const FleetManagerDashboardScreen({Key? key}) : super(key: key);

  @override
  State<FleetManagerDashboardScreen> createState() => _FleetManagerDashboardScreenState();
}

class _FleetManagerDashboardScreenState extends State<FleetManagerDashboardScreen> {
  bool _isLoading = false;

  // Mock Dashboard Data for Web Rendering
  final Map<String, dynamic> _kpiData = {
    'total_vehicles': 14,
    'active_vehicles': 11,
    'maintenance_vehicles': 2,
    'inactive_vehicles': 1,
    'availability_percentage': 78.6,
    'monthly_fuel_cost': 4200.0,
    'monthly_maintenance_cost': 1850.0,
    'total_monthly_cost': 6050.0,
    'active_trips_count': 6,
  };

  final List<Map<String, dynamic>> _costRankings = [
    {
      'rank': 1,
      'license_plate': 'V-108',
      'make_model': 'Isuzu NPR Truck',
      'fuel_cost': 1400.0,
      'maintenance_cost': 850.0,
      'total_cost': 2250.0,
      'cost_per_km': 0.18,
    },
    {
      'rank': 2,
      'license_plate': 'V-102',
      'make_model': 'Ford Transit Van',
      'fuel_cost': 1100.0,
      'maintenance_cost': 600.0,
      'total_cost': 1700.0,
      'cost_per_km': 0.15,
    },
    {
      'rank': 3,
      'license_plate': 'V-105',
      'make_model': 'Toyota Hilux Pickup',
      'fuel_cost': 950.0,
      'maintenance_cost': 250.0,
      'total_cost': 1200.0,
      'cost_per_km': 0.12,
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Fleet Manager Executive Dashboard'),
        backgroundColor: Colors.indigo,
        actions: [
          IconButton(
            icon: const Icon(Icons.dashboard_customize),
            tooltip: 'Customize Layout',
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Dashboard layout mode activated')),
              );
            },
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildKpiHeaderGrid(),
                  const SizedBox(height: 24),
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Expanded(flex: 3, child: _buildCostRankingCard()),
                      const SizedBox(width: 20),
                      Expanded(flex: 2, child: _buildAvailabilityWidget()),
                    ],
                  ),
                ],
              ),
            ),
    );
  }

  Widget _buildKpiHeaderGrid() {
    return Wrap(
      spacing: 16,
      runSpacing: 16,
      children: [
        _buildKpiCard('Total Fleet Size', '${_kpiData['total_vehicles']}', Icons.directions_car, Colors.blue),
        _buildKpiCard('Fleet Availability', '${_kpiData['availability_percentage']}%', Icons.check_circle, Colors.green),
        _buildKpiCard('Total Monthly Cost', '\$${_kpiData['total_monthly_cost']}', Icons.attach_money, Colors.orange),
        _buildKpiCard('Active Trips', '${_kpiData['active_trips_count']}', Icons.route, Colors.purple),
      ],
    );
  }

  Widget _buildKpiCard(String title, String value, IconData icon, Color color) {
    return SizedBox(
      width: 260,
      child: Card(
        elevation: 3,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
            children: [
              CircleAvatar(
                backgroundColor: color.withOpacity(0.15),
                radius: 24,
                child: Icon(icon, color: color, size: 28),
              ),
              const SizedBox(width: 14),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: TextStyle(color: Colors.grey.shade600, fontSize: 13)),
                  const SizedBox(height: 4),
                  Text(value, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCostRankingCard() {
    return Card(
      elevation: 3,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              mainAxisAlignment: MainAxisAlignment.between,
              children: [
                Text(
                  'Fleet Vehicle Cost Rankings (TCO & Heatmap)',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
                Icon(Icons.bar_chart, color: Colors.indigo),
              ],
            ),
            const Divider(height: 24),
            DataTable(
              columns: const [
                DataColumn(label: Text('#')),
                DataColumn(label: Text('Vehicle / Plate')),
                DataColumn(label: Text('Fuel Cost')),
                DataColumn(label: Text('Mnt. Cost')),
                DataColumn(label: Text('Total Cost')),
                DataColumn(label: Text('Cost / km')),
              ],
              rows: _costRankings.map((item) {
                return DataRow(cells: [
                  DataCell(Text('${item['rank']}')),
                  DataCell(Text('${item['make_model']} (${item['license_plate']})')),
                  DataCell(Text('\$${item['fuel_cost']}')),
                  DataCell(Text('\$${item['maintenance_cost']}')),
                  DataCell(Text('\$${item['total_cost']}', style: const TextStyle(fontWeight: FontWeight.bold))),
                  DataCell(Text('\$${item['cost_per_km']}/km')),
                ]);
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAvailabilityWidget() {
    return Card(
      elevation: 3,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Vehicle Availability Status',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const Divider(height: 24),
            ListTile(
              leading: const Icon(Icons.check_circle, color: Colors.green),
              title: const Text('Available / Active'),
              trailing: Text('${_kpiData['active_vehicles']} Vehicles', style: const TextStyle(fontWeight: FontWeight.bold)),
            ),
            ListTile(
              leading: const Icon(Icons.build, color: Colors.orange),
              title: const Text('Under Maintenance'),
              trailing: Text('${_kpiData['maintenance_vehicles']} Vehicles', style: const TextStyle(fontWeight: FontWeight.bold)),
            ),
            ListTile(
              leading: const Icon(Icons.do_not_disturb_on, color: Colors.red),
              title: const Text('Inactive / Decommissioned'),
              trailing: Text('${_kpiData['inactive_vehicles']} Vehicles', style: const TextStyle(fontWeight: FontWeight.bold)),
            ),
          ],
        ),
      ),
    );
  }
}
