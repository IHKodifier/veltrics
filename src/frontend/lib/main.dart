import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'theme/app_theme.dart';
import 'core/localization/app_localizations.dart';
import 'features/auth/presentation/screens/login_screen.dart';
import 'features/dashboard/presentation/screens/dashboard_screen.dart';
import 'features/vehicle/presentation/screens/vehicle_list_screen.dart';
import 'features/settings/presentation/controllers/settings_controller.dart';
import 'features/settings/presentation/screens/settings_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(
    ChangeNotifierProvider(
      create: (_) => SettingsController(),
      child: const VeltricsApp(),
    ),
  );
}

class VeltricsApp extends StatelessWidget {
  const VeltricsApp({super.key});

  @override
  Widget build(BuildContext context) {
    final settings = Provider.of<SettingsController>(context);

    return MaterialApp(
      title: 'Veltrics Fleet & Vehicle Management',
      debugShowCheckedModeBanner: false,
      theme: VeltricsTheme.light(settings.palette, highContrast: settings.highContrastMode),
      darkTheme: VeltricsTheme.dark(settings.palette, highContrast: settings.highContrastMode),
      themeMode: settings.themeMode,
      locale: settings.locale,
      localizationsDelegates: const [
        AppLocalizationsDelegate(),
      ],
      supportedLocales: const [
        Locale('en'),
        Locale('ur'),
        Locale('ar'),
      ],
      home: const MainNavigationWrapper(),
    );
  }
}

class MainNavigationWrapper extends StatefulWidget {
  const MainNavigationWrapper({super.key});

  @override
  State<MainNavigationWrapper> createState() => _MainNavigationWrapperState();
}

class _MainNavigationWrapperState extends State<MainNavigationWrapper> {
  int _currentIndex = 0;

  final List<Widget> _screens = const [
    DashboardScreen(),
    VehicleListScreen(),
    LoginScreen(),
    SettingsScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context);

    return Directionality(
      textDirection: loc.textDirection,
      child: Scaffold(
        body: IndexedStack(
          index: _currentIndex,
          children: _screens,
        ),
        bottomNavigationBar: NavigationBar(
          selectedIndex: _currentIndex,
          onDestinationSelected: (index) {
            setState(() {
              _currentIndex = index;
            });
          },
          destinations: [
            NavigationDestination(
              icon: const Icon(Icons.dashboard_outlined),
              selectedIcon: const Icon(Icons.dashboard),
              label: loc.translate('dashboard'),
            ),
            NavigationDestination(
              icon: const Icon(Icons.directions_car_outlined),
              selectedIcon: const Icon(Icons.directions_car),
              label: loc.translate('fleet'),
            ),
            NavigationDestination(
              icon: const Icon(Icons.security),
              selectedIcon: const Icon(Icons.security_rounded),
              label: loc.translate('auth'),
            ),
            NavigationDestination(
              icon: const Icon(Icons.settings_outlined),
              selectedIcon: const Icon(Icons.settings),
              label: loc.translate('settings'),
            ),
          ],
        ),
      ),
    );
  }
}
