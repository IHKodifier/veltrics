import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/auth_repository.dart';
import '../../domain/user_model.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final AuthRepository _authRepository = AuthRepository();
  bool _isLoading = false;
  String? _errorMessage;
  AuthSession? _currentSession;

  Future<void> _handleGoogleSignIn() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final session = await _authRepository.registerWithGoogle(
        idToken: "mock-google-id-token-one-tap",
        email: "alex.driver@veltrics.com",
        fullName: "Alex Rivera",
        firebaseUid: "fb-uid-alex-rivera-101",
      );

      setState(() {
        _currentSession = session;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: VeltricsSpacing.pagePadding,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Spacer(),
              // Brand Logo & Header
              Center(
                child: Container(
                  width: 72,
                  height: 72,
                  decoration: BoxDecoration(
                    color: theme.colorScheme.primary.withValues(alpha: 0.12),
                    shape: BoxShape.circle,
                  ),
                  child: Icon(
                    Icons.directions_car_filled_rounded,
                    size: 36,
                    color: theme.colorScheme.primary,
                  ),
                ),
              ),
              const SizedBox(height: VeltricsSpacing.md),
              Text(
                "VELTRICS",
                textAlign: TextAlign.center,
                style: VeltricsTextStyles.displayLg.copyWith(
                  letterSpacing: 2.0,
                  color: theme.colorScheme.primary,
                ),
              ),
              const SizedBox(height: VeltricsSpacing.xs2),
              Text(
                "Fleet & Vehicle Management Platform",
                textAlign: TextAlign.center,
                style: VeltricsTextStyles.bodyLg.copyWith(
                  color: isDark ? VeltricsColors.neutralD500 : VeltricsColors.neutral500,
                ),
              ),
              const Spacer(),

              if (_currentSession != null) ...[
                // Logged In Status Card
                Card(
                  child: Padding(
                    padding: VeltricsSpacing.cardPaddingMobile,
                    child: Column(
                      children: [
                        VeltricsStatusPill.healthy(),
                        const SizedBox(height: VeltricsSpacing.xs3),
                        Text(
                          "Welcome, ${_currentSession!.user.fullName}!",
                          style: VeltricsTextStyles.titleLg,
                        ),
                        Text(
                          _currentSession!.user.email,
                          style: VeltricsTextStyles.bodyMd,
                        ),
                        const SizedBox(height: VeltricsSpacing.xs3),
                        Container(
                          padding: const EdgeInsets.all(VeltricsSpacing.xs3),
                          decoration: BoxDecoration(
                            color: theme.colorScheme.primaryContainer,
                            borderRadius: VeltricsRadius.smAll,
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                "Workspace:",
                                style: VeltricsTextStyles.labelMd,
                              ),
                              Text(
                                _currentSession!.organization.name,
                                style: VeltricsTextStyles.titleSm,
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: VeltricsSpacing.md),
              ],

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

              // Google One-Tap Sign In Button
              ElevatedButton.icon(
                onPressed: _isLoading ? null : _handleGoogleSignIn,
                icon: _isLoading
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(strokeWidth: 2.5),
                      )
                    : const Icon(Icons.account_circle_outlined, size: 22),
                label: Text(
                  _isLoading ? "Signing in..." : "Continue with Google",
                ),
              ),
              const SizedBox(height: VeltricsSpacing.md),
              Text(
                "By continuing you agree to Veltrics Terms of Service & Privacy Policy.",
                textAlign: TextAlign.center,
                style: VeltricsTextStyles.bodySm.copyWith(
                  color: isDark ? VeltricsColors.neutralD400 : VeltricsColors.neutral400,
                ),
              ),
              const SizedBox(height: VeltricsSpacing.md),
            ],
          ),
        ),
      ),
    );
  }
}
