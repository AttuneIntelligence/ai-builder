## AI Builder
**by [Attune Engineering](https://attuneengineering.com/)**
#### Maintained by _[Reed Bender](https://reedbender.com/)_
For support, either add an issue or email us at contact@attuneengineering.com

---

[![Build Status](https://github.com/Attune-Engineering/ai-builder/actions/workflows/main.yml/badge.svg)](https://github.com/Attune-Engineering/ai-builder/actions)
---
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Attune-Engineering/ai-builder)

## Setting up Github Actions
*Need to set secrets for workspace image to be built with code commits* 

In your `ai-builder` repository, go to `Settings --> Code and Automation / Secrets and Variables --> Actions --> Manage Environment Secrets` and add the following secrets:
```
DOCKERHUB_USER=xxx
DOCKERHUB_TOKEN=xxx
REGISTRY_IMAGE=reedbndr/ai-builder
```

## Settimng up Gitpod
```
docker login -u $DOCKERHUB_USER -p $DOCKERHUB_TOKEN
echo -n "registry.hub.docker.com:";echo -n "$DOCKERHUB_USER:$DOCKERHUB_TOKEN" | base64
export GITPOD_IMAGE_AUTH=registry.hub.docker.com:cmVlZGJuZHI6ZGNrcl9wYXRfaDhaMXBud1NZdUotbkNDYmMtR1FJWUVpUHJ3
```