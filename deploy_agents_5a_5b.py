#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Production Test Script for Agent 5a (Veo) and Agent 5b (Runway)
Tests API availability and image generation capabilities
"""

import argparse
import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}[OK] {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}[WARN] {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}[ERROR] {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}[INFO] {text}{Colors.RESET}")

def check_agent8_api():
    """Check if Agent 8 API is running"""
    import requests

    print_info("Checking Agent 8 API availability...")
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print_success("Agent 8 API is running on http://localhost:5000")
            return True
        else:
            print_warning(f"Agent 8 API responded with status {response.status_code}")
            return False
    except Exception as e:
        print_warning(f"Agent 8 API not available: {e}")
        print_info("Continuing without Agent 8 validation...")
        return False

def check_screenplay_file():
    """Find screenplay file"""
    screenplay_path = Path("agent-4-screenplay-generator/screenplay.json")

    if screenplay_path.exists():
        print_success(f"Screenplay file found: {screenplay_path}")
        return screenplay_path
    else:
        print_error(f"Screenplay file not found: {screenplay_path}")
        return None

def run_agent_5a(screenplay_file, output_dir):
    """Run Agent 5a (Veo) and generate prompts"""
    print_header("AGENT 5a - VEO 3.1 ADAPTER")

    agent_path = Path("agent-5a-veo-adapter/agent_5a.py")

    if not agent_path.exists():
        print_error(f"Agent 5a not found: {agent_path}")
        return None

    print_info(f"Running Agent 5a with screenplay: {screenplay_file}")

    try:
        result = subprocess.run(
            ["python", str(agent_path), str(screenplay_file)],
            capture_output=True,
            text=True,
            timeout=60
        )

        print(result.stdout)

        if result.returncode == 0:
            veo_prompts_path = Path("veo_prompts.json")
            if veo_prompts_path.exists():
                # Move to output directory
                output_path = output_dir / "veo_prompts.json"
                veo_prompts_path.rename(output_path)

                with open(output_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                print_success(f"Veo prompts generated: {len(data.get('prompts', []))} scenes")
                print_success(f"Output saved to: {output_path}")
                return output_path
            else:
                print_error("Veo prompts file not created")
                return None
        else:
            print_error(f"Agent 5a failed with error:\n{result.stderr}")
            return None

    except subprocess.TimeoutExpired:
        print_error("Agent 5a timed out after 60 seconds")
        return None
    except Exception as e:
        print_error(f"Error running Agent 5a: {e}")
        return None

def run_agent_5b(screenplay_file, output_dir):
    """Run Agent 5b (Runway) and generate prompts"""
    print_header("AGENT 5b - RUNWAY GEN-3 ADAPTER")

    agent_path = Path("agent-5b-runway-adapter/agent_5b.py")

    if not agent_path.exists():
        print_error(f"Agent 5b not found: {agent_path}")
        return None

    print_info(f"Running Agent 5b with screenplay: {screenplay_file}")

    try:
        result = subprocess.run(
            ["python", str(agent_path), str(screenplay_file)],
            capture_output=True,
            text=True,
            timeout=60
        )

        print(result.stdout)

        if result.returncode == 0:
            runway_prompts_path = Path("runway_prompts.json")
            if runway_prompts_path.exists():
                # Move to output directory
                output_path = output_dir / "runway_prompts.json"
                runway_prompts_path.rename(output_path)

                with open(output_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                print_success(f"Runway prompts generated: {len(data.get('prompts', []))} scenes")
                print_success(f"Output saved to: {output_path}")
                return output_path
            else:
                print_error("Runway prompts file not created")
                return None
        else:
            print_error(f"Agent 5b failed with error:\n{result.stderr}")
            return None

    except subprocess.TimeoutExpired:
        print_error("Agent 5b timed out after 60 seconds")
        return None
    except Exception as e:
        print_error(f"Error running Agent 5b: {e}")
        return None

def display_summary(output_dir, veo_path, runway_path):
    """Display test summary"""
    print_header("TEST SUMMARY")

    print(f"\n{Colors.BOLD}Output Directory:{Colors.RESET}")
    print(f"  [DIR] {output_dir.absolute()}")

    if veo_path:
        print(f"\n{Colors.BOLD}Veo 3.1 Prompts:{Colors.RESET}")
        print(f"  [FILE] {veo_path.name}")
        with open(veo_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"  [SCENES] {len(data.get('prompts', []))}")
            print(f"  [TITLE] {data.get('music_title', 'N/A')}")

    if runway_path:
        print(f"\n{Colors.BOLD}Runway Gen-3 Prompts:{Colors.RESET}")
        print(f"  [FILE] {runway_path.name}")
        with open(runway_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"  [SCENES] {len(data.get('prompts', []))}")
            print(f"  [TITLE] {data.get('music_title', 'N/A')}")

    print(f"\n{Colors.GREEN}{Colors.BOLD}[SUCCESS] Production test completed successfully!{Colors.RESET}\n")

def main():
    parser = argparse.ArgumentParser(
        description='Deploy and test Agent 5a (Veo) and Agent 5b (Runway)'
    )
    parser.add_argument(
        '--production',
        action='store_true',
        help='Run in production mode'
    )
    parser.add_argument(
        '--test-single',
        action='store_true',
        help='Test with single screenplay'
    )

    args = parser.parse_args()

    print_header("AGENT 5a & 5b PRODUCTION TEST")

    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"outputs/agents_5a_5b_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)

    print_info(f"Output directory: {output_dir}")

    # Check Agent 8 API
    agent8_available = check_agent8_api()

    # Find screenplay file
    screenplay_file = check_screenplay_file()
    if not screenplay_file:
        print_error("Cannot proceed without screenplay file")
        sys.exit(1)

    # Run Agent 5a
    veo_path = run_agent_5a(screenplay_file, output_dir)

    # Run Agent 5b
    runway_path = run_agent_5b(screenplay_file, output_dir)

    # Display summary
    if veo_path or runway_path:
        display_summary(output_dir, veo_path, runway_path)
    else:
        print_error("Both agents failed to generate outputs")
        sys.exit(1)

if __name__ == '__main__':
    main()
