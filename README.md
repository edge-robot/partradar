# PartRadar 📡

Search first. Design only when necessary.

PartRadar is an AI Worth Using OpenClaw 2.0 app that searches the open-source hardware ecosystem before new mechanical engineering work begins. If the part already exists, reuse it. If it almost fits, create a local engineering order for ClawCAD adaptation. If nothing suitable exists, request a new ClawCAD design through the same local order.

**PartRadar finds it before ClawCAD builds it.**

**PartRadar discovers whether we need to design. ClawCAD decides how we design it.**

## How it works

```mermaid
flowchart TD
    A[Need a physical part] --> B[📡 PartRadar<br/>OpenClaw 2.0]
    B --> C[Search open-source hardware]
    C --> D{Radar result}
    D -->|FOUND| E[Reuse existing design]
    D -->|ADAPTABLE| F[DesignRequired]
    D -->|NOT_FOUND| F
    F --> G[Persistent engineering order<br/>Plow state volume]
    G --> H[Engineering team / ClawCAD]
    H --> I[Design]
    I --> J[Simulation]
    J --> K[Human gate]
    K --> L[Manufacturing]
```

```mermaid
flowchart TD
    A[AI Worth Using / Plow] --> B[Plow OpenClaw base]
    B --> C[📡 PartRadar]
    C --> D[AGENTS.md]
    C --> E[PartRadar skills]
    C --> F[Research and work order helper]
    B --> G[Inherited Agent Index reporter]
```

PartRadar is a **Build on Plow** variant image. Its Dockerfile inherits the maintained [Plow OpenClaw base](https://github.com/plow-pbc/plow-openclaw-agent), pinned at upstream commit `771198a9609dcef54d44843e7da5329c17fa51b4` and image digest `sha256:f1e7c421b97a80f1bd17015f96daceb965f350a241f7edc7e4d856a0e3a6f8f5`. It replaces only the agent prompt, adds three skills, and includes a small deterministic artifact renderer. OpenClaw remains the runtime. Plow provides phone conversations, its channel/plugin, gateway, state volume, model access, and Agent Index registration and five-minute usage reporting. No second reporter runs here. See [architecture](docs/architecture.md).

## Try it locally

Follow the [installation guide](docs/install.md). Local development uses **Podman Compose**. After the current [`plow-agents` CLI](https://github.com/plow-pbc/plow-agents) provisions a line and writes `plow-credentials`, run `podman compose up --build -d`; the CLI's attempted `docker compose` step can fail on a Podman-only machine. Open the local OpenClaw Control UI at `http://localhost:3001` through the loopback-only Plow development proxy, then text the listed phone number. `AGENT_ID` is supplied by the ignored `.env` file and enables inherited Agent Index reporting.

Example request: “I need an FDM-printable enclosure for a Raspberry Pi Zero with an RPIZ CAM 5MP 120 camera.” PartRadar searches for existing designs, cites their license and files, and replies `FOUND`, `ADAPTABLE`, or `NOT_FOUND`. For the latter two, it persists the research, a `DesignRequired` event, and an open engineering work order under `/var/lib/plow/research/REQ-NNNN/`. The engineering team can review the local order through the agent or Plow state volume. PartRadar does not make CAD or simulation calls. The [demo guide](docs/demo.md) includes a real, source-backed `ADAPTABLE` example.

Run the deterministic demo artifact locally without an agent account:

```sh
python3 tools/part_radar.py examples/pi-zero-camera-research.json --out artifacts
cat artifacts/REQ-0042/research.yaml
cat artifacts/REQ-0042/design-required.json
cat artifacts/REQ-0042/engineering-order.json
```

This fixture demonstrates artifact rendering from inspected sources. It is not a recorded live OpenClaw conversation or proof that the engineering team has reviewed the order.

## Publication

PartRadar is MIT licensed. The target repository is [edge-robot/partradar](https://github.com/edge-robot/partradar). The [publishing checklist](docs/publishing.md) tracks its public availability, the public digest-pinned image, Index metadata and usage, verification, one-click admission, demo video, and real screenshot. The final agent slug, video, and image still need to be supplied by the owner.

Upstream references: [AI Worth Using publication guide](https://aiworthusing.com/agent-index/publish), [Plow OpenClaw base](https://github.com/plow-pbc/plow-openclaw-agent), [`plow-agents`](https://github.com/plow-pbc/plow-agents), and [Agent Index client](https://github.com/plow-pbc/agent-index-client).
