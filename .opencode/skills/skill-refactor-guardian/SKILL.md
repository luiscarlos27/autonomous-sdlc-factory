---
name: skill-refactor-guardian
description: AI agent skill for refactor guardian implementation
---

# Skill: Refactor Guardian y Testing Mutacional (Etapa 6)

## 1. Visión General y Propósito del Skill
Este skill establece la metodología para construir un **Refactor Guardian**, una herramienta automatizada de protección de código en pipelines de CI/CD [2, 120, 138]. Su objetivo es verificar sintácticamente las refactorizaciones de código mediante **Tree-sitter AST** y garantizar la preservación rigurosa del comportamiento de las suites de pruebas mediante **Testing Mutacional (Mutmut)** e **Integración Continua en GitHub Actions** [3, 5, 13, 112, 113, 120, 152].

---

## 2. Competencias Técnicas y Componentes Clave

### A. Parsing Sintáctico y Refactorización con Tree-sitter AST
* **Navegación e Inspección Estructurada**: Uso de **Tree-sitter** para generar árboles de sintaxis abstracta (AST) rápidos, tolerantes a errores e incrementales para Python y múltiples lenguajes [11, 13, 14].
* **Consultas Sintácticas (S-Expression Queries)**:
  * Definición de patrones Lisp-like para identificar definiciones de funciones, bloques de código, tipos de nodos y llamadas a métodos [15, 185].
  * Traversals de árboles para análisis semántico, extracción de dependencias y construcción de grafos de llamadas [10, 187].
* **Transformaciones Sintácticas**: Modificación de código a nivel AST utilizando `tree.edit` para refactorizaciones precisas (renombrado de identificadores, reestructuración sintáctica) [15, 187].

### B. Testing Mutacional con Mutmut (Preservación del Comportamiento)
* **Concepto de Testing Mutacional**: Inyección sintáctica de pequeñas fallas (*mutantes*) como sustitución de operadores (`+` $\rightarrow$ `-`, `>=` $\rightarrow$ `>`) o retornos (`return 0` $\rightarrow$ `return 1`) para evaluar la efectividad de la suite de pruebas [2, 121, 150].
* **Evaluación del Estado de Mutantes**:
  * **Killed Mutants**: Mutantes detectados por las pruebas (fallo esperado) [112, 121].
  * **Survived Mutants**: Mutantes no detectados que revelan brechas en las aserciones, puntos ciegos en los bordes o código redundante [112, 121, 151].
* **Configuración Avanzada de Mutmut en Python**:
  * Ejecución incremental y persistente basada en caché (`.mutmut-cache` / `mutmut run`) [4, 152, 154].
  * Filtrado de ruido sintáctico con `do_not_mutate_patterns` (expresiones regulares para ignorar logs o excepciones) y pragmas de exclusión en código (`# pragma: no mutate`) [156, 157].
  * Filtrado de mutantes sintácticamente inválidos integrando verificadores estáticos de tipos (`mypy` / `pyrefly`) mediante `type_check_command` [157].
  * Inspección interactiva con `mutmut browse` y re-aplicación a disco para depuración con `mutmut apply` [152, 155].

### C. Automatización en CI/CD con GitHub Actions
* **Estrategia de Caching Persistente**: Uso de `actions/cache/restore` y `actions/cache/save` sobre la carpeta `.mutmut-cache` utilizando *cache keys* basadas en hashes de archivos para permitir ejecuciones incrementales súper rápidas [5].
* **Análisis Enfocado en Commits (*Git Diff*)**: Ejecución de mutaciones únicamente sobre las líneas y archivos modificados en la rama (*feature branch / pull request*) en lugar de re-evaluar todo el repositorio [133, 139, 158].
* **Generación de Artefactos y Reportes**: Generación automática de reportes HTML (`mutmut html`) y su publicación como artefactos del flujo de CI/CD (`actions/upload-artifact`) [3, 5].

---

## 3. Plan de Trabajo Paso a Paso (Semanas 11-12)

### Semana 11: Parsing con Tree-sitter y Testing Mutacional Local
1. **Desarrollo del Parser con Tree-sitter**:
   * Implementar un script en Python que cargue la gramática `tree-sitter-python`, parsee archivos fuente y extraiga la estructura de nodos mediante consultas S-expression [13, 15, 187].
2. **Configuración de Mutmut en el Proyecto**:
   * Configurar `pyproject.toml` especificando `source_paths`, patrones a omitir y comando de *type-checking* [153, 157].
   * Realizar la primera corrida local con `mutmut run`, analizar los mutantes sobrevivientes en `mutmut browse` y ajustar los tests [154, 155].

### Semana 12: Integración Continua y Control de Calidad en GitHub Actions
1. **Construcción del Workflow de CI**:
   * Crear el archivo `.github/workflows/mutation.yml` que active las pruebas de mutación en cada *Push* o *Pull Request* [3, 5, 138].
   * Configurar los pasos de restauración y guardado de `.mutmut-cache` [5].
2. **Puertas de Calidad (*Quality Gates*)**:
   * Establecer un umbral mínimo de **Mutation Score** para bloquear fusiones de código si el nuevo código introduce mutantes sobrevivientes [123, 142].

---

## 4. Ejemplos de Configuración y Workflow

### Configuración de Mutmut en `pyproject.toml`
```toml
[tool.mutmut]
source_paths = ["src/"]
pytest_add_cli_args_test_selection = ["tests/"]
do_not_mutate_patterns = [
    'logger\.\w+',
    'raise \w+',
]
type_check_command = ["mypy", "src", "--output", "json"]
```

### Workflow de GitHub Actions (`.github/workflows/mutation.yml`)
```yaml
name: 🦠 Mutation Testing CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  mutation-test:
    runs-on: ubuntu-latest
    steps:
      - name: 📥 Checkout Repository
        uses: actions/checkout@v3

      - name: 🐍 Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: 📦 Install Dependencies
        run: |
          pip install pytest mutmut mypy

      - name: 🗃️ Restore Mutation Cache
        uses: actions/cache/restore@v3
        with:
          path: .mutmut-cache
          key: mutmut-cache-${{ github.ref_name }}-${{ hashFiles('src/**/*.py') }}
          restore-keys: |
            mutmut-cache-${{ github.ref_name }}
            mutmut-cache-main

      - name: 🦠 Run Mutation Tests
        run: |
          mutmut run --no-progress --CI
          mutmut html

      - name: 📤 Upload Mutation HTML Report
        uses: actions/upload-artifact@v3
        with:
          name: mutmut-html-report
          path: html/

      - name: 🗃️ Save Mutation Cache
        uses: actions/cache/save@v3
        with:
          path: .mutmut-cache
          key: mutmut-cache-${{ github.ref_name }}-${{ hashFiles('src/**/*.py') }}
```

---

## 5. Criterios de Aceptación y Calidad
* **Optimización de Tiempo de CI**: Tiempo de ejecución reducido significativamente gracias a la estrategia de caché incremental `.mutmut-cache` y análisis enfocado en `git diff` [4, 5, 139].
* **Mutation Score Elevado**: Garantizar un porcentaje de mutantes eliminados (*Killed Mutants*) superior al 80% en el código refactorizado [121, 123].
* **Visibilidad de Pruebas**: Generación y disponibilidad inmediata del reporte HTML interactivo tras cada ejecución en GitHub Actions [3, 5].

