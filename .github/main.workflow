workflow "Build maguowei/base" {
  on = "push"
  resolves = ["Docker push"]
}

action "Docker login" {
  uses = "actions/docker/login@master"
  secrets = ["DOCKER_USERNAME", "DOCKER_PASSWORD"]
}

action "Docker build" {
  uses = "actions/docker/cli@master"
  needs = ["Docker login"]
  args = "build -t maguowei/base base"
}

action "Docker push" {
  uses = "actions/docker/cli@master"
  needs = ["Docker build"]
  args = "push maguowei/base"
}
