# Azure Service Connector Conformance Test
Conformance tests used to validate Arc extension of Azure Service Connector.

## Test Infrastructure
Now the tests are fixed to use the infra below
- [Aks Cluster](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/937bc588-a144-4083-8612-5f9ffbbddb14/resourceGroups/servicelinker-test-linux-group/providers/Microsoft.ContainerService/managedClusters/test-scextension-cluster/overview) (where the extension is installed)
- [Keyvault](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/937bc588-a144-4083-8612-5f9ffbbddb14/resourceGroups/servicelinker-test-linux-group/providers/Microsoft.KeyVault/vaults/test-scextension-kv/overview) (to test csi secret store)
- [App Registration](https://ms.portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/~/Overview/appId/8caf986f-fbc5-4205-9a83-9f6fe1075bb9/isMSAApp~/false) (to authenticate CLI)

## Prerequisites
- Install sonobuoy ([sonobuoy release](https://github.com/vmware-tanzu/sonobuoy/releases))
- Install kubectl. ([install instructions](https://kubernetes.io/docs/tasks/tools/install-kubectl/))
- A Kubernetes config file configured to access the target Kubernetes cluster and set as the current context.

## Executing conformance tests
Run sonobuoy test
```
sonobuoy run --plugin .\conformance.yaml --plugin-env azure-arc-serviceconnector.CLIENT_SECRET=<replace with SP secret> --wait
```

Retrive test results
```
sonobuoy retrive
```

Check result
```
sonobuoy results <result_file_name>.tar.gz
```