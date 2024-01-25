
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

## RUNNING THE CODE

We've containerized the complete development environment for interfacing with Generative AI models, templatized the configurations necessary for provisioning GPUs on <a href="https://runpod.io?ref=zdeyr0zx">Runpod</a> and made it easy for new users to get up with all the necessary package installations at the click of a button. Simply launch the `AI Builder` Docker container and get a fully configured environment with Jupyter to get you writing code in minutes.

### Running on your local machine

1. Install [Docker](https://docs.docker.com/get-docker/) on your machine if it is not already installed.

2. Clone the `AI Builder` repository to your local machine.
    ```bash
    git clone git@github.com:AttuneEngineering/ai-builder.git
    cd ai-builder
    ```

3. Build the Docker image yourself _OR_ pull the image from Attune Engineering.
    ```bash
    ### BUILD FROM SOURCE...
    export REGISTRY_IMAGE="ghcr.io/attuneengineering/ai-builder"
    docker build -f Dockerfile -t $REGISTRY_IMAGE:main .

    ### ...OR PULL FROM ATTUNE ENGINEERING
    docker pull $REGISTRY_IMAGE:main
    ```

4. Run the Docker container.
    ```bash
    docker run -it $REGISTRY_IMAGE:main

    ### OPTIONALLY, LAUNCH JUPYTER LAB ON START
    docker run $REGISTRY_IMAGE:main /workspace/ai-builder/bin/jupyter-lab.sh
    ```
    You're now ready to begin working within the interactive Docker CLI, or otherwise access Jupyter Lab at `http://localhost:8888`.

5. Configure your secrets as environment variables.
    ```bash
    export GITHUB_TOKEN="xxx"
    export OPENAI_API_KEY="xxx"
    export SERPAPI_API_KEY="xxx"
    ```
    This can also be done using the Python [dotenv](https://configu.com/blog/using-py-dotenv-python-dotenv-package-to-manage-env-variables/) package.

6. _optional_ Push the Docker image to your own Github Container Registry.
    This will require you to have a Github account and a personal access token with `read:packages` and `write:packages` permissions. You can create a token [here](https://github.com/settings/tokens). Note that you'll also need to either fork the `AI Builder` repository or create a new repository in your own account.
    ```bash
    export GITHUB_TOKEN="xxx" 
    export REGISTRY_IMAGE="ghcr.io/YOUR_GITHUB_USERNAME/ai-builder"
    docker build -f Dockerfile -t $REGISTRY_IMAGE:main .
    echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
    docker push $REGISTRY_IMAGE:main
    ```

    Additionally, this process can be automated with Github Actions. In order for the Github Workflows to successfully build the image and push it to your Github Container Registry, you must add the following to your `Repository Settings` --> `Secrets and Variables` --> `Actions` --> `Repository Secrets`...
    ```
    REGISTRY_IMAGE="ghcr.io/YOUR_GITHUB_USERNAME/ai-builder"
    ```
    `GITHUB_TOKEN` is already managed by the Github actions we are triggering with `.github/workflows/main.yml`, so it does not need to be added in addition.

### Developing with [Gitpod](https://www.gitpod.io/docs/configure/workspaces/)

Attune Engineering configures all of our repositories to work with Gitpod, enabling seamless version control and dependency management across software architectures. This is a great option for those who don't want to install Docker on their local machine, or who want to develop from a Chromebook or other device that doesn't support Docker. You are granted a free 50 hours of development per month, which is more than enough to get started.

<div align="center">
    <a href="https://gitpod.io/#https://github.com/AttuneEngineering/ai-builder"><img src="https://gitpod.io/button/open-in-gitpod.svg" alt="Open-in-Gitpod"></a>
</div>

_note_ Gitpod also allows you to manage your collection of API keys as project-level secrets, which can be configured in Projects --> Settings --> Variables. 

---

