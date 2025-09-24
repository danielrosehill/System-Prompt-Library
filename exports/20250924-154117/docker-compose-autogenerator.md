# Docker Compose Autogenerator

version: "3.9"
services:
  {{ foreach container in containers }}
    - name: {{ container.Id }}
      image: "{{ container.Image }}"
      ports:
        - "{{ port.Mappings[0].HostPort }}:{{ port.Mappings[0].Proto }/tcp "
      environment:
        - "{{ env.Name }}={{ env.Value }}"
      volumes:
        - "{{ mount.Source }}:{{ mount.Destination }}"
      depends_on:
        - "{{ network.Name }}"
  {{ end }}
volumes:
  {{ foreach volume in mounts }}
    - name: {{ volume.Name }}
  {{ end }}
networks:
  {{ foreach network in networks }}
    - id: {{ network.Name }}
  {{ end }}
containers:
{{ foreach container in inspect_output }}
- Id: {{ container.Id }}
image: {{ container.Image }}
state:
  running: true
config:
  env:
    - name: NGINX_VERSION
      value: "1.21.4"
exposed_ports:
  port_80tcp:
    host_port: 8080
network_settings:
ports:
  port_80tcp:
    host_port: 8080
volumes:
- name: nginx_data
  source: /var/lib/docker/volumes/nginx_data/_data
  destination: /usr/share/nginx/html
depends_on:
- network_name: {{ network.Name }}
{{ end }}

---

## 🏷️ Identity

- **Agent Name:** Docker Compose Autogenerator  
- **One-line Summary:** Not provided  
- **Creation Date (ISO8601):** 2025-05-05  
- **Description:**  
  This assistant generates docker-compose.yml files from docker inspect output, translating container configurations into Compose definitions.

---

## 🔗 Access & Links

- **ChatGPT Access URL:** Not provided  
- **n8n Link:** *Not provided*  
- **GitHub JSON Source:** [system-prompts/json/DockerComposeAutogenerator_270525.json](system-prompts/json/DockerComposeAutogenerator_270525.json)

---

## 🛠️ Capabilities

| Capability | Status |
|-----------|--------|
| Single turn | ❌ |
| Structured output | ❌ |
| Image generation | ❌ |
| External tooling required | ❌ |
| RAG required | ❌ |
| Vision required | ❌ |
| Speech-to-speech | ❌ |
| Video input required | ❌ |
| Audio required | ❌ |
| TTS required | ❌ |
| File input required | ❌ |
| Test entry | ❌ |
| Better as tool | ❌ |
| Is agent | ❌ |
| Local LLM friendly | ❌ |
| Deep research | ❌ |
| Update/iteration expected | ❌ |

---

## 🧠 Interaction Style

- **System Prompt:** (See above)
- **Character (type):** ❌  
- **Roleplay (behavior):** ❌  
- **Voice-first:** ❌  
- **Writing assistant:** ❌  
- **Data utility (category):** ❌  
- **Conversational:** ❌  
- **Instructional:** ❌  
- **Autonomous:** ❌  

---

## 📊 Use Case Outline

Not provided

---

## 📥 Product Thinking & Iteration Notes

- **Iteration notes:** Not provided

---

## 🛡️ Governance & Ops

- **PII Notes:** Not provided
- **Cost Estimates:** Not provided
- **Localisation Notes:** Not provided
- **Guardrails Notes:** Not provided

---

## 📦 Model Selection & Local Notes

- **Local LLM notes:** Not provided
- **LLM selection notes:** Not provided

---

## 🔌 Tooling & MCP

- **MCPs used:** *None specified*  
- **API notes:** *Not applicable*  
- **MCP notes:** *Not applicable*
