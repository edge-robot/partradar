# Architecture and upstream contracts

PartRadar uses the **Build on Plow** path. The image inherits the Plow OpenClaw base; it does not copy or fork its boot code, channel plugin, or reporter. The runtime chain is AI Worth Using / Plow → pinned Plow base → OpenClaw → PartRadar prompt and skills. ClawCAD is a separate application. PartRadar persists an engineering work order locally instead of invoking ClawCAD or depending on its source code.

## Upstream inspection (2026-09-28)

| Source | Inspected revision | Relevant contract |
| --- | --- | --- |
| [plow-openclaw-agent](https://github.com/plow-pbc/plow-openclaw-agent/tree/771198a9609dcef54d44843e7da5329c17fa51b4) | `771198a9609dcef54d44843e7da5329c17fa51b4` | Variant `FROM` by digest; copy prompt to `/opt/plow/prompt/AGENTS.md`, skills to `/opt/plow/skills/`; boot owns workspace prompt and the reporter. README, Dockerfile, prompt, skills, plugin, Compose, boot, and docs were checked. |
| [plow-agents](https://github.com/plow-pbc/plow-agents/tree/3033a59754067bb21b4b6b2844967db343ecf7bd) | `3033a59754067bb21b4b6b2844967db343ecf7bd` | `deploy --local` mints a line credential and invokes `docker compose up --build -d`; image build/push, digest deployment, Index metadata, and promotion commands. |
| [agent-index-client](https://github.com/plow-pbc/agent-index-client/tree/fbfe8b635c1f20ce1f0152497abb419623f53329) | `fbfe8b635c1f20ce1f0152497abb419623f53329` | Registration metadata and direct OpenClaw usage collection. The base pins its own reviewed client commit; PartRadar does not vendor or invoke the standalone client. |

The exact base is `public.ecr.aws/e1h7x4a2/plow-cloud-agents:base-771198a9609dcef54d44843e7da5329c17fa51b4@sha256:f1e7c421b97a80f1bd17015f96daceb965f350a241f7edc7e4d856a0e3a6f8f5`. The digest was resolved from the public ECR registry on 2026-09-29. The base itself pins `ghcr.io/openclaw/openclaw:2026.9.6` by digest.

The base starts OpenClaw through `/opt/plow/boot/main.js`. It persists state under `/var/lib/plow`, reads PartRadar's prompt at boot, and renders `/var/lib/plow/workspace/AGENTS.md`. Boot replaces that file and workspace `BOOTSTRAP.md`, `SOUL.md`, `IDENTITY.md`, and `USER.md`, so research lives instead under `/var/lib/plow/research`. A named Compose volume preserves it through restart. Plow-owned config includes the gateway, model/provider, channel, plugin, tool policy, identity, and session rules. Other owner settings can be configured through the OpenClaw Control UI. Local Compose also follows upstream's `dev-dashboard` Caddy proxy: only `127.0.0.1:3001` is published, while OpenClaw's port 3000 remains private. The local Podman bridge needed explicit public DNS resolvers to reach Plow; cloud deployment does not use this Compose setting.

When `AGENT_ID` is nonempty, the inherited boot reporter registers the installation using `AGENT_NAME`, `AGENT_BLURB`, and `AGENT_RUNTIME` and reports roughly every 300 seconds. It runs the pinned Agent Index client and `agentsview`, links the moved OpenClaw sessions into the collector's expected path, and also tells the client `OPENCLAW_STATE_DIR=/var/lib/plow` so it can read current SQLite transcripts directly. Its installation identity and ledger remain in the state volume. The base owns this loop; PartRadar adds no reporting process. Actual nonzero reporting requires a live text conversation and a running, registered container; packaging alone cannot prove it.

The base tool profile includes read, write, edit, and exec, plus Plow messaging and connected Latch MCP when the owner has it. It does not promise a built-in web search service. PartRadar uses whatever OpenClaw browser or Latch capability is actually connected. If research access is unavailable, it reports an incomplete investigation instead of fabricating `NOT_FOUND`.

## PartRadar contract

The agent writes research input JSON; `tools/part_radar.py` validates the three statuses, conservative license classification, evidence links, and selected candidate, then renders YAML. `FOUND` writes only the research artifact. `ADAPTABLE` and `NOT_FOUND` also render `design-required.json` and `engineering-order.json` with `status: OPEN` in the persistent `/var/lib/plow/research/REQ-NNNN/` directory. The helper never searches, sends messages, invokes ClawCAD, or creates CAD. All CAD and simulation decisions belong to the engineering team and ClawCAD.

The local order records a request for engineering review; it is not an acknowledgement that the team has received or accepted the job. A later integration can consume this explicit file contract without changing PartRadar's research boundary.
