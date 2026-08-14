import 'package:flutter/material.dart';

class AdBannerWidget extends StatelessWidget {
  final String tier;
  final String adUnitId;

  const AdBannerWidget({
    Key? key,
    required this.tier,
    this.adUnitId = 'ca-app-pub-3940256099942544/6300978111', // Official Google AdMob Test Banner Unit ID
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // UC-101: Render Ad-Free Experience for Pro Subscribers
    if (tier.toLowerCase() == 'pro') {
      return const SizedBox.shrink();
    }

    // UC-098: Display AdMob Banner Ads (Free Tier Mobile)
    return Container(
      width: double.infinity,
      height: 50,
      color: Colors.grey.shade200,
      alignment: Alignment.center,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
            decoration: BoxDecoration(
              color: Colors.amber.shade700,
              borderRadius: BorderRadius.circular(4),
            ),
            child: const Text(
              'Ad',
              style: TextStyle(
                color: Colors.white,
                fontSize: 10,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          const SizedBox(width: 8),
          Text(
            'Google AdMob Banner ($adUnitId)',
            style: TextStyle(
              fontSize: 12,
              color: Colors.grey.shade800,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }
}
