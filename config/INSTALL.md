# Install
*This guide will walk you through the installation of Tsuru on a Kubernetes cluster.*

## Prerequisites
To get started running Imperial PaaS from scratch, you will need:
- A Kubernetes cluster on [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-gb/products/kubernetes-service) with the [application routing add-on enabled](https://learn.microsoft.com/en-us/azure/aks/app-routing)
- A Docker registry on [Azure Container Registry (ACR)](https://azure.microsoft.com/en-gb/products/container-registry), which is [attached to the Kubernetes cluster](https://learn.microsoft.com/en-us/azure/aks/cluster-container-registry-integration)
- A [Microsoft Entra (formerly Azure AD) application](https://learn.microsoft.com/en-us/entra/identity-platform/howto-create-service-principal-portal) for single sign-on (SSO) with college accounts
- A domain name, which you can point to the ingress controller's public IP address - we use [impaas.uk](https://impaas.uk)
- (optional) another Virtual Machine (in Azure, or elsewhere) to run the [MySQL Service Provisioner](https://github.com/impaas/mysql-database-provisioner), if you wish to enable database capability

> :exclamation: All of the YAML files provided are redacted and contain placeholders.<br>
> They are indicated by `{{placeholder}}` and should be replaced with your own values.

## Installing [`cert-manager`](https://cert-manager.io/)
First, install `cert-manager` which automatically handles TLS certificates.<br>
Here a `letsencrypt-prod` issuer is used to obtain certificates from Let's Encrypt.

> :warning: Let's Encrypt has a [rate limit](https://letsencrypt.org/docs/rate-limits/) of 50 certificates per week.<br>
> If you are testing, you can use their [staging API](https://letsencrypt.org/docs/staging-environment/) instead, which has a higher rate limit.<br>

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

## Installing [`tsuru-stack`](https://tsuru.io/)
Next, install the ImPaaS fork of Tsuru on the cluster using Helm.

```sh
helm install tsuru impaas/tsuru-stack -n tsuru-system --create-namespace -f values.yaml
kubectl create -n tsuru-system -f letsencrypt-prod.yaml
kubectl exec -it -n tsuru-system deploy/tsuru-api -- tsurud root user create abc123@ic.ac.uk
```

> If you change configuration, update an existing installation with `helm upgrade`.
> ```sh
> helm upgrade tsuru impaas/tsuru-stack -n tsuru-system -f values.yaml
> ```

## DNS
Create two DNS records on your domain. If your domain is `impaas.uk`, you will need:
- `impaas.uk` pointing to the public IP address of the Azure app routing ingress controller.
- `*.impaas.uk` pointing to the public IP address of the Azure app routing ingress controller.

> This IP can be found using the following command:<br>
> `kubectl get service nginx -n app-routing-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}'`.

## CLI
Install and configure the Tsuru CLI as described in [USAGE.md](USAGE.md).
Create a team to deploy applications to.

```sh
impaas team create admin
```

You are now ready to use your own instance of ImPaaS!

# Additional Configuration
## Roles
These roles for apps, services, and volumes are used by [`impaas-manager`](https://github.com/impaas/impaas-manager).<br>
The deployer role is intended for use with CI/CD.

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
This snippet creates users and assigns them the `AllowAll` role, which grants full access to the platform.

```sh
for user in abc123@ic.ac.uk def456@ic.ac.uk ghi789@ic.ac.uk
do
  yes | head -n 2 | impaas user create $user
  impaas role-assign AllowAll $user
done
```

## Platforms
This snippet adds the platforms that are available to deploy applications to.<br>
See all available platforms at [tsuru/platforms](https://github.com/tsuru/platforms).

```sh
for platform in static python nodejs go
do
  impaas platform add $platform
done
```

## Services
If you have a MySQL Service Provisioner running, you can add it as a service.

```sh
impaas service create service-manifest.yaml
```

# Uninstall
To uninstall Tsuru, run the following commands.<br>
> :warning: The second command will delete all resources within the `tsuru-system` namespace.

```sh
helm uninstall tsuru -n tsuru-system
kubectl delete namespace tsuru-system
```
