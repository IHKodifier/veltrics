import 'package:flutter/material.dart';
import 'theme/app_theme.dart';
import 'features/auth/presentation/screens/login_screen.dart';
import 'features/counter/counter_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const VeltricsApp());
}

class VeltricsApp extends StatelessWidget {
  const VeltricsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Veltrics Fleet & Vehicle Management',
      debugShowCheckedModeBanner: false,
      theme: VeltricsTheme.light(VeltricsPalette.teal),
      darkTheme: VeltricsTheme.dark(VeltricsPalette.teal),
      themeMode: ThemeMode.system,
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
    LoginScreen(),
    CounterScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
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
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.security),
            selectedIcon: Icon(Icons.security_rounded),
            label: 'Veltrics Auth',
          ),
          NavigationDestination(
            icon: Icon(Icons.add_circle_outline),
            selectedIcon: Icon(Icons.add_circle),
            label: 'Counter Demo',
          ),
        ],
      ),
    );
  }
}
