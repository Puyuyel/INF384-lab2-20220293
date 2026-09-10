# 1.1 Defectos (reordenados — defecto 1 = falta más relevante)

1. Instalación desde `requirements.txt` (sin lockfile) — `/.github/workflows/pipeline.yml` (líneas 23-26 y 53-56).
	Consecuencia: no se garantiza reproducibilidad de dependencias entre ejecuciones.
2. Ausencia de caché de dependencias — `/.github/workflows/pipeline.yml` (líneas 23-26 y 53-56).
	Consecuencia: CI más lento e inestable por reinstalaciones completas.
3. Quality Gate no bloquea la publicación — `/.github/workflows/pipeline.yml` (líneas 31-39).
	Consecuencia: código de baja calidad puede llegar a publicarse.
4. Publicación incondicional y artefacto no identificado — `/.github/workflows/pipeline.yml` (líneas 41-66) y `pyproject.toml` (línea 7).
	Consecuencia: pérdida de trazabilidad y publicación desde ramas no deseadas.

# 1.2 Defecto que explica la duración

El defecto que explica el tiempo registrado es el defecto 3 (ausencia de caché de dependencias), ya que obliga a reinstalar las dependencias en cada ejecución. Sustento: tiempos medidos en `docs/linea-base.md`: 1m10s, 1m14s, 55s (media ≈ 1m6s).

# 1.4 Métrica DORA
Métricas alcanzables sin despliegue: `Tasa de fallos en cambios` y `Lead Time de cambios`.
Por qué: `Lead Time de cambios` mide la velocidad desde commit/PR hasta build/merge exitoso y mejora con cache, lockfile y builds rápidos.
Elegida: `Lead Time de cambios` — reducir el tiempo desde el cambio hasta el build/merge exitoso.

# 1.5 Métrica proxy
Métrica a medir: duración media/mediana del pipeline (tiempo de ejecución del workflow) en segundos.
Por qué: el pipeline es la parte que afecta directamente el Lead Time; reducir su duración acelera delivery.
Cómo: usar los tiempos registrados en `docs/linea-base.md` y estadísticas de runs (media/mediana).

