---
name: skill-intent-engine
description: AI agent skill for intent engine implementation
---

# Skill: Intent Engine & Structural Validation (Etapa 1)

## 📋 Información General
* **Nombre de la Habilidad**: `intent-engine-structural-validation`
* **Etapa del Roadmap**: Etapa 1 (Semanas 1-2)
* **Objetivo**: Garantizar la clasificación de intenciones de usuario, extracción estructurada sin errores de parsing mediante reintentos automáticos, optimización declarativa de prompts mediante compilación/finetuning y validación robusta en CI/CD.
* **Stack Tecnológico**: `Pydantic V2`, `Instructor`, `DSPy`, `PyTest`

---

## 🏗️ Módulos y Patrones Arquitectónicos

### 1. Pydantic V2: Esquemas Estrictos y Validación de Funciones
Pydantic V2 aporta un motor en Rust (`pydantic-core`) con rendimiento de orden de magnitud superior.
* **BaseModel con Discriminadores**: Para clasificaciones multitarea.
* **`@validate_call`**: Decorador para forzar tipado estricto en funciones de pipeline de agentes.
* **Validación de Campo con Docstrings**: Docstrings y metadatos `Field(description=...)` se inyectan en el prompt del LLM para guiar la generación de código/JSON.

```python
from pydantic import BaseModel, Field, validate_call
from typing import Literal

class IntentClassification(BaseModel):
    """
    Clasificación de intención del usuario y extracción de contexto.
    """
    chain_of_thought: str = Field(
        ..., 
        description="Razonamiento paso a paso antes de determinar la intención principal."
    )
    intent: Literal["TECHNICAL_QUERY", "CODE_EXECUTION", "SYSTEM_COMMAND", "UNKNOWN"] = Field(
        ...,
        description="Categoría principal de la solicitud del usuario."
    )
    confidence_score: float = Field(
        ...,
        ge=0.0, le=1.0,
        description="Puntaje de confianza estimado (0.0 a 1.0)."
    )

@validate_call
def process_user_intent(query: str, classification: IntentClassification) -> dict:
    return {
        "query": query,
        "intent": classification.intent,
        "confidence": classification.confidence_score
    }
```

---

### 2. Instructor: Extracción Estructurada con Bucle de Reintentos Automático
`Instructor` envuelve los clientes de proveedores de LLM (`OpenAI`, `Anthropic`, etc.) reemplazando los esquemas manuales por modelos Pydantic y gestionando los errores de validación mediante un ciclo de retroalimentación en tiempo de ejecución (`max_retries`).

* **Manejo de Errores en Reintento**: Si el LLM genera un valor fuera de rango o un JSON malformado, `Instructor` reinyecta la excepción devuelta por Pydantic en el contexto del LLM para autocorregirse.

```python
import instructor
from openai import OpenAI

# Creación del cliente envuelto con Instructor
client = instructor.from_provider("openai/gpt-4o-mini")

def extract_intent_with_retry(user_prompt: str) -> IntentClassification:
    response: IntentClassification = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=IntentClassification,
        max_retries=3,
        messages=[
            {"role": "system", "content": "Eres un motor de intención preciso. Analiza la entrada del usuario."},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response
```

---

### 3. DSPy: Compilación Declarativa y Optimización de Prompts
DSPy abstrae las llamadas a los LLMs convirtiendo las plantillas de prompts en grafos de transformación de texto declarativos mediante `Signature`, `Predict`, `ChainOfThought` y teleprompters/optimizadores (`BootstrapFewShot`, `BootstrapFinetune`).

* **Firma Declarativa (`dspy.Signature`)**: Define el *qué* (contrato de entrada/salida) sin codificar cadenas de texto rígidas.
* **Optimizadores (Teleprompters)**: Evalúan trazas del programa contra una métrica y generan automáticamente demostraciones *few-shot* o ajustan pesos del modelo.

```python
import dspy

# 1. Definición de la Firma Declarativa
class IntentSignature(dspy.Signature):
    """Clasifica la intención técnica del usuario y provee justificación detallada."""
    user_query = dspy.InputField(desc="Texto ingresado por el usuario")
    chain_of_thought = dspy.OutputField(desc="Pasos lógicos de análisis")
    category = dspy.OutputField(desc="Clase asignada: TECHNICAL_QUERY, CODE_EXECUTION, SYSTEM_COMMAND")

# 2. Definición del Módulo de DSPy
class IntentClassifierModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought(IntentSignature)

    def forward(self, user_query):
        return self.prog(user_query=user_query)

# 3. Compilación con BootstrapFewShot contra una métrica
def intent_metric(gold, pred, trace=None):
    return gold.category.strip().upper() == pred.category.strip().upper()

# Teleprompter para optimizar prompts automáticamente
teleprompter = dspy.BootstrapFewShot(metric=intent_metric, max_bootstrapped_demos=4)
# trainset = [dspy.Example(user_query="...", category="...").with_inputs("user_query"), ...]
# compiled_classifier = teleprompter.compile(IntentClassifierModule(), trainset=trainset)
```

---

### 4. PyTest: Pruebas de Comportamiento para Flujos de LLM
Garantiza que la suite de integración valide tanto el cumplimiento del esquema como la semántica de la respuesta sin ocultar fallas en entornos CI/CD.

```python
import pytest
from pydantic import ValidationError

def test_intent_classification_schema_valid():
    data = {
        "chain_of_thought": "El usuario solicita ejecutar un script en Python.",
        "intent": "CODE_EXECUTION",
        "confidence_score": 0.95
    }
    instance = IntentClassification(**data)
    assert instance.intent == "CODE_EXECUTION"
    assert instance.confidence_score == 0.95

def test_intent_classification_invalid_score():
    data = {
        "chain_of_thought": "Análisis fallido",
        "intent": "TECHNICAL_QUERY",
        "confidence_score": 1.5  # Invalido (> 1.0)
    }
    with pytest.raises(ValidationError):
        IntentClassification(**data)
```

---

## ⚡ Guía de Ejecución y Validaciones de la Etapa
1. **Paso 1**: Crear los esquemas Pydantic V2 en `src/schemas/intent.py`.
2. **Paso 2**: Implementar el extractor de `Instructor` con soporte para `max_retries=3`.
3. **Paso 3**: Construir la firma e integrar el pipeline de DSPy en `src/engine/dspy_intent.py`.
4. **Paso 4**: Ejecutar `pytest tests/test_intent_engine.py -v` para verificar la cobertura de tipos y la resiliencia ante errores de formato.

