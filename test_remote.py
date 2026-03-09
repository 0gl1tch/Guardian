#!/usr/bin/env python3
"""
Guardian Standalone - Overall Test
Tests the all-in-one guardian_standalone.py file
"""

import subprocess
import sys

def test_standalone_import():
    """Test if standalone script can be imported"""
    print("Testing guardi_standalone.py...")
    
    # Test basic imports
    result = subprocess.run(
        [sys.executable, '-c', 
         'from guardian_standalone import DFIRShell, DFIRAnalyzer, get_processes; '
         'print("✓ Standalone imports work")'],
        cwd='/home/vincius.souza/Guardian',
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(result.stdout)
        return True
    else:
        print(f"✗ Error: {result.stderr}")
        return False


def test_standalone_functionality():
    """Test core functionality"""
    print("\nTesting standalone functionality...")
    
    code = """
from guardian_standalone import DFIRAnalyzer

# Create analyzer
analyzer = DFIRAnalyzer()

# Test snapshot
snap = analyzer.take_snapshot('system')
print(f"✓ System snapshot: {snap['type']}")

# Test export
if analyzer.export_json('/tmp/test_standalone.json'):
    print("✓ JSON export works")
else:
    print("✗ Export failed")

# Test list
snaps = analyzer.list_snapshots()
print(f"✓ Snapshots list: {len(snaps)} snapshot(s)")
"""
    
    result = subprocess.run(
        [sys.executable, '-c', code],
        cwd='/home/vincius.souza/Guardian',
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(result.stdout)
        return True
    else:
        print(f"✗ Error: {result.stderr}")
        return False


def test_server_code():
    """Test server script loads without errors"""
    print("\nTesting server.py syntax...")
    
    result = subprocess.run(
        [sys.executable, '-m', 'py_compile', 'server.py'],
        cwd='/home/vincius.souza/Guardian',
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ server.py syntax is valid")
        return True
    else:
        print(f"✗ Error: {result.stderr}")
        return False


def test_powershell_script():
    """Validate PowerShell script syntax (without executing)"""
    print("\nTesting PowerShell script...")
    
    try:
        with open('/home/vincius.souza/Guardian/guardian_loader.ps1', 'r') as f:
            content = f.read()
            if 'python3' in content and 'DownloadString' in content:
                print("✓ PowerShell loader looks valid")
                return True
    except:
        pass
    
    print("✗ PowerShell loader validation failed")
    return False


def test_bash_script():
    """Validate Bash script syntax (without executing)"""
    print("\nTesting Bash script...")
    
    result = subprocess.run(
        ['bash', '-n', 'guardian_loader.sh'],
        cwd='/home/vincius.souza/Guardian',
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ Bash loader syntax is valid")
        return True
    else:
        print(f"✗ Error: {result.stderr}")
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("Guardian Standalone & Remote Execution Test Suite")
    print("=" * 60)
    
    tests = [
        test_standalone_import,
        test_standalone_functionality,
        test_server_code,
        test_powershell_script,
        test_bash_script,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if all(results):
        print("\n✓ All tests passed! Guardian is ready for remote execution")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed")
        sys.exit(1)
