---
name: skill-observability
description: AI agent skill for observability implementation
---

# Skill: Observabilidad Avanzada y Performance del Kernel (Etapa 5)

## 1. Visión General y Propósito del Skill
Este skill define el procedimiento estandarizado para diseñar, desplegar y operar un **stack de observabilidad unificado** de nivel empresarial [33, 34]. Su propósito principal es correlacionar en tiempo real la latencia y rendimiento de las aplicaciones en el espacio de usuario (*user space*) con eventos de red, I/O y llamadas al sistema en el espacio del kernel de Linux (*kernel space*) utilizando **OpenTelemetry (OTel)**, **eBPF (BCC / libbpf C)**, **Prometheus** y **Grafana** [25, 26, 45, 47].

---

## 2. Competencias Técnicas y Componentes Clave

### A. Pipeline de Telemetría con OpenTelemetry Collector
* **Configuración de Receivers y Exporters**: Despliegue de OpenTelemetry Collector intermedio que acepta telemetría OTLP vía gRPC (puerto `4317`) y HTTP (puerto `4318`) [30, 36].
* **Integración con Prometheus**:
  * Uso de `prometheusremotewrite` o `prometheusexporter` (puerto `8889`) para exponer métricas OTel en formato raspable por Prometheus [30, 175].
  * Configuración explícita de `resource_to_telemetry_conversion: enabled: true` para mapear los atributos de recursos de OTel (ej. `service.name`, `deployment.environment`) a etiquetas estándar de Prometheus [27, 30, 175, 180].
* **Procesamiento de Métricas y Trazas**:
  * `batch`: Procesamiento en lotes para optimizar el rendimiento de red [30, 37].
  * `memory_limiter`: Prevención de colapsos por Out-Of-Memory (OOM) en entornos de alta carga [30, 37, 42].
  * `resourcedetection`: Enriquecimiento automático de contexto de infraestructura (Kubernetes, Docker, Host) [37, 54].

### B. Auto-Instrumentación e Instrumentación del Kernel con eBPF
* **Programas eBPF C Personalizados (BCC vs. libbpf CO-RE)**:
  * Desarrollo e integración de sondas *kprobes* para monitorear retransmisiones TCP (`tcp_retransmit_skb`) y *uprobes* para medir latencia DNS a través de `getaddrinfo` en `libc` [50, 51, 52].
  * Evolución de scripts dinámicos en BCC hacia binarios nativos portables con **libbpf** y **BPF CO-RE (Compile Once – Run Everywhere)** aprovechando formatos BTF (*BPF Type Format*) [9, 99, 100, 172].
* **Auto-Instrumentación Sin Código (*Zero-Code*)**:
  * Despliegue de agentes eBPF (como **OpenTelemetry eBPF Instrumentation / OBI** o **Grafana Beyla**) como `DaemonSet` en Kubernetes [48, 171].
  * Configuración de capacidades requeridas en el contenedor de eBPF: `CAP_BPF`, `CAP_PERFMON`, `CAP_SYS_PTRACE` y `CAP_NET_RAW` en kernels Linux 5.8+ [48, 54, 172].
  * Captura automática de métricas RED (Rate, Errors, Duration), trazas distribuidas y protocolos de base de datos (PostgreSQL, MySQL, Redis) sin inyección de SDKs ni modificación del código fuente [171].

### C. Almacenamiento, Alertamiento y Visualización
* **Prometheus TSDB**: Configuración de ingesta directa OTLP (`--web.enable-otlp-receiver`) o raspado de colectores OTel, con políticas de retención de series temporales y evaluación de reglas PromQL [27, 28, 38].
* **Unificación en Grafana (LGTM Stack)**:
  * **Grafana Mimir**: Métricas escalables compatibles con Prometheus [165].
  * **Grafana Tempo**: Almacenamiento y trazabilidad distribuida [165].
  * **Grafana Loki**: Agregación de logs enriquecidos con `trace_id` [37, 40, 165].
  * **Grafana Pyroscope**: Profiling continuo de código a nivel de CPU y memoria [165].
* **Correlación Kernel-Aplicación**:
  * Enlazado de picos de latencia en peticiones HTTP/gRPC con retransmisiones de red TCP o demoras de I/O de disco [47, 53].

---

## 3. Plan de Trabajo Paso a Paso (Semanas 9-10)

### Semana 9: Arquitectura de Telemetría e Instrumentación Kernel
1. **Despliegue del OTel Collector**:
   * Crear el archivo de configuración `otel-collector-config.yml` especificando receivers OTLP/Prometheus y exporters hacia Prometheus y Jaeger/Loki [36, 37].
   * Levantar el stack mediante Docker Compose o manifiestos de Kubernetes [36, 40].
2. **Desarrollo e Inyección eBPF**:
   * Implementar un script eBPF C con BCC/libbpf para medir la latencia de resolución DNS con *uprobes* en `libc:getaddrinfo` [52].
   * Exportar eventos capturados en el kernel como histogramas OTel (`dns.resolution.duration`) enviando datos al colector [50, 52].

### Semana 10: Auto-Instrumentación Distribuida y Correlación
1. **Despliegue de OBI (OpenTelemetry eBPF Instrumentation)**:
   * Aplicar el `DaemonSet` de OBI con privilegios de kernel e integración con metadatos de Kubernetes [48, 171].
   * Verificar la generación automática de *spans* de trazado para llamadas HTTP, gRPC y consultas SQL [49, 171].
2. **Dashboard de Correlación y Alertas en Grafana**:
   * Configurar datasources OTLP en Grafana (Prometheus, Tempo, Loki) [164, 165].
   * Diseñar paneles correlacionados: latencia de endpoints HTTP vs. métrica `tcp.retransmissions` del kernel [50, 53].

---

## 4. Ejemplos de Configuración y Código

### Archivo de Configuración de OpenTelemetry Collector (`otel-collector-config.yml`)
```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 10s
    send_batch_size: 1024
  memory_limiter:
    check_interval: 1s
    limit_mib: 512
    spike_limit_mib: 128

exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
    namespace: "otel"
    resource_to_telemetry_conversion:
      enabled: true

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [prometheus]
```

---

## 5. Criterios de Aceptación y Calidad
* **Impacto en Rendimiento**: El consumo de CPU por parte de los programas eBPF debe mantenerse **por debajo del 1%** [54].
* **Sin Modificación de Código**: Captura exitosa de métricas y trazas en servicios existentes mediante el agente eBPF [48, 171].
* **Visibilidad Transversal**: Correlación demostrable de un evento de alta latencia de aplicación con un evento de retransmisión TCP o latencia DNS en el kernel [47, 53].

