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
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _fullNameController = TextEditingController();
  bool _isLoading = false;
  bool _showEmailForm = false;
  bool _isSignUpMode = false;
  String? _errorMessage;
  AuthSession? _currentSession;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _fullNameController.dispose();
    super.dispose();
  }

  Future<void> _handleGoogleSignIn() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final session = await _authRepository.signInWithGoogle(
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

  Future<void> _handleFacebookSignIn() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final session = await _authRepository.signInWithFacebook(
        idToken: "mock-facebook-id-token",
        email: "alex.driver@veltrics.com",
        fullName: "Alex Rivera",
        firebaseUid: "fb-uid-alex-rivera-fb",
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

  Future<void> _handleEmailSignUp() async {
    final email = _emailController.text.trim();
    final password = _passwordController.text;
    final fullName = _fullNameController.text.trim();

    if (email.isEmpty) {
      setState(() {
        _errorMessage = "Please enter your email address.";
      });
      return;
    }

    final passRegex = RegExp(r'^(?=.*[A-Z])(?=.*\d).{8,}$');
    if (!passRegex.hasMatch(password)) {
      setState(() {
        _errorMessage = "Password must be at least 8 characters with 1 uppercase letter & 1 digit.";
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final session = await _authRepository.registerWithEmail(
        email: email,
        password: password,
        fullName: fullName.isNotEmpty ? fullName : null,
      );

      setState(() {
        _currentSession = session;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll("Exception: ", "");
        _isLoading = false;
      });
    }
  }

  Future<void> _handleEmailSignIn() async {
    final email = _emailController.text.trim();
    final password = _passwordController.text;

    if (email.isEmpty) {
      setState(() {
        _errorMessage = "Please enter your email address.";
      });
      return;
    }
    if (password.isEmpty) {
      setState(() {
        _errorMessage = "Please enter your password.";
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final session = await _authRepository.signInWithEmail(
        email: email,
        password: password,
      );

      setState(() {
        _currentSession = session;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll("Exception: ", "");
        _isLoading = false;
      });
    }
  }

  void _showForgotPasswordDialog() {
    final emailCtrl = TextEditingController(text: _emailController.text);
    final tokenCtrl = TextEditingController();
    final newPassCtrl = TextEditingController();
    String? dialogError;
    String? issuedToken;

    showDialog(
      context: context,
      builder: (ctx) {
        return StatefulBuilder(
          builder: (context, setDialogState) {
            return AlertDialog(
              title: Text(issuedToken == null ? "Forgot Password" : "Reset Password"),
              content: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  if (dialogError != null) ...[
                    Text(
                      dialogError!,
                      style: VeltricsTextStyles.bodySm.copyWith(color: VeltricsColors.errorLight),
                    ),
                    const SizedBox(height: VeltricsSpacing.xs3),
                  ],
                  if (issuedToken == null) ...[
                    const Text("Enter your registered email address to receive password reset instructions."),
                    const SizedBox(height: VeltricsSpacing.sm),
                    TextField(
                      controller: emailCtrl,
                      keyboardType: TextInputType.emailAddress,
                      decoration: const InputDecoration(
                        labelText: "Email Address",
                        prefixIcon: Icon(Icons.email_outlined),
                      ),
                    ),
                  ] else ...[
                    const Text("Enter the reset token and your new strong password."),
                    const SizedBox(height: VeltricsSpacing.sm),
                    TextField(
                      controller: tokenCtrl,
                      decoration: const InputDecoration(
                        labelText: "Reset Token",
                        prefixIcon: Icon(Icons.vpn_key_outlined),
                      ),
                    ),
                    const SizedBox(height: VeltricsSpacing.xs3),
                    TextField(
                      controller: newPassCtrl,
                      obscureText: true,
                      decoration: const InputDecoration(
                        labelText: "New Password (Min 8 chars, 1 upper, 1 digit)",
                        prefixIcon: Icon(Icons.lock_outline),
                      ),
                    ),
                  ],
                ],
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.of(ctx).pop(),
                  child: const Text("Cancel"),
                ),
                ElevatedButton(
                  onPressed: () async {
                    if (issuedToken == null) {
                      final email = emailCtrl.text.trim();
                      if (email.isEmpty) {
                        setDialogState(() => dialogError = "Please enter your email.");
                        return;
                      }
                      try {
                        setDialogState(() => dialogError = null);
                        final res = await _authRepository.forgotPassword(email: email);
                        final token = res["reset_token"];
                        if (token != null) {
                          setDialogState(() {
                            issuedToken = token;
                            tokenCtrl.text = token;
                          });
                        } else {
                          Navigator.of(ctx).pop();
                          if (context.mounted) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(content: Text(res["message"] ?? "Reset email sent.")),
                            );
                          }
                        }
                      } catch (e) {
                        setDialogState(() => dialogError = e.toString().replaceAll("Exception: ", ""));
                      }
                    } else {
                      final token = tokenCtrl.text.trim();
                      final newPass = newPassCtrl.text;
                      if (token.isEmpty || newPass.isEmpty) {
                        setDialogState(() => dialogError = "Please fill in all fields.");
                        return;
                      }
                      try {
                        setDialogState(() => dialogError = null);
                        final res = await _authRepository.resetPassword(token: token, newPassword: newPass);
                        Navigator.of(ctx).pop();
                        if (context.mounted) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text(res["message"] ?? "Password reset successfully.")),
                          );
                        }
                      } catch (e) {
                        setDialogState(() => dialogError = e.toString().replaceAll("Exception: ", ""));
                      }
                    }
                  },
                  child: Text(issuedToken == null ? "Request Reset" : "Reset Password"),
                ),
              ],
            );
          },
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: VeltricsSpacing.pagePadding,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: VeltricsSpacing.xl),
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
              const SizedBox(height: VeltricsSpacing.lg),

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
                        if (_currentSession!.user.linkedProviders.isNotEmpty) ...[
                          const SizedBox(height: VeltricsSpacing.xs3),
                          Text(
                            "Linked Providers: ${_currentSession!.user.linkedProviders.join(', ')}",
                            style: VeltricsTextStyles.bodySm,
                          ),
                        ],
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

              if (_showEmailForm) ...[
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    ChoiceChip(
                      label: const Text("Sign In"),
                      selected: !_isSignUpMode,
                      onSelected: (val) {
                        if (val) setState(() => _isSignUpMode = false);
                      },
                    ),
                    const SizedBox(width: VeltricsSpacing.xs3),
                    ChoiceChip(
                      label: const Text("Sign Up"),
                      selected: _isSignUpMode,
                      onSelected: (val) {
                        if (val) setState(() => _isSignUpMode = true);
                      },
                    ),
                  ],
                ),
                const SizedBox(height: VeltricsSpacing.sm),
                if (_isSignUpMode) ...[
                  TextField(
                    controller: _fullNameController,
                    decoration: const InputDecoration(
                      labelText: "Full Name (Optional)",
                      prefixIcon: Icon(Icons.person_outline),
                    ),
                  ),
                  const SizedBox(height: VeltricsSpacing.xs3),
                ],
                TextField(
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                  decoration: const InputDecoration(
                    labelText: "Email Address",
                    prefixIcon: Icon(Icons.email_outlined),
                  ),
                ),
                const SizedBox(height: VeltricsSpacing.xs3),
                TextField(
                  controller: _passwordController,
                  obscureText: true,
                  decoration: InputDecoration(
                    labelText: _isSignUpMode
                        ? "Password (Min 8 chars, 1 upper, 1 digit)"
                        : "Password",
                    prefixIcon: const Icon(Icons.lock_outline),
                  ),
                ),
                if (!_isSignUpMode) ...[
                  Align(
                    alignment: Alignment.centerRight,
                    child: TextButton(
                      onPressed: _showForgotPasswordDialog,
                      child: const Text("Forgot Password?"),
                    ),
                  ),
                ] else ...[
                  const SizedBox(height: VeltricsSpacing.sm),
                ],
                ElevatedButton.icon(

                  onPressed: _isLoading
                      ? null
                      : (_isSignUpMode ? _handleEmailSignUp : _handleEmailSignIn),
                  icon: Icon(_isSignUpMode ? Icons.person_add_rounded : Icons.login_rounded),
                  label: Text(_isLoading
                      ? (_isSignUpMode ? "Creating Account..." : "Signing In...")
                      : (_isSignUpMode ? "Sign Up with Email" : "Sign In with Email")),
                ),
                const SizedBox(height: VeltricsSpacing.xs3),
                TextButton(
                  onPressed: () => setState(() => _showEmailForm = false),
                  child: const Text("Back to OAuth Options"),
                ),
              ] else ...[
                // Email & Password Sign In / Sign Up Option Toggle
                ElevatedButton.icon(
                  onPressed: () => setState(() {
                    _showEmailForm = true;
                    _isSignUpMode = false;
                  }),
                  icon: const Icon(Icons.mail_outline_rounded, size: 22),
                  label: const Text("Sign In or Sign Up with Email"),
                ),
                const SizedBox(height: VeltricsSpacing.sm),

                // Google One-Tap Sign In Button
                OutlinedButton.icon(
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
                const SizedBox(height: VeltricsSpacing.sm),

                // Facebook Sign In Button
                OutlinedButton.icon(
                  onPressed: _isLoading ? null : _handleFacebookSignIn,
                  icon: _isLoading
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(strokeWidth: 2.5),
                        )
                      : const Icon(Icons.facebook_rounded, size: 22, color: Color(0xFF1877F2)),
                  label: Text(
                    _isLoading ? "Signing in..." : "Continue with Facebook",
                  ),
                ),
              ],
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
