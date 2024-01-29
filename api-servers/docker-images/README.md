# Custom Docker Images for Runpod

---

In cases where we want the Runpod container images to execute particualr behavior on startup, such as launching a Flask server, we can customize the image off of a base build and reference this in the One-Click-Templates for GPU server deployment.

Each of these is a revised container environment for deploying a particular [One-Click-Template](https://attuneengineering.com/models.html) to provisioned GPUs.

### LLaVA

Adapted from the [official LLaVA Docker Image](https://github.com/ashleykleynhans/llava-docker). In this case, we are explicitly installing `Flask` and then running an inference server on port 5000 on start to create our.
  ```bash
  # export REGISTRY_IMAGE="ghcr.io/attuneengineering/ai-builder/llava-api"
  # export VERSION_TAG="v0.1"
  # echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
  # docker build -f llava.Dockerfile -t $REGISTRY_IMAGE:main .
  # docker push $REGISTRY_IMAGE:$VERSION_TAG
  docker pull ghcr.io/attuneengineering/ai-builder/llava-api:v0.1
  ```
  
---

## CHANGELOG

- [01/29/2024] - Published custom container image `ghcr.io/attuneengineering/ai-builder/llava-api:0.1` with Flask server deployment for Runpod inference.