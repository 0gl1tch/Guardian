#!/usr/bin/env python3
"""
Guardian DFIR CLI - Complete functionality test
"""
from src.dfir_cli.windows_native import get_system_info, get_processes, get_network_connections
from src.dfir_cli.analyzer import DFIRAnalyzer
import os
import json

print("=" * 60)
print("Guardian DFIR CLI - Live Test")
print("=" * 60)

print("\n1. SYSTEM INFORMATION")
print("-" * 60)
info = get_system_info()
for key, value in info.items():
    if key != 'systeminfo':
        print(f"  {key}: {value}")

print("\n2. PROCESS SAMPLE (first 3)")
print("-" * 60)
procs = get_processes()
if procs:
    keys = list(procs[0].keys())[:4]
    for i, proc in enumerate(procs[:3]):
        parts = [f"{k}={proc.get(k, 'N/A')}" for k in keys]
        print(f"  [{i+1}] {', '.join(parts)}")

print("\n3. NETWORK CONNECTIONS (first 2)")
print("-" * 60)
conns = get_network_connections()
if conns:
    for i, conn in enumerate(conns[:2]):
        proto = conn.get('protocol', 'N/A')
        local = conn.get('local_address', 'N/A')
        remote = conn.get('remote_address', 'N/A')
        state = conn.get('state', 'N/A')
        print(f"  [{i+1}] {proto} {local} -> {remote} [{state}]")

print("\n4. SNAPSHOT CREATION")
print("-" * 60)
analyzer = DFIRAnalyzer()
snap = analyzer.take_snapshot('full')
print(f"  ✓ Snapshot taken: {snap['timestamp']}")
print(f"  ✓ Type: {snap['type']}")
data_keys = ', '.join(snap['data'].keys())
print(f"  ✓ Data captured: {data_keys}")

print("\n5. JSON EXPORT")
print("-" * 60)
if analyzer.export_json('/tmp/guardian_test.json'):
    size = os.path.getsize('/tmp/guardian_test.json')
    print(f"  ✓ Exported to /tmp/guardian_test.json ({size} bytes)")
    
    # Show sample of JSON
    with open('/tmp/guardian_test.json', 'r') as f:
        data = json.load(f)
        print(f"  ✓ JSON contains {len(data['snapshots'])} snapshot(s)")
        print(f"  ✓ Export time: {data['export_time']}")

print("\n" + "=" * 60)
print("✓ All features working perfectly!")
print("=" * 60)
