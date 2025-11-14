# API Keys Directory

🔒 **WICHTIG: Diese Keys bleiben lokal und werden NIEMALS committed!**

Das `keys/` Verzeichnis ist in `.gitignore` eingetragen.

## Setup

1. **Kopiere die Templates:**
   ```bash
   cp google-key.json.template google-key.json
   cp runway-key.json.template runway-key.json
   ```

2. **Fülle die JSON-Dateien mit deinen echten Keys:**

   **google-key.json:**
   ```json
   {
     "api_key": "dein-echter-gemini-api-key",
     "project_id": "dein-google-project-id"
   }
   ```

   **runway-key.json:**
   ```json
   {
     "api_key": "dein-echter-runway-api-key"
   }
   ```

3. **Starte den Production-Test:**
   ```bash
   python deploy_agents_5a_5b.py --production --test-single
   ```

## Sicherheit

- ✅ `keys/` ist in `.gitignore` - wird NIEMALS committed
- ✅ JSON-Dateien bleiben nur auf deinem lokalen System
- ✅ Keine Keys erscheinen im Chat oder in der History

## Alternative Key-Namen

Das Skript unterstützt verschiedene Key-Namen in den JSON-Dateien:

**Google/Gemini:** `api_key`, `key`, `GEMINI_API_KEY`, `private_key`
**Runway:** `api_key`, `key`, `RUNWAY_API_KEY`, `token`
