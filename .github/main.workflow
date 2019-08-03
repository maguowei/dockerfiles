workflow "Build maguowei/base" {
  on = "push"
  resolves = [
    "Docker push python",
    "Docker push base",
    "Docker push python-app",
  ]
}

action "Docker login" {
  uses = "actions/docker/login@master"
  secrets = ["DOCKER_USERNAME", "DOCKER_PASSWORD"]
}

action "Docker build base" {
  uses = "actions/docker/cli@master"
  needs = ["Docker login"]
  args = "build -t maguowei/base base"
}

action "Docker push base" {
  uses = "actions/docker/cli@master"
  args = "push maguowei/base"
  needs = ["Docker build base"]
}

action "Docker build python" {
  uses = "actions/docker/cli@master"
  needs = ["Docker login"]
  args = "build -t maguowei/python python"
}

action "Docker push python" {
  uses = "actions/docker/cli@master"
  needs = ["Docker build python"]
  args = "push maguowei/python"
}

action "Docker build python-app" {
  uses = "actions/docker/cli@master"
  needs = ["Docker login"]
  args = "build -t maguowei/python-app:onbuild python-app"
}

action "Docker push python-app" {
  uses = "actions/docker/cli@master"
  needs = ["Docker build python-app"]
  args = "push maguowei/python-app:onbuild"
}
