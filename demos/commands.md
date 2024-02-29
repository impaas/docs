# Demo Commands
## Static Blog
```sh
pushd blog
impaas app create blog static -t demo
impaas app deploy -a blog .
popd
```

## Flask App
```sh
pushd greet
impaas app create greet python -t demo
impaas app deploy -a greet .
popd
```

## CI Deployment
```sh
pushd greet-ci
impaas token create --id demo-ci-token -t demo
impaas role assign deployer demo-ci-token greet
impaas token show demo-ci-token
popd
```

## Dockerfile
```sh
pushd counter
impaas platform list
impaas app create counter -t demo
impaas app deploy -a counter --dockerfile .
popd
```

## Docker Registry
```sh
impaas app create dashboard -t demo
impaas app deploy -a dashboard -i tsuru/dashboard
```

## Services
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

## Volumes
```sh
pushd filemgr
impaas app create filemgr python -t demo
impaas app deploy -a filemgr .
impaas volume create uploads azurefile -t demo -o capacity=512Mi -o access-modes=ReadWriteMany -p local
impaas volume bind uploads /uploads -a filemgr
popd
```
