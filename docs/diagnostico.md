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

# 1.3 El vínculo con su caso
* **Caso elegido:** Caso 2 - Financiera Los Andes (Gobierno tardío).
* **Defecto que ataca la restricción:** Defecto 3 (Quality Gate no bloquea la publicación).
* **Dato del VSM:** En el mapa de flujo de valor, la etapa de "Revisión de seguridad manual" requiere solo 6 horas de trabajo, pero genera una espera monumental de **120 horas**. Además, la lectura detalla que 11 de los 14 hallazgos de seguridad provienen de dependencias desactualizadas.
* **Vínculo analítico:** Al corregir el Defecto 3 obligando al Quality Gate de SonarQube a romper la compilación si hay vulnerabilidades, logramos automatizar el análisis (análisis estático y de composición). Esto permite aplicar *shift-left* a la seguridad, descubriendo estos problemas en minutos durante el PR, y eliminando la necesidad de la enorme cola de 120 horas al final del flujo [cite: 1].

# 1.4 Métrica DORA
Métricas alcanzables sin despliegue: `Tasa de fallos en cambios` y `Lead Time de cambios`.
Por qué: `Lead Time de cambios` mide la velocidad desde commit/PR hasta build/merge exitoso y mejora con cache, lockfile y builds rápidos.
Elegida: `Lead Time de cambios` — reducir el tiempo desde el cambio hasta el build/merge exitoso.

# 1.5 Métrica proxy
Métrica a medir: duración media/mediana del pipeline (tiempo de ejecución del workflow) en segundos.
Por qué: el pipeline es la parte que afecta directamente el Lead Time; reducir su duración acelera delivery.
Cómo: usar los tiempos registrados en `docs/linea-base.md` y estadísticas de runs (media/mediana).

## 4.1 Medición posterior
- Línea base (proxy = duración del pipeline): `docs/linea-base.md` registra 1m10s, 1m14s, 55s → mediana = 70s.
- Después de la intervención: ejecución manual registrada 1m30s (90s).
- Qué cambió: la duración aumentó 20s (≈ +28.6%). Nota: la primera ejecución posterior incluye calentamiento de caché; hay que medir varias ejecuciones para ver efecto estable.

## 4.2 Justificación de la versión
- Versión declarada: `1.2.1` en `pyproject.toml` (campo `version`).
- Commits que sostienen la versión: historial relevante en `pyproject.toml` (ej.: `b7e44ce`, `0b981ca`, `4e0df78`) y el commit actual de trabajo `8a00d2f` que introdujo cambios (parche) en `src/despachos/pedidos.py` (se hizo un commit posterior para arreglar la versión y publicar la versión final del diagnóstico).

## 4.3 Lo que no se resolvió
- Limitación principal: el calentamiento del caché en la primera ejecución (cache miss) hace que la primera corrida no refleje la mejora.
- Qué haría falta: ejecutar varias corridas consecutivas para medir la mediana una vez el caché está caliente, o mejorar la estrategia de cache (claves deterministas/restore primary) y/o usar runners persistentes.

## 4.4 Declaración de uso de IA generativa
- Se usó asistencia de IA para redactar el diagnóstico y proponer cambios en el pipeline y la documentación.
- Propósito: identificación de defectos, redacción concisa y propuestas de corrección.
- Prompts (resumen): "Analiza .github/workflows/pipeline.yml y enumera los principales defectos respecto a reproducibilidad, cache, quality gate y publicación"; "Redacta breve diagnóstico y medidas recomendadas".

