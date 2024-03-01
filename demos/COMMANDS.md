# Demonstration Commands
## Static Site
```sh
pushd blog
impaas app create blog static -t demo
impaas app deploy -a blog .
popd
```

## Dynamic Web App
```sh
pushd greet
impaas app create greet python -t demo
impaas app deploy -a greet .
popd
```

## CI Deployments
```sh
pushd greet-ci
impaas token create --id demo-ci-token -t demo
impaas role assign deployer demo-ci-token greet
impaas token show demo-ci-token
popd
```

## Container Deployments
### Using a Dockerfile
```sh
pushd counter
impaas platform list
impaas app create counter -t demo
impaas app deploy -a counter --dockerfile .
popd
```

## From a Registry
```sh
impaas app create dashboard -t demo
impaas app deploy -a dashboard -i tsuru/dashboard
```

## Databases
```sh
pushd todo
impaas app create todo python -t demo
impaas service plan list mysql
impaas service instance add mysql tododb -t demo
impaas service instance info mysql tododb
impaas service instance bind mysql tododb -a todo
impaas app deploy -a todo .
popd
```

## File Storage
```sh
pushd filemgr
impaas app create filemgr python -t demo
impaas app deploy -a filemgr .
impaas volume create uploads azurefile -t demo -o capacity=512Mi -o access-modes=ReadWriteMany -p local
impaas volume bind uploads /uploads -a filemgr
popd
```
