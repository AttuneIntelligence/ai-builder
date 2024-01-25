
<div align="center">
    <h1>AI Builder</h1>
</div>

<div align="center">
  <!-- Build Status -->
  <a href="https://github.com/AttuneEngineering/ai-builder/actions">
    <img src="https://github.com/AttuneEngineering/ai-builder/actions/workflows/main.yml/badge.svg" alt="Build Status" />
  </a>
  <!-- Code Size -->
  <a href="">
    <img src="https://img.shields.io/github/languages/code-size/attuneengineering/ai-builder" alt="Code Size" />
  </a>
  <!-- Contributers -->
  <a href="https://github.com/attuneengineering/ai-builder/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/attuneengineering/ai-builder.svg" alt="Contributers" />
  </a>
  <!-- GitHub Issues -->
  <a href="https://github.com/attuneengineering/ai-builder/issues">
    <img src="https://img.shields.io/github/issues/attuneengineering/ai-builder.svg" alt="GitHub Issues" />
  </a>
  <!-- Forks -->
  <a href="https://github.com/attuneengineering/ai-builder/network/members">
    <img src="https://img.shields.io/github/forks/attuneengineering/ai-builder.svg" alt="GitHub Issues" />
  </a>
  <!-- License -->
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License" />
  </a>
</div>

<div align="center">
    <p>For support, either <a href="https://github.com/AttuneEngineering/ai-builder/issues/new/choose"> add an issue</a> or reach out to <a href="mailto:contact@attuneengineering.com">contact@attuneengineering.com</a>.</p>
</div>

---
## OVERVIEW

The `AI Builder` repository is a template for building your own AI applications, containing all of the building blocks necessary to get you building intelligent systems with LLMs in Python without the headaches of dependency management or infrastructure provisioning - _entirely for free and open source_.

### Features

- **Open Source Inference Guide**
  - Complete tutorial with source code for building your own inference pipeline with open source instruction-following LLMs.

- **Runpod Server Templates**
  * One-Click-Templates for deploying and configuring open source LLMs on [Runpod](https://runpod.io?ref=zdeyr0zx) GPUs.

- **Multimodal AI Vision**
  * Server templates and inference scripts for working with multimodal LLMs and integrating AI vision into your processes.

- **Function Calling**
  * Learn to build agential software architectures that can take actions with GPT-4 **OR** Attune Engineering's custom fine-tuned function calling models.

- **Complete DevOps Solutions**
  * Manage all development and production environments for your AI systems with our curated Docker containers and Github workflows for building with AI.

### One-Click-Templates for API Server Deployment

The largest barrier-to-entry for working with open source LLMs lies in provisioning the resources to GPUs that can be made available via an API. <a href="https://runpod.io?ref=zdeyr0zx" target="_blank">Runpod</a> simplifies much of this process, and we have created a collection of ready-to-deploy templates that will make an API endpoint available to you in minutes.
  * See the complete list <a href="https://attuneengineering.com/models" target="_blank">here</a>.
  * Includes Mixtral 8x7B, Llama 2, LLaVA Vision, and a plethora of others...

## BUILDING YOUR ENVIRONMENT

### (a) Developing with Gitpod

Attune Engineering configures all of our repositories to work with [Gitpod](https://www.gitpod.io/docs/configure/workspaces), enabling you to deploy a preconfigured development environment to provisioned cloud resources. You are granted a free 50 hours of development per month, which is more than enough to get started.

<div align="center">
    <a href="https://gitpod.io/#https://github.com/AttuneEngineering/ai-builder"><img src="https://gitpod.io/button/open-in-gitpod.svg" alt="Open-in-Gitpod"></a>
</div>

### (b) Running Docker on your local machine

1. Install [Docker](https://docs.docker.com/get-docker/) on your machine if it is not already installed.

2. Clone the `AI Builder` repository to your local machine.
    ```bash
    git clone git@github.com:AttuneEngineering/ai-builder.git
    cd ai-builder
    ```

3. Build the Docker image yourself _OR_ pull the image from Attune Engineering.
    ```bash
    ### BUILD FROM SOURCE...
    export REGISTRY_IMAGE="YOUR_GITHUB_USERNAME/ai-builder"
    docker build -f Dockerfile -t $REGISTRY_IMAGE:main .

    ### ...OR PULL FROM ATTUNE ENGINEERING\'S GITHUB CONTAINER REGISTRY
    export REGISTRY_IMAGE="ghcr.io/attuneengineering/ai-builder"
    docker pull $REGISTRY_IMAGE:main
    ```

4. Run the Docker container.
    ```bash
    docker run -it $REGISTRY_IMAGE:main

    ### OPTIONALLY, LAUNCH JUPYTER LAB ON START
    docker run $REGISTRY_IMAGE:main /workspace/ai-builder/bin/jupyter-lab.sh
    ```
    You're now ready to begin working within the interactive Docker CLI, or otherwise access Jupyter Lab at `http://localhost:8888`.

5. _optional_ Push the Docker image to your own Github Container Registry.
    This will require you to have a personal access token with `read:packages` and `write:packages` permissions. You can create a token [here](https://github.com/settings/tokens). Note that you'll also need to either fork the `AI Builder` repository or create a new repository in your own account.
    ```bash
    export GITHUB_TOKEN="xxx" 
    export REGISTRY_IMAGE="ghcr.io/YOUR_GITHUB_USERNAME/ai-builder"
    docker build -f Dockerfile -t $REGISTRY_IMAGE:main .
    echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
    docker push $REGISTRY_IMAGE:main
    ```
    _note_... Your `GITHUB_TOKEN` is already managed by the Github actions we are triggering with `.github/workflows/main.yml`, so it does not need to be added in addition.

    Additionally, this process can be automated with Github Actions. In order for the Github Workflows to successfully build the image and push it to your Github Container Registry, you must add the following to your `Repository Settings` --> `Secrets and Variables` --> `Actions` --> `Repository Secrets`...
    ```
    REGISTRY_IMAGE="ghcr.io/YOUR_GITHUB_USERNAME/ai-builder"
    ```

### (c) Building the environment locally

This is not ideal, as all of the source code is organized relative to the container's home directory within (`/workspace/ai-builder/src`). If you're simply looking to adapt the code to your own purposes, however, you can simply install the necessary requirements and update the `PYTHONPATH` to point to your `src` directory.
    ```bash
    pip install -r requirements.txt
    ```

---

## NEXT STEPS...

The `AI Builder` repository is a template for building your own AI applications. It is designed to be a starting point for your own projects, simplifying the process of building software applications around interchangeable open source models. This toolkit-based approach to interfacing with LLMs makes it easier to build complex architectures around these custom deployments.

Attune Engineering has compiled a collection of private repositories that contain source code for engineering a complete production-ready chat application, fine-tune your own models, or create knowledge graph representations with custom models, all of which build atop the building blocks of this repository.
