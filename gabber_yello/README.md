# Gabber Yello staging test route

Gabber Yello is exposed only through the staging backend route `POST /gabber-yello/chat`.

The route reuses Yello Core, selective MHJH knowledge and database-backed conversation history, but prefixes the supplied session id with `gabber-yello-test:` so test conversations stay isolated from YellowMind history.

Reset test history with `POST /gabber-yello/reset` using the same external session id.

This route is intentionally backend-only for step 8. No live or frontend wiring is included yet.
