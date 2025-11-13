# 🚀 Agent 8 Quick Start (5 Minuten)

## Schritt 1: Repo runterladen

```bash
git clone https://github.com/Hubsi91-create/music-agents-repo.git
cd music-agents-repo
```

## Schritt 2: Python Setup

```bash
# Virtual Environment erstellen
python -m venv venv

# Aktivieren
# Windows:
.\venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt
```

## Schritt 3: Agent 8 Server starten

```bash
python agent_8_server.py
```

Du siehst:

```
* Running on http://localhost:5000
✅ Agent 8 HTTP Server started!
```

## Schritt 4: Dashboard öffnen

**Windows:**
```bash
start agent_8_simple_dashboard.html
```

**Linux/Mac:**
```bash
open agent_8_simple_dashboard.html
```

Dashboard öffnet sich im Browser! 🎉

## Schritt 5: Test durchführen

Im Dashboard: Klick **"🧪 Test Agent 8 durchführen"**

Du siehst:
- 🟢 Quality Score: 0.xx
- Status: ✅ Ready oder ⚠️ Not Ready
- Issues gefunden
- Auto-Fixes angewendet

---

# Das wars! 🎉

Dein Agent 8 ist jetzt am Laufen!

---

## Nächste Schritte

### Lokal testen (15 Min):
- Prompts ändern im Dashboard
- Verschiedene Genres testen
- Quality Scores beobachten

### In die Cloud (30 Min):
- Google Cloud Project erstellen
- `./deploy_to_gcloud.sh` ausführen
- Function URL kopieren

### In Produktion (1 Stunde):
- Agent 5a/5b mit Cloud URL verbinden
- 100 Prompts testen
- Metrics analysieren

---

## FAQ

**Q: Server läuft nicht?**
A: Port 5000 belegt? → `netstat -ano | findstr :5000`

**Q: Dashboard zeigt nur Rot?**
A: Server nicht gestartet → `python agent_8_server.py`

**Q: Welcher Browser?**
A: Chrome, Firefox, Edge - alle funktionieren!

---

## Support

- **GitHub Issues:** https://github.com/Hubsi91-create/music-agents-repo/issues
- **Questions?** → docs/README.md
