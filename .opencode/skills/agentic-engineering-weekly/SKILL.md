---
name: agentic-engineering-weekly
description: Weekly practice skill for transforming engineers into agent orchestrators with governance and portfolio execution
---

# SKILL: Agentic Engineering Weekly Practice & Portfolio Execution

---
name: agentic-engineering-weekly
description: Guía de ejecución semanal y definición de habilidad (Skill) para transformar a un ingeniero de software en un Arquitecto de Intenciones y Orquestador de Agentes mediante proyectos prácticos, observabilidad, control de deriva y modelos AaaS.
---

## Descripción General
Esta habilidad proporciona un flujo de trabajo estructurado paso a paso para ejecutar el plan de entrenamiento práctico semanal en **Ingeniería Agéntica (2026–2030)**. Permite a un desarrollador o agente de IA orquestar laboratorios, verificar la calidad del código, controlar el *Agent Drift*, prevenir el *Efecto Bola de Nieve* y empaquetar soluciones en productos comerciales B2B / AaaS.

---

## Flujo de Trabajo Semanal Estándar

### Paso 1: Configuración del Entorno y Preparación del SPRINT
Para cada nueva semana de entrenamiento:
1. Crear una rama en el repositorio de trabajo local: `git checkout -b feature/semana-[N]-[modulo-slug]`.
2. Definir el estado compartido (*Shared State*) del laboratorio en un archivo de configuración (`config.yaml` o Pydantic Schema).
3. Establecer los Criterios de Aceptación (*Definition of Done*) y la suite de pruebas unitarias/de integración que servirán como "verdad absoluta" para los agentes.

---

## Mapeo de Habilidades y Laboratorios por Módulo

### MÓDULO 1: Orquestación de Enjambres Multiaagente (Multi-Agent Swarms)
* **Objetivo:** Construir una arquitectura jerárquica de 2 niveles (Router + Especialistas) con estado compartido.
* **Stack Recomendado:** LangGraph, AutoGen v0.4, CrewAI, Model Context Protocol (MCP).
* **Protocolo de Ejecución:**
  1. Instanciar el `RouterAgent` con permisos exclusivos de lectura y planificación (sin side-effects).
  2. Definir los agentes especializados: `DeveloperAgent` (generación ReAct) y `QAAgent` (auditoría de regresiones).
  3. Implementar un bucle de comunicación en grafo con un máximo de 3 reintentos antes de escalamiento a `Human-in-the-Loop`.
* **Criterio de Salida (DoD):** El enjambre resuelve tareas de código multinodo pasando el 100% de los testbeds sin entablar bucles infinitos de decisión.

---

### MÓDULO 2: Memoria a Largo Plazo y Control de Context Drift
* **Objetivo:** Implementar arquitecturas de tri-memoria y compresión periódica para prevenir la degradación conversacional.
* **Stack Recomendado:** Qdrant / ChromaDB, MemGPT / Letta, Hermes Agent FTS5 Search.
* **Protocolo de Ejecución:**
  1. Configurar capas de memoria: Episódica (interacciones pasadas), Semántica (hechos/RAG) y Procedimental (*Skills* reutilizables).
  2. Implementar un pipeline de **Episodic Memory Consolidation (EMC)** que resuma historiales cuando la ventana supere el 80% de su capacidad.
  3. Aplicar *Adaptive Behavioral Anchoring (ABA)* reinyectando ejemplos *few-shot* iniciales si el puntaje ASI decae.
* **Criterio de Salida (DoD):** Mantener la coherencia del agente y una tasa de respuesta válida tras más de 100 turnos consecutivos de interacción.

---

### MÓDULO 3: Observabilidad Centrada en Trazas (AgentOps)
* **Objetivo:** Bridging the *Semantic Gap* entre intenciones en prompts y acciones del sistema operativo mediante eBPF.
* **Stack Recomendado:** AgentSight (eBPF), Langfuse / LangSmith, OpenTelemetry GenAI, Python/Rust.
* **Protocolo de Ejecución:**
  1. Desplegar sondas eBPF en el kernel para interceptar llamadas del sistema (`execve`, `openat2`, `connect`) e intercepciones TLS.
  2. Construir el motor de correlación temporal (ventana de 100-500 ms) para vincular respuestas del LLM con sus procesos hijo.
  3. Configurar un `Observer LLM` secundario o sonda de estados ocultos (*Cognitive Companion*) para clasificar anomalías en tiempo real.
