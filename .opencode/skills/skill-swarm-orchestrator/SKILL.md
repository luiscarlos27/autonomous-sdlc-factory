---
name: skill-swarm-orchestrator
description: AI agent skill for swarm orchestrator implementation
---

# Skill: Swarm Orchestration & MCP Integration (Etapa 2)

## 📋 Información General
* **Nombre de la Habilidad**: `swarm-orchestration-mcp-redis`
* **Etapa del Roadmap**: Etapa 2 (Semanas 3-4)
* **Objetivo**: Orquestar agentes autónomos mediante grafos de estado dirigido (`LangGraph`), integrar herramientas y servicios distribuidos mediante el estándar `Model Context Protocol (MCP)` y garantizar la persistencia de estado y memoria a través de `Redis Checkpoint` evitando vulnerabilidades de deserialización y desbordamiento de contexto.
* **Stack Tecnológico**: `LangGraph`, `Model Context Protocol (MCP)`, `Redis Checkpoint (langgraph-checkpoint-redis)`

---

## 🏗️ Módulos y Patrones Arquitectónicos

### 1. LangGraph: Orquestación Basada en Grafos de Estado Dirigido
LangGraph modela flujos de trabajo agénticos complejos como grafos dirijidos acíclicos o cíclicos (DAGs/DCGs) utilizando un `StateGraph`.

```python
from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages

# 1. Definición del Estado del Grafo
class SwarmState(TypedDict):
    messages: Annotated[List[dict], add_messages]
    next_agent: str
    task_completed: bool

# 2. Nodos de Ejecución
async def router_agent(state: SwarmState):
    messages = state["messages"]
    last_message = messages[-1]["content"] if messages else ""
    
    if "código" in last_message.lower():
        return {"next_agent": "code_agent", "task_completed": False}
    return {"next_agent": "general_agent", "task_completed": False}

async def code_agent(state: SwarmState):
    # Simulación de ejecución del agente de código
    return {
        "messages": [{"role": "assistant", "content": "Código procesado exitosamente."}],
        "task_completed": True
    }

async def general_agent(state: SwarmState):
    return {
        "messages": [{"role": "assistant", "content": "Consulta general respondida."}],
        "task_completed": True
    }

# 3. Construcción y Enrutamiento del Grafo
workflow = StateGraph(SwarmState)
workflow.add_node("router", router_agent)
workflow.add_node("code_agent", code_agent)
workflow.add_node("general_agent", general_agent)

workflow.add_edge(START, "router")

def route_decision(state: SwarmState):
    if state["task_completed"]:
        return END
    return state["next_agent"]

workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "code_agent": "code_agent",
        "general_agent": "general_agent",
        END: END
    }
)
workflow.add_edge("code_agent", END)
workflow.add_edge("general_agent", END)
```

---

### 2. Integración MCP (Model Context Protocol)
El protocolo MCP estandariza la comunicación de dos vías entre clientes agénticos y servidores distribuidos de recursos mediante JSON-RPC 2.0 sobre encodificación UTF-8.

* **Estructura de Tres Niveles**: Herramientas (`Tools`), Recursos (`Resources`) y Prompts (`Prompts`).
* **Descubrimiento Dinámico**: Invocación mediante `MultiServerMCPClient` sin requerir adaptadores ad-hoc por herramienta.

```python
# Protocolo MCP - Ejemplo de cliente de orquestación de herramientas distribuidas
from typing import Any, Dict

class MCPToolAdapter:
    """
    Adaptador para descubrir e invocar herramientas expuestas por servidores MCP
    siguiendo la especificación JSON-RPC 2.0.
    """
    def __init__(self, server_uri: str):
        self.server_uri = server_uri

    async def list_tools() -> List[Dict[str, Any]]:
        # Solicitud JSON-RPC 2.0 list_tools
        return [
            {"name": "execute_sandbox_code", "description": "Ejecuta código de forma aislada en gVisor"}
        ]

    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        # Envío de request JSON-RPC 2.0 sobre UTF-8
        return {"status": "success", "output": "Resultado de ejecución"}
```

---

### 3. Persistencia de Estado con Redis Checkpoint & Seguridad
`langgraph-checkpoint-redis` provee dos primitivas clave:
1. **`AsyncRedisSaver`**: Persistencia a nivel de hilo (*short-term memory*).
2. **`RedisStore`**: Almacenamiento episódico y memoria semántica entre hilos (*cross-thread long-term memory*).

#### 🛡️ Mitigación de Vulnerabilidades Críticas de Checkpointers (RCE & SQLi)
* **CVE-2025-67644 & CVE-2026-28277**: Inyección SQL y deserialización insegura de objetos `msgpack` en checkpointers SQLite/Redis que permitían RCE.
* **Mitigación**: Forzar la actualización a `@langchain/langgraph-checkpoint-redis >= 1.0.2`, `langgraph-checkpoint-sqlite >= 3.0.1` y `langgraph >= 1.0.10`, además de sanitizar los filtros en `get_state_history()`.

```python
from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from langgraph.store.redis.aio import AsyncRedisStore

# Inicialización segura de Checkpointer y Store compartiendo conexión
async def init_redis_persistence(redis_url: str):
    # Checkpointer para persistencia por hilo
    checkpointer = AsyncRedisSaver(redis_url=redis_url)
    await checkpointer.asetup()

    # Store para memoria de largo plazo con búsqueda vectorial integrada
    store = AsyncRedisStore(redis_url=redis_url)
    await store.asetup()

    # Compilación del grafo con el checkpointer
    app = workflow.compile(checkpointer=checkpointer, store=store)
    return app
```

---

## ⚡ Guía de Ejecución y Validaciones de la Etapa
1. **Paso 1**: Asegurar que las dependencias estén actualizadas para mitigar CVEs: `pip install "langgraph>=1.0.10" "langgraph-checkpoint-redis>=1.0.2"`.
2. **Paso 2**: Implementar el grafo de orquestación en `src/orchestration/swarm_graph.py`.
3. **Paso 3**: Configurar los conectores MCP en `src/mcp/client_adapter.py`.
4. **Paso 4**: Validar la recuperación ante interrupciones ejecutando un hilo con un `thread_id` en Redis e interrumpiendo el flujo para comprobar la restauración de checkpoints.

