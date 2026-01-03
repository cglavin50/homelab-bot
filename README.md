# Homelab Bot

This is a project maintaing a Python Discord Bot to help automate tasks in my homelab. At the moment, it is used for onboarding new users to my tailnet so they can leverage private services

It is currently deployed in my [homelab](https://github.com/cglavin50/nix-homelab).

## Requirements

A `requirements.txt` is provided, as is a flake.nix for nix-systems.

The following environment variables are required:

```
DISCORD_TOKEN=
GUILD_ID=
TAILSCALE_KEY=
TAILNET_ID=
```

## Functionality

Uses Discord App Commands, configured to pair with a Guild ID (allowed for easier development iteration). Exposes the following commands:

`/invite` (generates Tailnet invite link)
`/ping` (simple ping/pong command for confirming bot is alive)

## Dockerhub

Since I deploy this via kubernetes, this repo has a basic CD pipeline to build and push the image to DockerHub, see [workflow](.github/workflows/dockerhub.yaml).

The workflow requires the following to be configured in the repo:

`secrets.DOCKER_USERNAME`
`secrets.DOCKER_PASSWORD` (Dockerhub PAT)
`vars.REPO_NAME` (Dockerhub repo name)
