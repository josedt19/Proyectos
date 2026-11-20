# MatchMind

Plataforma de fútbol con predicciones, modo entrenador y retos. Proyecto de 1.º de ASIR. Datos de demostración.

## Arrancar (PowerShell, en la carpeta del proyecto)
    Copy-Item .env.example .env      # y edita .env con tu contraseña
    docker compose config            # valida la configuración
    docker compose up -d --build
    docker compose ps
    curl.exe http://localhost:8000/api/health
    curl.exe http://localhost:8000/api/health/db
    docker compose exec api alembic upgrade head

## Detener
    docker compose stop              # pausa, conserva datos
    docker compose down              # elimina contenedores, conserva datos
    docker compose down -v           # BORRA también la base de datos

Documentación interactiva de la API: http://localhost:8000/docs