* **Criterio de Salida (DoD):** Capturar y alertar en tiempo real inyecciones de prompts indirectas o bucles de razonamiento con < 3% de overhead.

---

### MÓDULO 4: Control del Efecto Bola de Nieve y Benchmarking EvoClaw
* **Objetivo:** Prevenir la acumulación de regresiones en desarrollos de larga duración.
* **Stack Recomendado:** Docker Sandboxes, Pytest / Jest, Pydantic, DeepCommit / EvoClaw Pipeline.
* **Protocolo de Ejecución:**
  1. Construir un entorno aislado de ejecución (*sandbox*) sin acceso no autorizado al sistema anfitrión.
  2. Configurar la métrica duplicada: **Recall** (avance de características) y **Precision** (ausencia de regresiones).
  3. Ejecutar verificaciones automáticas *develop-in-place, evaluate-in-isolation* descartando parches que degraden tests P2P.
* **Criterio de Salida (DoD):** El agente completa 5 hitos consecutivos de desarrollo manteniendo un Precision de tests pasados > 90%.

---

### MÓDULO 5: Contratos de Herramientas, Sandboxing y Guardrails
* **Objetivo:** Restringir el espacio de acción agéntico mediante esquemas tipados y políticas como código.
* **Stack Recomendado:** Guardrails AI, Llama Guard, Firecracker / Wasm, Policy-as-Code (OPA/Cedar).
* **Protocolo de Ejecución:**
  1. Definir esquemas tipados Pydantic para cada llamada a herramienta (*Tool Contracts*).
  2. Implementar un gateway con barreras de permisos (*Allowlists*) y validación de pre/post-condiciones.
  3. Establecer presupuestos de cómputo en inferencia (*test-time compute budgets*) y confirmación humana obligatoria para operaciones irreversibles (escrituras/pagos/despliegues).
* **Criterio de Salida (DoD):** Invocaciones no autorizadas o mal formateadas son interceptadas y bloqueadas antes de producir efectos secundarios en el entorno.

---

### MÓDULO 6: Cómputo en Tiempo de Inferencia y Agentes Auto-Evolutivos
* **Objetivo:** Habilitar la deliberación adaptativa y la síntesis autónoma de herramientas.
* **Stack Recomendado:** Tree of Thoughts (ToT), Reflexion, TaskCraft Dataset, Auto-Evolve Framework.
* **Protocolo de Ejecución:**
  1. Implementar la búsqueda en árbol de pensamientos (*Tree of Thoughts*) con poda por verifiadores cuando la incertidumbre sea alta.
  2. Configurar el módulo `Code-Gen LLM` para sintetizar nuevas herramientas Python en tiempo de ejecución ante fallas del agente operativo.
  3. Ejecutar el ciclo de clonación, entrenamiento en currículum y reemplazo cuando $\Delta_{\text{perf}} \ge \epsilon_{\text{verify}}$.
* **Criterio de Salida (DoD):** El agente genera autónomamente un módulo de código reutilizable, valida su corrección y lo integra en su librería de habilidades.

---

### MÓDULO 7: Empaquetamiento AaaS y Posicionamiento Profesional
* **Objetivo:** Transformar los laboratorios en productos comerciales B2B y activos de alta visibilidad.
* **Protocolo de Ejecución:**
  1. **Estructuración AaaS:** Definir un modelo de cobro basado en resultados (ej. por ticket o PR resuelto exitosamente) con SLAs de latencia y costo.
  2. **GitHub Showcase:** Publicar el repositorio con arquitectura ASCII, instrucciones Docker `docker-compose up`, trazas de observabilidad y métricas de desempeño.
  3. **LinkedIn & CV:** Documentar en el perfil el rol de "Arquitecto de Intenciones y Orquestador Agéntico", destacando métricas cuantitativas (ej. "Reducción del 80% en deriva de comportamiento usando el marco ASI").

---

## Reglas de Oro para la Gestión del Ritmo Semanal
1. **No saltar módulos sin Criterio de Salida:** No avanzar a la semana siguiente si el arnés de pruebas del laboratorio actual no pasa de forma reproducible.
2. **Priorizar el Criterio sobre la Sintaxis:** Evaluar el trabajo agéntico por la estabilidad del sistema a largo plazo, no por la cantidad de líneas de código generadas.
3. **Mantener Logs e Historiales Limpios:** Utilizar herramientas de trazado de trazas en cada experimento para poder auditar el razonamiento del agente post-hoc.

