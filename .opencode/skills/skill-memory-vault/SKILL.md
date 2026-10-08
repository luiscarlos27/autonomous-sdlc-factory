---
name: skill-memory-vault
description: AI agent skill for memory vault implementation
---

# Skill: Memory Vault & Hermes Dynamic Skill Loader (Etapa 3)

## 📋 Información General
* **Nombre de la Habilidad**: `memory-vault-hermes-loader`
* **Etapa del Roadmap**: Etapa 3 (Semanas 5-6)
* **Objetivo**: Implementar una arquitectura de memoria en dos niveles (*Hot Working Memory* en Redis y *Durable Episodic/Semantic Memory* en Pgvector/PostgreSQL) e integrar un cargador dinámico de habilidades (*Hermes Skills Dynamic Loader*) con límites estrictos contra la hinchazón de tablas (*table bloat*).
* **Stack Tecnológico**: `Pgvector (PostgreSQL)`, `Redis`, `Hermes Skills Dynamic Loader`

---

## 🏗️ Módulos y Patrones Arquitectónicos

### 1. Pgvector (PostgreSQL): Memoria Semántica Durable y Optimización de Páginas
PostgreSQL gestiona páginas atómicas de 8192 bytes (8 KiB). Vectores de alta dimensión (ej. 1536 dimensiones x 4 bytes = 6 KiB o 3072 dimensiones = 12 KiB) exceden el espacio de página e invocan la tabla TOAST, introduciendo latencia I/O.

* **Estrategia HNSW & Cuantización**: Uso de índices **HNSW** para alta recuperación (*recall*) y soporte de cuantización binaria o `halfvec` para reducir la huella de memoria RAM.
* **Escaneo Iterativo de Índices (pgvector 0.8+)**: Mejora el recall en consultas con filtros `WHERE` muy selectivos.

```sql
-- Configuración de extensión y tabla de vectores con metadatos JSONB
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS agent_semantic_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id VARCHAR(64) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB NOT NULL,
    embedding vector(1536) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Creación de Índice HNSW optimizado para distancia Coseno
CREATE INDEX IF NOT EXISTS idx_agent_memory_hnsw 
ON agent_semantic_memory 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 64);
```

---

### 2. Redis: Capa de Memoria Caliente de Sub-Milisegundo y Caché Semántica
En una arquitectura de dos niveles, Redis actúa como el almacén de estado activo de sesión (<1 ms de latencia) y motor de caché semántica para reducir costos de tokens de LLM.

```python
import redis.asyncio as redis
import json
from datetime import timedelta

class HotMemoryVault:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.ttl = timedelta(hours=24)

    async def set_working_context(self, session_id: str, context: dict):
        key = f"agent:hot_state:{session_id}"
        # Serialización compacta
        payload = json.dumps(context)
        await self.redis.setex(key, self.ttl, payload)

    async def get_working_context(self, session_id: str) -> dict:
        key = f"agent:hot_state:{session_id}"
        data = await self.redis.get(key)
        return json.loads(data) if data else {}
```

---

### 3. Hermes Skills Dynamic Loader
El patrón de **Hermes Agent** pre-carga únicamente los metadatos de cabecera YAML (*frontmatter* de 20–50 tokens) de las habilidades registradas dentro del prompt de sistema. El cuerpo completo con las instrucciones e invocaciones del `SKILL.md` solo se inyecta dinámicamente cuando el agente decide activar la habilidad.

```
/workspace/skills/
├── data-craft/
│   └── SKILL.md
├── pdf-creation/
│   └── SKILL.md
```

```python
import yaml
import re
from pathlib import Path

class HermesSkillLoader:
    def __init__(self, skills_dir: str):
        self.skills_dir = Path(skills_dir)
        self.registered_skills = {}
        self._preload_skill_headers()

    def _preload_skill_headers(self):
        """Lee únicamente el YAML frontmatter para minimizar tokens en el prompt inicial."""
        for path in self.skills_dir.glob("*/SKILL.md"):
            content = path.read_text(encoding="utf-8")
            match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
            if match:
                frontmatter = yaml.safe_load(match.group(1))
                self.registered_skills[frontmatter["name"]] = {
                    "description": frontmatter.get("description", ""),
                    "file_path": path
                }

    def get_system_prompt_skills_summary(self) -> str:
        """Retorna un resumen compacto de habilidades para el prompt de sistema."""
        summary = "Habilidades disponibles:\n"
        for name, info in self.registered_skills.items():
            summary += f"- {name}: {info['description']}\n"
        return summary

    def load_full_skill_instructions(self, skill_name: str) -> str:
        """Inyecta las instrucciones completas solo bajo demanda."""
        if skill_name in self.registered_skills:
            path = self.registered_skills[skill_name]["file_path"]
            return path.read_text(encoding="utf-8")
        raise ValueError(f"Habilidad '{skill_name}' no encontrada.")
```

---

### 4. Disciplina de Almacenamiento JSONB (Prevención de Table Bloat)
Volcar logs masivos de herramientas (ej. archivos de 50MB) directamente en columnas `JSONB` de Postgres causa una violenta fragmentación de páginas y sobrecarga del proceso `Autovacuum`.

* **Regra de Truncamiento**: Aplicar truncamiento estricto en la capa de aplicación para salidas de herramientas que superen los 100 KB antes de persistir en PostgreSQL.

```python
def sanitize_tool_output_for_db(raw_output: str, max_chars: int = 10000) -> str:
    if len(raw_output) > max_chars:
        return raw_output[:max_chars] + f"\n... [TRUNCADO: {len(raw_output) - max_chars} caracteres omitidos para mantener la salud de la DB]"
    return raw_output
```

---

## ⚡ Guía de Ejecución y Validaciones de la Etapa
1. **Paso 1**: Ejecutar las migraciones SQL para crear la extensión `pgvector` e índices `HNSW`.
2. **Paso 2**: Probar la velocidad de escritura y lectura del `HotMemoryVault` en Redis (<1ms).
3. **Paso 3**: Verificar el ahorro de tokens en el prompt del sistema utilizando `HermesSkillLoader`.
4. **Paso 4**: Validar que las salidas de las herramientas se trunquen correctamente antes de insertarse en las tablas `JSONB` de PostgreSQL.

