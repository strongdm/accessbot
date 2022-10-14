# Helm Chart Configuration

## Install Chart

```
helm install accessbot ./accessbot --values values-override.yaml
```

## Chart values

| Key | Type | Default | Description |
|:-----|:------|:---------|:-------------|
| replicaCount | int | `1` | Number of replicas (pods) to launch. |
| image.repository | string | `"tusproject/tusd"` | Name of the image repository to pull the container image from. |
| image.pullPolicy | string | `"IfNotPresent"` | [Image pull policy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) for updating already existing images on a node. |
| image.tag | string | `""` | Image tag override for the default value (chart appVersion). |
| imagePullSecrets | list | `[]` | Reference to one or more secrets to be used when [pulling images](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#create-a-pod-that-uses-your-secret) (from private registries). |
| nameOverride | string | `""` | A name in place of the chart name for `app:` labels. |
| fullnameOverride | string | `""` | A name to substitute for the full names of resources. |
| env | object | `{}` | For more information and a full list of variables, please refer to the [detailed guide for access configuration](../docs/configure_accessbot/ACCESS_CONFIGURATION.md). |
| deploymentAnnotations | object | `{}` | Annotations to be added to deployments. |
| podAnnotations | object | `{}` | Annotations to be added to pods. |
| podSecurityContext | object | `{}` | Pod [security context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/#set-the-security-context-for-a-pod). See the [API reference](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#security-context) for details. |
| securityContext | object | `{}` | Container [security context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/#set-the-security-context-for-a-container). See the [API reference](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#security-context-1) for details. |
| resources | object | No requests or limits. | Container resource [requests and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/). See the [API reference](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#resources) for details. |
| nodeSelector | object | `{}` | [Node selector](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector) configuration. |
| tolerations | list | `[]` | [Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) for node taints. See the [API reference](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#scheduling) for details. |
| affinity | object | `{}` | [Affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) configuration. See the [API reference](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#scheduling) for details. |
| strongdm.admins | string | `""` | List of admin users who will manage the bot and approve grant requests (by default). |
| strongdm.api_access_key | string | `""` | SDM API Access Key |
| strongdm.api_secret_key | string | `""` | SDM API Access Key Secret |
| slack.enabled | bool | `false` | Set to `true` to enable Slack Integration |
| slack.app_token | string | `""` | Slack App-Level Token |
| slack.bot_token | string | `""` | Slack Bot User OAuth Token |
| teams.enabled | bool | `false` | Set to `true` to enable MS Teams Integration |
| teams.app_id | string | `""` | Azure Bot application ID |
| teams.app_password | string | `""` | Azure Bot application password |
