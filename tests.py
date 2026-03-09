#!/usr/bin/env python3
"""
Quick test script to verify DFIR CLI functionality.
"""
import subprocess
import json
import sys
import os

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from src.dfir_cli.cli import DFIRShell
        from src.dfir_cli.analyzer import DFIRAnalyzer
        from src.dfir_cli.windows_native import (
            get_processes,
            get_network_connections,
            get_system_info,
        )
        print("✓ All imports successful\n")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}\n")
        return False


def test_snapshot():
    """Test snapshot functionality."""
    print("Testing snapshot functionality...")
    try:
        from src.dfir_cli.analyzer import DFIRAnalyzer
        
        analyzer = DFIRAnalyzer()
        
        # Test different snapshot types
        for snap_type in ["system", "processes", "network"]:
            snap = analyzer.take_snapshot(snap_type)
            assert snap["type"] == snap_type
            assert "timestamp" in snap
            assert "data" in snap
            print(f"  ✓ Snapshot type '{snap_type}' works")
        
        print("✓ Snapshot tests passed\n")
        return True
    except Exception as e:
        print(f"✗ Snapshot test failed: {e}\n")
        return False


def test_export():
    """Test JSON export."""
    print("Testing JSON export...")
    try:
        from src.dfir_cli.analyzer import DFIRAnalyzer
        
        analyzer = DFIRAnalyzer()
        analyzer.take_snapshot("system")
        
        # Export to temp file
        export_file = "/tmp/test_export.json"
        if analyzer.export_json(export_file):
            # Verify file was created and is valid JSON
            with open(export_file, "r") as f:
                data = json.load(f)
                assert "snapshots" in data
                assert len(data["snapshots"]) > 0
            os.remove(export_file)
            print("✓ JSON export successful\n")
            return True
        else:
            print("✗ Export failed\n")
            return False
    except Exception as e:
        print(f"✗ Export test failed: {e}\n")
        return False


def test_sysinfo():
    """Test system information gathering."""
    print("Testing system information...")
    try:
        from src.dfir_cli.windows_native import get_system_info
        
        info = get_system_info()
        assert "os" in info
        assert "platform" in info
        assert "python" in info
        
        print(f"  ✓ OS: {info['os']}")
        print(f"  ✓ Platform: {info['platform']}")
        print(f"  ✓ Python: {info['python']}")
        print("✓ System info retrieval successful\n")
        return True
    except Exception as e:
        print(f"✗ System info test failed: {e}\n")
        return False


def test_processes():
    """Test process listing."""
    print("Testing process listing...")
    try:
        from src.dfir_cli.windows_native import get_processes
        
        procs = get_processes()
        assert isinstance(procs, list)
        assert len(procs) > 0
        
        print(f"  ✓ Found {len(procs)} processes")
        if procs:
            first_proc = procs[0]
            print(f"  ✓ First process keys: {list(first_proc.keys())[:3]}")
        
        print("✓ Process listing successful\n")
        return True
    except Exception as e:
        print(f"✗ Process test failed: {e}\n")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("DFIR CLI Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_imports,
        test_sysinfo,
        test_processes,
        test_snapshot,
        test_export,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
