# AI Builder
#### _by [Attune Engineering](https://attuneengineering.com/)_**
For support, either add an issue or email us at contact@attuneengineering.com
Maintained by _[Reed Bender](https://github.com/mrbende)_.

<div align="center">
  <!-- Build Status -->
  <a href="https://github.com/AttuneEngineering/ai-builder/actions">
    <img src="https://github.com/AttuneEngineering/ai-builder/actions/workflows/main.yml/badge.svg" alt="Build Status" />
  </a>
  <!-- Docker Image Size -->
  <a href="">
    <img src="https://img.shields.io/docker/image-size/attuneengineering/ai-builder/main" alt="Docker Image Size" />
  </a>
  <!-- Code Size -->
  <a href="">
    <img src="https://img.shields.io/github/languages/code-size/attuneengineering/ai-builder" alt="Code Size" />
  </a>
  <!-- GitHub Issues -->
  <a href="https://github.com/attuneengineering/ai-builder/issues">
    <img src="https://img.shields.io/github/issues/attuneengineering/ai-builder.svg" alt="GitHub Issues" />
  </a>
  <!-- License -->
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License" />
  </a>
</div>

<div align="center">
  <p><em>tools used</em></p>
  <a href="">
    <img src="assets/icons/python.svg" alt="Python" />
  </a>
  <a href="">
    <img src="assets/icons/docker.svg" alt="Docker" />
  </a>
  <a href="">
    <img src="assets/icons/github.svg" alt="Github" />
  </a>
  <a href="">
    <img src="assets/icons/openai.svg" alt="OpenAI" />
  </a>
  <a href="">
    <img src="assets/icons/markdown.svg" alt="Markdown" />
  </a>
  <a href="">
    <img src="assets/icons/markdown.svg" alt="Markdown" />
  </a>
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
    export REGISTRY_IMAGE="ai-builder:main"
    docker build -f Dockerfile -t $REGISTRY_IMAGE .

    ### ...OR PULL FROM ATTUNE ENGINEERING
    export REGISTRY_IMAGE="ghcr.io/attuneengineering/ai-builder:main"
    docker pull $REGISTRY_IMAGE
    ```

4. Run the Docker container.
    ```bash
    docker run -it $REGISTRY_IMAGE

    ### OPTIONALLY, LAUNCH JUPYTER LAB ON START
    docker run $REGISTRY_IMAGE /workspace/ai-builder/bin/jupyter-lab.sh
    ```
    You're now ready to begin working within the interactive Docker CLI, or otherwise access Jupyter Lab at `http://localhost:8888`.

5. Configure your secrets as environment variables.
    ```bash
    export GITHUB_TOKEN="xxx"
    export HUGGING_FACE_HUB_TOKEN="xxx"
    export OPENAI_API_KEY="xxx"
    export SERPAPI_API_KEY="xxx"
    ```
    This can also be done using the Python [dotenv](https://configu.com/blog/using-py-dotenv-python-dotenv-package-to-manage-env-variables/) package.

6. _optional_ Push the Docker image to your own Github Container Registry.
    This will require you to have a Github account and a personal access token with `read:packages` and `write:packages` permissions. You can create a token [here](https://github.com/settings/tokens). Note that you'll also need to either fork the `AI Builder` repository or create a new repository in your own account.
    ```bash
    export GITHUB_TOKEN="xxx" 
    echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
    docker tag $REGISTRY_IMAGE ghcr.io/YOUR_GITHUB_USERNAME/ai-builder:main
    docker push ghcr.io/YOUR_GITHUB_USERNAME/ai-builder:main
    ```

### Developing with [Gitpod](https://www.gitpod.io/docs/configure/workspaces/)

Attune Engineering configures all of our repositories to work with Gitpod, enabling seamless version control and dependency management across software architectures. This is a great option for those who don't want to install Docker on their local machine, or who want to develop from a Chromebook or other device that doesn't support Docker. You are granted a free 50 hours of development per month, which is more than enough to get started.

<div align="center">
    <a href="https://gitpod.io/#https://github.com/AttuneEngineering/ai-builder"><img src="https://gitpod.io/button/open-in-gitpod.svg" alt="Open-in-Gitpod"></a>
</div>

_note_ Gitpod also allows you to manage your collection of API keys as project-level secrets, which can be configured in Projects --> Settings --> Variables. 

---

