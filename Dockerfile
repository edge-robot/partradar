FROM public.ecr.aws/e1h7x4a2/plow-cloud-agents:base-771198a9609dcef54d44843e7da5329c17fa51b4@sha256:f1e7c421b97a80f1bd17015f96daceb965f350a241f7edc7e4d856a0e3a6f8f5

# The final slug is supplied by the owner at build time. An empty ID leaves
# upstream reporting dormant during development; cloud deployments must set it.
ARG AGENT_ID=""
ENV AGENT_ID=${AGENT_ID} \
    AGENT_NAME=PartRadar \
    AGENT_BLURB="Search first. Design only when necessary." \
    AGENT_RUNTIME=OpenClaw

COPY --chown=node:node prompt/AGENTS.md /opt/plow/prompt/AGENTS.md
COPY --chown=node:node skills/ /opt/plow/skills/
COPY --chown=node:node tools/part_radar.py /opt/plow/part-radar/part_radar.py
