# Install

## Cert Manager
```sh
kubectl create -f letsencrypt-prod.yaml
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.14.3 \
  --set installCRDs=true \
  --set ingressShim.defaultIssuerName=letsencrypt-prod \
  --set ingressShim.defaultIssuerKind=Issuer \
  --set ingressShim.defaultIssuerGroup=cert-manager.io
```

## Tsuru
### New Installation
```sh
helm install tsuru impaas/tsuru-stack -n tsuru-system --create-namespace -f values.yaml
kubectl create -n tsuru-system -f letsencrypt-prod.yaml
kubectl exec -it -n tsuru-system deploy/tsuru-api -- tsurud root user create rsa21@ic.ac.uk
```

### Update Existing Installation
```sh
helm upgrade tsuru impaas/tsuru-stack -n tsuru-system -f values.yaml
```

# Setup
```sh
brew tap tsuru/homebrew-tsuru
brew install tsuru
echo "alias tsuru='impaas'" >> ~/.bashrc
source ~/.bashrc

impaas remote add https://impaas.uk -s
impaas login
scp ~/.tsuru/token dev:~/.tsuru/token

impaas team create demo
```

# Configuration

## Roles
```sh
impaas role-add team-member team
impaas role-permission-add team-member app
impaas role-add team-member_service team
impaas role-permission-add team-member_service service
impaas role-add team-member_volume team
impaas role-permission-add team-member_volume volume
impaas role-add deployer app
impaas role-permission-add deployer app.deploy
```

## Admins
```sh
for user in ard21@ic.ac.uk app21@ic.ac.uk akm20@ic.ac.uk th520@ic.ac.uk ssw21@ic.ac.uk
do
  yes | head -n 2 | impaas user create $user
  impaas role-assign AllowAll $user
done
```

## Platforms
```sh
for platform in static python nodejs go
do
  impaas platform add $platform
done
```

## Services
```sh
impaas service create service-manifest.yaml
```

# Uninstall
```sh
helm uninstall tsuru -n tsuru-system
kubectl delete namespace tsuru-system
```
