---
name: skill-sandbox-runtime
description: AI agent skill for sandbox runtime implementation
---

# Skill: Sandbox Runtime & OPA Governance (Etapa 4)

## 📋 Información General
* **Nombre de la Habilidad**: `sandbox-runtime-opa-gvisor`
* **Etapa del Roadmap**: Etapa 4 (Semanas 7-8)
* **Objetivo**: Aislar la ejecución de código no confiable generado por los agentes en entornos seguros con **gVisor (`runsc`)** y aplicar gobernanza declarativa de autorización mediante **Open Policy Agent (OPA / Rego)** integrado con Docker Engine y Kubernetes.
* **Stack Tecnológico**: `gVisor`, `Open Policy Agent (OPA - Rego)`, `Docker Engine`, `opa-docker-authz`

---

## 🏗️ Módulos y Patrones Arquitectónicos

### 1. gVisor: Aislamiento con Kernel en Espacio de Usuario (`runsc`)
gVisor proporciona una arquitectura de defensa en profundidad interponiendo un kernel Linux implementado en Go entre la aplicación y el host.

* **Sentry**: Kernel en espacio de usuario que intercepta y gestiona las llamadas al sistema (*syscalls*) de la aplicación en modo KVM o ptrace.
* **Gofer**: Proceso auxiliar desacoplado que abre archivos en el host a través del protocolo **9P**, evitando que el Sentry interactúe directamente con llamadas al sistema de archivos del host (`open`, `socket`).
* **Netstack**: Pila de red completa escrita en Go e integrada en el Sentry.

```yaml
# Configuración Kubernetes para Pods de Sandbox con gVisor
apiVersion: agents.x-k8s.io/v1beta1
kind: Sandbox
metadata:
  name: agent-code-interpreter
  namespace: agent-sandbox-system
spec:
  podTemplate:
    spec:
      runtimeClassName: gvisor
      containers:
      - name: python-interpreter
        image: python:3.12-slim
        command: ["python3", "-c", "import sys; print('Sandboxed under gVisor')"]
        resources:
          limits:
            cpu: "1.0"
            memory: "512Mi"
```

---

### 2. OPA & Rego: Reglas Declarativas de Autorización para Docker Engine
Regla declarativa en lenguaje **Rego** para denegar contenedores inseguros (privilegiados, con seccomp desactivado o montajes peligrosos del host).

```rego
# authz.rego - Política de autorización OPA para Docker Daemon
package docker.authz

default allow := false

# Permitir la solicitud solo si NO activa reglas de denegación
allow if {
    not deny
}

# Denegar si se intenta ejecutar en modo privilegiado
deny if {
    input.Body.HostConfig.Privileged == true
}

# Denegar si se desactiva el perfil de seguridad seccomp
deny if {
    input.Body.HostConfig.SecurityOpt[_] == "seccomp:unconfined"
}

# Denegar si se intenta montar el socket del Docker del host
deny if {
    input.Body.HostConfig.Binds[_] == "/var/run/docker.sock:/var/run/docker.sock"
}
```

---

### 3. Integración del Plugin `opa-docker-authz`
El daemon de Docker se configura para delegar las solicitudes HTTP/JSON-RPC de creación y ejecución de contenedores (`/v1.38/containers/create`) al plugin `opa-docker-authz`.

```json
// /etc/docker/daemon.json
{
  "runtimes": {
    "runsc": {
      "path": "/usr/local/bin/runsc"
    }
  },
  "authorization-plugins": ["opa-docker-authz"]
}
```

---

### 4. Wrapper Python de Invocación Segura del Sandbox
Módulo Python para lanzar contenedores sandboxed mediante la CLI de Docker forzando el runtime `runsc` y aplicando límites de recursos.

```python
import subprocess
import json

class SandboxedExecutor:
    def __init__(self, runtime: str = "runsc", memory_limit: str = "512m"):
        self.runtime = runtime
        self.memory_limit = memory_limit

    def execute_script(self, code_content: str, timeout_seconds: int = 10) -> dict:
        cmd = [
            "docker", "run", "--rm",
            f"--runtime={self.runtime}",
            f"--memory={self.memory_limit}",
            "--network=none",  # Aislamiento total de red
            "python:3.12-slim",
            "python3", "-c", code_content
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=True
            )
            return {"status": "success", "stdout": result.stdout, "stderr": result.stderr}
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Tiempo de ejecución excedido (Timeout)"}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "stdout": e.stdout, "stderr": e.stderr}
```

---

## ⚡ Guía de Ejecución y Validaciones de la Etapa
1. **Paso 1**: Verificar la instalación de `runsc` ejecutando `docker run --runtime=runsc --rm hello-world`.
2. **Paso 2**: Desplegar OPA con la política `authz.rego` y conectar el plugin `opa-docker-authz`.
3. **Paso 3**: Probar que intentos de ejecutar contenedores con `--privileged` o `--security-opt seccomp:unconfined` sean bloqueados inmediatamente por OPA.
4. **Paso 4**: Validar mediante `dmesg` dentro del contenedor que la salida certifique el aislamiento bajo el kernel de gVisor.

