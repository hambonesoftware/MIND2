# Default Config Values (PoC)

Backend defaults:
- tempo: 120
- time_signature: "4/4"
- loop_bars: 1
- division: 16
- anchor_midi: 60
- velocity scale: 0..1

Frontend defaults:
- auto-start transport on first sound: allowed (document behavior)
- debounce: 500ms
- swap boundary: 1 measure ("1m")

CORS:
- allow `http://localhost:5173` (vite default) or the configured dev origin

