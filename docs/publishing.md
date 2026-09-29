# Agent Index and hackathon release

PartRadar follows [Build on Plow](https://aiworthusing.com/agent-index/publish). The project is MIT licensed; the pinned upstream Plow image is inherited under its own license and remains maintained upstream. Complete the [install smoke test](install.md) before publishing. The MVP's engineering order stays local in OpenClaw state. Discord appears below only for the hackathon's human admin and verification process.

## Registration and metadata

The final slug is `partradar` (`AGENT_ID`), and the public repository is `https://github.com/edge-robot/partradar`. From this checkout, after `plow-agents login`:

```sh
plow-agents image set partradar --name "PartRadar" --blurb "Search first. Design only when necessary." --repo https://github.com/edge-robot/partradar
plow-agents image set partradar --link https://github.com/edge-robot/partradar/blob/main/docs/install.md
```

Only issue the [screenshot and video commands](demo.md) after real media exists at stable public URLs. `--link` is the installation/tutorial URL in the current CLI. The `image set` flow edits Index metadata. `AGENT_RUNTIME=OpenClaw` and the name/blurb are present in the image and local Compose environment for inherited registration. Use the same slug in the image, local `.env`, and Index listing. `plow-agents image show partradar` can return 404 before one-click image admission because it reads the Plow image pin, not just the Index listing.

## Public image and one-click admission

Use the [Podman release build and push commands](install.md) to bake the owner slug into the variant image and push it in Docker image format. Record the immutable `ghcr.io/edge-robot/partradar@sha256:...` reference from the push digest. In GHCR settings, make the package public and verify anonymous pull. Then run:

```sh
plow-agents profile --show
```

Published `v2` image (2026-09-29): `ghcr.io/edge-robot/partradar@sha256:0fd033b803e2f1884046418be124b0add53c7856ed7bbfd82bbb943f68e58d4b`. An anonymous registry manifest request returned this digest.

The profile shows the owner UID. Provide the following to the AI Worth Using / Plow Discord admin for initial one-click admission:

```text
slug: partradar
owner UID: <OWNER_UID_FROM_PROFILE>
image: ghcr.io/edge-robot/partradar@sha256:<PUSH_DIGEST>
```

The admin operation is `plow-agents image promote partradar ghcr.io/edge-robot/partradar@sha256:IMAGE_DIGEST --owner OWNER_UID`. The participant does not run that privileged action. An existing Index listing is required first. On a Podman-only machine, build and push later releases with Podman, then promote their immutable digest using the current Plow CLI:

```sh
podman build --format docker --platform linux/amd64 --build-arg AGENT_ID=partradar -t ghcr.io/edge-robot/partradar:v2 .
podman push --digestfile partradar-image.digest ghcr.io/edge-robot/partradar:v2
plow-agents image promote partradar ghcr.io/edge-robot/partradar@sha256:IMAGE_DIGEST
```

Read `IMAGE_DIGEST` from `partradar-image.digest` without committing that file. Promotion makes the exact pushed image available for new installations; existing running agents keep their image. Recheck the current CLI before a future release.

For hackathon verification, the human owner posts the public repository URL, **final release commit SHA**, and Agent Index ID `partradar` in the [AI Worth Using verification thread](https://discord.com/channels/1519035948191449268/1549100840583700481). Confirm the verified badge and working one-click deployment afterward. The [publish guide](https://aiworthusing.com/agent-index/publish) requires MIT license, reporting usage, and verification for prizes; the product release also requires install instructions, real media, a public repository, and a public image.

## Release checklist

- [x] PartRadar works through a live OpenClaw text conversation
- [x] SMS receive/reply works on the local Plow line
- [x] MIT `LICENSE` exists
- [x] Repository is public at `https://github.com/edge-robot/partradar`
- [x] `AGENT_ID=partradar` is configured locally
- [x] Agent Index installation is registered and live OpenClaw usage is detected
- [x] The inherited reporter is present; no second reporter was added
- [x] Release fixes are committed and pushed
- [x] Docker-format public GHCR release image is pushed
- [x] Immutable image digest is recorded and anonymous pull is verified
- [ ] Public release image is deployed and live-tested
- [x] Listing name, blurb, repository, and install URL were submitted with `image set`
- [x] README and install guide are available in the repository
- [ ] Real screenshot is captured and registered
- [x] [Demo video](https://youtu.be/vHG0AgGHOfI) is recorded, published, and registered
- [ ] One-click admission is requested and enabled by an admin
- [ ] Verification is requested with repository URL, final commit, and Index ID
- [ ] Verified status is confirmed
