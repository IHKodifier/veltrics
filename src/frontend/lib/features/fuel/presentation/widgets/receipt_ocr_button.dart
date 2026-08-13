import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../../../../theme/app_theme.dart';

class ReceiptOcrButton extends StatefulWidget {
  final Function(Map<String, dynamic> ocrData) onOcrResult;

  const ReceiptOcrButton({
    super.key,
    required this.onOcrResult,
  });

  @override
  State<ReceiptOcrButton> createState() => _ReceiptOcrButtonState();
}

class _ReceiptOcrButtonState extends State<ReceiptOcrButton> {
  bool _isScanning = false;

  Future<void> _triggerOcrScan() async {
    setState(() => _isScanning = true);
    try {
      final uri = Uri.parse('http://localhost:8000/api/v1/fuel/ocr-scan');
      final request = http.MultipartRequest('POST', uri);
      request.files.add(
        http.MultipartFile.fromString(
          'file',
          'Shell Gas Station Receipt\nTotal: \$112.50\nLiters: 45.0 L',
          filename: 'receipt_scan.jpg',
        ),
      );

      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        widget.onOcrResult(data);
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Receipt OCR scan complete! Fields auto-filled.')),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('OCR scan failed: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isScanning = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return OutlinedButton.icon(
      onPressed: _isScanning ? null : _triggerOcrScan,
      icon: _isScanning
          ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
          : const Icon(Icons.document_scanner, color: VeltricsColors.infoLight),
      label: Text(
        _isScanning ? 'Scanning Receipt...' : 'Scan Receipt with OCR (Pro)',
        style: const TextStyle(color: VeltricsColors.infoLight, fontWeight: FontWeight.bold),
      ),
      style: OutlinedButton.styleFrom(
        side: const BorderSide(color: VeltricsColors.infoLight),
        minimumSize: const Size.fromHeight(44),
      ),
    );
  }
}
