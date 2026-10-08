---
name: skill-test-time-compute
description: AI agent skill for test time compute implementation
---

# Skill: Capstone & Inferencia Avanzada de LLMs (Etapa 7)

## 1. Visión General y Propósito del Skill
Este skill define el procedimiento para diseñar, desplegar y evaluar **pipelines de producción basados en LLMs con razonamiento deliberado en tiempo de inferencia (*Inference-Time Compute*)** [56, 189]. Combina la exploración en árbol **Tree of Thoughts (ToT)** para la resolución de problemas complejos con marcos de evaluación automatizada **LLM-as-a-Judge** utilizando **DeepEval** para garantizar respuestas precisas, explicables y libres de sesgos [58, 59, 71, 72, 189].

---

## 2. Competencias Técnicas y Componentes Clave

### A. Razonamiento Deliberado: Tree of Thoughts (ToT)
* **Paradigma de Búsqueda en Árbol**: Formulación del razonamiento como una búsqueda sobre un árbol donde cada nodo representa un estado $s = [x, z_{1\dots i}]$ con el problema inicial $x$ y una secuencia de "pensamientos" $z_i$ [56, 190, 192].
* **Generador de Pensamientos ($G$)**:
  * *Sample i.i.d.*: Muestreo de pensamientos independientes mediante CoT para espacios de pensamiento ricos [193].
  * *Propose Prompt*: Generación secuencial de candidate thoughts utilizando prompts estructurados de propuesta [56, 193, 199].
* **Evaluador de Estados ($V$)**:
  * Valuación heurística directa basada en categorías (`sure` / `maybe` / `impossible`) para podar ramas inviables [56, 199].
  * Votación mayoritaria (*Majority Voting / Zero-shot Voting*) para seleccionar el mejor estado candidato entre $k$ opciones [56, 201, 209].
* **Algoritmos de Búsqueda**:
  * **Breadth-First Search (BFS)**: Exploración por niveles con ancho del árbol acotado ($b$) para problemas de planificación estructurada [57, 194, 199].
  * **Depth-First Search (DFS)**: Exploración profunda con umbral de podado (*pruning threshold*) y *backtracking* para problemas con restricciones complejas [195, 202, 203].

### B. Evaluación Automatizada: LLM-as-a-Judge & DeepEval
* **Modos de Evaluación**:
  * **Single-Output Scoring**: Evaluación de una única respuesta contra una rúbrica específica; idóneo para CI/CD y monitoreo de producción [60, 77].
  * **Pairwise Comparison**: Comparación de dos candidatos para determinar un ganador (`ArenaGEval`); idóneo para comparación de prompts y modelos [77, 94].
* **Mitigación Rigurosa de Sesgos**: Estrategias para neutralizar el sesgo de posición (*position bias*), el sesgo de verbosidad (*verbosity bias*) y el sesgo de preferencia propia (*self-preference bias*) [58, 61, 68].
* **Técnicas de Evaluación en DeepEval**:
  * **G-Eval**: Definición de criterios sintácticos/semánticos en lenguaje natural con razonamiento previo *Chain-of-Thought (CoT)* para calcular puntuaciones continuas (0 a 1) [65, 78, 79].
  * **DAGMetric**: Gráficos Acíclicos Dirigidos para árboles de decisión deterministas con reglas estrictas, puertas de entrada (*gates*) y penalizaciones específicas [78, 80, 81].
  * **JevEval**: Modelo de decisión que evalúa preguntas acotadas (`Noul`, `Score`, `Choice`) generando distribuciones de probabilidad calibradas con matemáticas fijas y sin llamadas generativas adicionales [73, 84, 93].
  * **Métricas Trajectoriales para Agentes**: Inspección completa de trazas ordenadas mediante `TaskCompletionMetric`, `StepEfficiencyMetric`, `PlanAdherenceMetric` y `PlanQualityMetric` [82, 92].
* **Calibración Humana**: Construcción de un *calibration set* de 100–500 ejemplos etiquetados por expertos para medir el acuerdo (*Cohen's kappa* / *Spearman correlation* > 75%) antes del despliegue masivo [62, 65, 68].

### C. Pipeline E2E de Inferencia y Producción
* **Arquitectura de Microservicios**: Pipelines escalables de inferencia (integración de OCR / Document AI y modelos de lenguaje) [24].
* **Integración en CI/CD y Monitoreo**:
  * Ejecución de pruebas de regresión con `assert_test` y `deepeval test run` [87, 95].
  * Monitoreo en producción con métricas referenceless (ej. `AnswerRelevancyMetric`) conectadas a plataformas de observabilidad [66, 88, 95].

---

## 3. Plan de Trabajo Paso a Paso (Semanas 13-14)

### Semana 13: Motor Tree of Thoughts e Infraestructura de Juzgamiento
1. **Implementación del Engine ToT**:
   * Construir el motor ToT en Python soportando los algoritmos **ToT-BFS** y **ToT-DFS** con prompts de propuesta y valuación en JSON [194, 195, 199].
2. **Diseño de Métricas de Juzgamiento en DeepEval**:
   * Definir métricas `GEval` con pasos de evaluación explícitos (`evaluation_steps`) y campos requeridos (`evaluation_params`) [65, 79].
   * Construir un `DAGMetric` para validación estricta de formato JSON y completitud lógica [80].

### Semana 14: Calibración, Pipeline E2E y Capstone
1. **Calibración del Juez con Dataset Humano**:
   * Crear el conjunto de calibración de 100–500 ejemplos etiquetados [62, 68].
   * Medir la correlación entre las puntuaciones del juez LLM y las etiquetas humanas, ajustando los prompts hasta superar el 75% de acuerdo [68].
2. **Integración del Pipeline Capstone End-to-End**:
   * Ensamblar la inferencia ToT, la evaluación automatizada y el envío de métricas de calidad y rendimiento al stack de observabilidad (Prometheus/Grafana) [20, 64, 95].

---

## 4. Ejemplos de Configuración y Código

### Implementación de Métrica G-Eval en DeepEval
```python
from deepeval import evaluate
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, SingleTurnParams

# Definición del caso de prueba
test_case = LLMTestCase(
    input="¿Cuál es la política de garantía para productos defectuosos?",
    actual_output="Los productos defectuosos pueden devolverse en un plazo de 30 días con recibo.",
    expected_output="Los clientes pueden devolver productos defectuosos dentro de los 30 días posteriores a la compra presentando el recibo original para un reembolso completo."
)

# Definición de la métrica de corrección semántica con G-Eval
correctness_metric = GEval(
    name="CorreccionSemantica",
    evaluation_steps=[
        "Verificar si la respuesta generada contradice la respuesta esperada.",
        "Penalizar la omisión de condiciones críticas de reembolso.",
        "Ignorar variaciones menores de estilo o redacción siempre que el sentido se preserve."
    ],
    evaluation_params=[
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.EXPECTED_OUTPUT
    ],
    threshold=0.8
)

# Ejecución de la evaluación
evaluate(test_cases=[test_case], metrics=[correctness_metric])
```

---

## 5. Criterios de Aceptación y Calidad
* **Calidad de Razonamiento**: Mejora significativa en la tasa de éxito de tareas complejas respecto a métodos sencillos CoT/IO utilizando ToT [189, 200].
* **Fiabilidad del Juez**: Correlación y acuerdo con evaluadores humanos (*Cohen's kappa* / *Spearman correlation*) **$\ge$ 75%** [68].
* **Trazabilidad y Formato**: Puntuaciones y justificaciones producidas en formato estructurado JSON con trazabilidad completa de razonamiento CoT [64, 65].

