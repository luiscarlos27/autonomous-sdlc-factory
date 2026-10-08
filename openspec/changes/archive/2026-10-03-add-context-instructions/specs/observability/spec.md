# Spec Delta

## Purpose

Defines kernel-to-cognitive observability correlating high-level metrics (tokens, cost) with kernel events via eBPF and exporting via OpenTelemetry.

## ADDED Requirements

### Requirement: System captures kernel-level telemetry
The system SHALL capture OS-level events using eBPF programs (C/libbpf).

#### Scenario: Trace syscalls
- **WHEN** system calls occur
- **THEN** eBPF tracer captures relevant syscalls

#### Scenario: Correlate kernel events
- **WHEN** events are captured
- **THEN** they are correlated with request/agent context

### Requirement: Export via OpenTelemetry
The system SHALL export telemetry (traces, metrics, logs) via OpenTelemetry with Prometheus/Grafana integration.

#### Scenario: Export distributed traces
- **WHEN** operations span components
- **THEN** traces are exported via OTel

#### Scenario: Export performance metrics
- **WHEN** metrics are collected
- **THEN** they are exposed to Prometheus
