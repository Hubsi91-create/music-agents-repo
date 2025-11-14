# 🚀 MUSIC AGENTS - START GUIDE

Einfache Start-Scripts für alle Komponenten des Music Agents Systems.

## ⚡ QUICK START

### Option 1: Alles auf einmal starten
```batch
start_all.bat
```
Öffnet 3 separate Fenster für Orchestrator, Backend und Tests.

### Option 2: Einzelne Komponenten starten

#### 🎯 Orchestrator
```batch
# Training starten
start_orchestrator.bat train

# Training mit verbose output
start_orchestrator.bat train --verbose

# Statistiken anzeigen
start_orchestrator.bat stats

# Enhanced Training (100 Iterationen)
start_orchestrator.bat enhanced-train 100

# Orchestration Report generieren
start_orchestrator.bat electro uplifting
```

#### 🌐 Dashboard Backend
```batch
start_backend.bat
```
**HINWEIS**: Backend ist aktuell minimal implementiert (nur database.py).
Weitere Entwicklung nötig für vollständige Funktionalität.

#### 🧪 Integration Tests
```batch
start_tests.bat
```
Führt `test_all_agents_local.py` mit pytest aus.

---

## 📋 VORAUSSETZUNGEN

### Erforderlich
- Python 3.13+ (installiert ✅)
- Basis-Dependencies aus requirements.txt

### Optional (für volle Funktionalität)
```batch
pip install -r requirements.txt
```

Fehlende Dependencies (aktuell):
- `praw` - Reddit API harvesting
- `youtube-transcript-api` - YouTube harvesting
- `beautifulsoup4` - Web scraping
- `requests` - HTTP requests

---

## 🔧 TROUBLESHOOTING

### Problem: "python not found"
**Lösung**: Python ist installiert, aber möglicherweise PATH-Problem.
Versuche: `python3` statt `python` oder vollständiger Pfad.

### Problem: "orchestrator.py not found"
**Lösung**: Die Scripts wechseln automatisch ins richtige Verzeichnis.
Nicht manuell `cd` verwenden!

### Problem: Warnungen beim Start
**Normal**: Warnungen über fehlende Module sind OK.
Das System läuft mit reduzierter Funktionalität.

### Problem: Backend startet nicht
**Status**: Backend ist noch in Entwicklung.
Nur database.py vorhanden, kein Entry Point (app.py) yet.

---

## 📁 DATEISTRUKTUR

```
music-agents-repo/
├── start_all.bat              # Master Start Script
├── start_orchestrator.bat     # Orchestrator Start
├── start_backend.bat          # Backend Start
├── start_tests.bat            # Tests Start
├── START_GUIDE.md            # Diese Anleitung
│
├── orchestrator/
│   ├── orchestrator.py       # HAUPTDATEI ✅
│   ├── prompt_harvesting/    # Harvesting Modules ✅
│   └── training/             # Training Modules ✅
│
├── dashboard/
│   └── backend/
│       ├── database.py       # DB Module ✅
│       ├── routes/           # (leer, in Entwicklung)
│       └── static/           # Static files
│
└── test_all_agents_local.py  # Integration Tests ✅
```

---

## ✅ NÄCHSTE SCHRITTE

1. **Dependencies installieren** (optional):
   ```batch
   pip install -r requirements.txt
   ```

2. **Test Orchestrator**:
   ```batch
   start_orchestrator.bat stats
   ```

3. **Backend implementieren**:
   - Erstelle `dashboard/backend/app.py`
   - Implementiere Flask Routes
   - Teste mit `start_backend.bat`

4. **Integration Tests ausführen**:
   ```batch
   start_tests.bat
   ```

---

## 🎯 PRODUCTION DEPLOYMENT

Für Production siehe:
- `DEPLOY_GUIDE.md`
- `deployment_guide.md`
- `QUICK_START.md`

---

**Erstellt**: 2025-01-14
**Version**: 1.0
**Status**: Development Ready ✅
