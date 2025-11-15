# Frontend Integration Guide

## Übersicht

Dieses Frontend wurde erfolgreich mit React Query und Axios integriert, um **alle Mock-Daten durch echte API-Aufrufe zu ersetzen**.

## Implementierte Features

### 1. **React Query Provider Setup**
- ✅ QueryClientProvider in [main.tsx](src/main.tsx) konfiguriert
- ✅ Optimale Default-Konfiguration (retry, staleTime, refetchOnWindowFocus)

### 2. **Zentraler API Client**
- ✅ [apiClient.ts](src/services/apiClient.ts) erstellt
- ✅ Axios-Instance mit dynamischer Base URL aus `.env.development`
- ✅ Globales Error Handling via Interceptors

### 3. **Custom Hooks für API-Aufrufe**
- ✅ [useStoryboardApi.ts](src/hooks/useStoryboardApi.ts) erstellt
- ✅ Wiederverwendbare Hooks für alle Storyboard-Endpoints
- ✅ Type-safe mit TypeScript (nutzt [storyboard-api.ts](src/types/storyboard-api.ts))

### 4. **StoryboardView Integration**
- ✅ [StoryboardView.tsx](src/components/storyboard/StoryboardView.tsx) aktualisiert
- ✅ Alle Mock-Daten durch echte API-Aufrufe ersetzt
- ✅ Loading States (Spinner) implementiert
- ✅ Error Handling (Fehlermeldungen) implementiert

### 5. **Polling für Echtzeit-Updates**
- ✅ Agent Progress Bar aktualisiert sich alle 5 Sekunden (`refetchInterval: 5000`)
- ✅ Health Check alle 30 Sekunden

## Dateistruktur

```
dashboard/frontend/
├── .env.development          # Umgebungsvariablen (API Base URL)
├── src/
│   ├── services/
│   │   └── apiClient.ts      # Zentraler Axios Client
│   ├── hooks/
│   │   └── useStoryboardApi.ts  # Custom React Query Hooks
│   ├── types/
│   │   └── storyboard-api.ts    # TypeScript API Types
│   ├── components/
│   │   └── storyboard/
│   │       └── StoryboardView.tsx  # Haupt-Komponente (aktualisiert)
│   └── main.tsx              # QueryClientProvider Setup
└── INTEGRATION_GUIDE.md      # Diese Datei
```

## Verwendete Hooks

### Video Engines
```typescript
const { data: enginesData, isLoading, isError } = useEngines();
```

### Agent Progress (mit Polling)
```typescript
const { data: agentProgress } = useAgentProgress({ refetchInterval: 5000 });
```

### Video Status
```typescript
const { data: videoStatus } = useVideoStatus(taskId, { refetchInterval: 3000 });
```

### Drive Files
```typescript
const { data: files } = useDriveFiles(folderId, 'audio', accessToken);
```

## Umgebungsvariablen

Die `.env.development` Datei enthält:

```env
VITE_API_BASE_URL=http://localhost:5000/api/storyboard
```

**Wichtig:** Für Production `.env.production` erstellen mit der entsprechenden URL.

## Backend-Anforderungen

Das Backend muss laufen auf:
- **Entwicklung:** `http://localhost:5000`
- **Endpoint:** `/api/storyboard/*`

## Nächste Schritte (Optional)

1. **React Query DevTools** installieren (für Debugging):
   ```bash
   npm install @tanstack/react-query-devtools
   ```

2. **Toast Notifications** für besseres Error Handling:
   ```bash
   npm install react-hot-toast
   ```

3. **Weitere Endpoints** integrieren:
   - Metadata Generation (Dadan)
   - Thumbnail Generation (Recraft)
   - Video Download

## Testing

### Frontend starten:
```bash
cd dashboard/frontend
npm run dev
```

### Backend starten (parallel):
```bash
cd dashboard/backend
python app.py
```

### Browser öffnen:
```
http://localhost:5173
```

## Troubleshooting

### "Network Error" oder "Failed to fetch"
- ✅ Backend läuft auf Port 5000
- ✅ CORS ist im Backend aktiviert
- ✅ `.env.development` ist korrekt konfiguriert

### "Loading forever" (Spinner hört nicht auf)
- ✅ API-Response-Format stimmt mit TypeScript-Types überein
- ✅ Backend-Endpoint existiert und antwortet korrekt

### TypeScript Errors
- ✅ `npm install` ausführen
- ✅ TypeScript-Version überprüfen (`typescript ~5.9.3`)

---

**Status:** ✅ **Integration abgeschlossen**
**Autor:** Claude Code
**Datum:** 2025-11-15
