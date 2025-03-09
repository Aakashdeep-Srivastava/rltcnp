#!/usr/bin/env python3
"""
Test script for feature extraction.
"""

import os
from src.feature_extraction import extract_features_from_rtl

def test_extract_features():
    """Test the extract_features_from_rtl function."""
    rtl_file = "data/sample_counter.v"
    
    # Test get_signals_only=True
    print("Testing get_signals_only=True...")
    signals = extract_features_from_rtl(rtl_file, get_signals_only=True)
    print(f"Signals found: {signals}")
    
    # Test extracting features for a specific signal
    print("\nTesting feature extraction for 'max_reached'...")
    features = extract_features_from_rtl(rtl_file, signal_name="max_reached")
    if features:
        print("Features extracted successfully:")
        for key, value in features.items():
            print(f"  {key}: {value}")
    else:
        print("Failed to extract features.")

if __name__ == "__main__":
    test_extract_features() 