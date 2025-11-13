"""
AGENT 8 - HTTP SERVER TEST SCRIPT
Testet die Agent 8 REST API Funktionalität

Stand: 13. November 2025
"""

import requests
import json
from datetime import datetime


# Konfiguration
AGENT_8_URL = "http://localhost:5000"
TEST_PROMPT = "Wide shot: Tropical beach at sunset. DJ spins reggaeton music. Camera pans right slowly."


def print_header(title):
    """Druckt einen formatierten Header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_success(message):
    """Druckt eine Erfolgs-Nachricht"""
    print(f"✅ {message}")


def print_error(message):
    """Druckt eine Fehler-Nachricht"""
    print(f"❌ {message}")


def print_info(message):
    """Druckt eine Info-Nachricht"""
    print(f"ℹ️  {message}")


def test_health_check():
    """Test 1: Ist der Server erreichbar?"""
    print_header("TEST 1: Server Health Check")

    try:
        response = requests.get(f"{AGENT_8_URL}/health", timeout=5)

        if response.status_code == 200:
            data = response.json()
            print_success("Server ist erreichbar!")
            print_info(f"Service: {data.get('service')}")
            print_info(f"Status: {data.get('status')}")
            print_info(f"Agent 8 initialisiert: {data.get('agent8_initialized')}")
            print_info(f"Verfügbare Endpoints: {', '.join(data.get('endpoints', []))}")
            return True
        else:
            print_error(f"Server antwortet mit Status Code: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print_error("Server ist nicht erreichbar!")
        print_info("Stelle sicher, dass der Server läuft: python agent_8_server.py")
        return False
    except Exception as e:
        print_error(f"Unerwarteter Fehler: {e}")
        return False


def test_validation():
    """Test 2: Funktioniert die Validation?"""
    print_header("TEST 2: Prompt Validation")

    print_info(f"Test-Prompt: \"{TEST_PROMPT}\"")
    print_info("Prompt Type: veo_3.1")
    print_info("Genre: reggaeton\n")

    try:
        # Request an Agent 8 senden
        response = requests.post(
            f"{AGENT_8_URL}/validate",
            json={
                "prompt": TEST_PROMPT,
                "prompt_type": "veo_3.1",
                "genre": "reggaeton"
            },
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            validation = data.get("validation", {})

            print_success("Validation erfolgreich!\n")

            # Ergebnis formatiert ausgeben
            print("┌─────────────────────────────────────────────────────────────────┐")
            print(f"│ VALIDATION RESULTS                                              │")
            print("├─────────────────────────────────────────────────────────────────┤")
            print(f"│ Quality Score:         {validation.get('quality_score', 0):.2f}                                      │")
            print(f"│ Ready for Generation:  {'Yes ✅' if validation.get('ready_for_generation') else 'No ⚠️ ':<45}│")
            print(f"│ Issues Found:          {validation.get('issues_count', 0):<45}│")
            print("└─────────────────────────────────────────────────────────────────┘")

            # Issues anzeigen
            issues = validation.get('issues', [])
            if issues:
                print("\n📋 Issues Found:")
                for i, issue in enumerate(issues, 1):
                    print(f"   {i}. {issue}")

            # Recommendations anzeigen
            recommendations = validation.get('recommendations', [])
            if recommendations:
                print("\n💡 Recommendations:")
                for i, rec in enumerate(recommendations, 1):
                    print(f"   {i}. {rec}")

            # Refined Prompt anzeigen
            refined_prompt = data.get('refined_prompt', '')
            if refined_prompt != TEST_PROMPT:
                print(f"\n🔧 Refined Prompt:")
                print(f"   {refined_prompt}")

            # Generation Mode
            gen_mode = data.get('generation_mode', 'N/A')
            print(f"\n🎬 Generation Mode: {gen_mode}")

            return True

        else:
            print_error(f"Validation fehlgeschlagen! Status Code: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print_error("Request Timeout! Server antwortet nicht innerhalb von 15 Sekunden.")
        return False
    except Exception as e:
        print_error(f"Validation Fehler: {e}")
        return False


def test_error_handling():
    """Test 3: Funktioniert das Fehler-Handling?"""
    print_header("TEST 3: Error Handling")

    # Test mit ungültigem prompt_type
    print_info("Teste ungültigen prompt_type...")

    try:
        response = requests.post(
            f"{AGENT_8_URL}/validate",
            json={
                "prompt": "Test prompt",
                "prompt_type": "invalid_type",  # Ungültiger Typ
                "genre": "pop"
            },
            timeout=5
        )

        if response.status_code == 400:
            print_success("Fehler-Handling funktioniert korrekt!")
            data = response.json()
            print_info(f"Fehler-Nachricht: {data.get('error')}")
            return True
        else:
            print_error(f"Unerwarteter Status Code: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Error Handling Test fehlgeschlagen: {e}")
        return False


def main():
    """Hauptfunktion - Führt alle Tests aus"""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  AGENT 8 HTTP SERVER - TEST SUITE".center(68) + "║")
    print("║" + f"  {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")

    # Test-Ergebnisse sammeln
    results = {
        "Health Check": test_health_check(),
        "Validation": test_validation(),
        "Error Handling": test_error_handling()
    }

    # Zusammenfassung
    print_header("TEST SUMMARY")

    all_passed = True
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name:<20} {status}")
        if not result:
            all_passed = False

    print("\n" + "-" * 70)

    if all_passed:
        print_success("Alle Tests erfolgreich! Agent 8 ist einsatzbereit! 🚀")
    else:
        print_error("Einige Tests sind fehlgeschlagen. Bitte prüfe die Logs.")

    print("-" * 70 + "\n")


if __name__ == "__main__":
    main()
