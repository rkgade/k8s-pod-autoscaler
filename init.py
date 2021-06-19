"""
Thought process is :

1. Figure out Kubernetes Objects, like deployments, services and pods
2. Figure out what pods are part of what deployments and what services
3. Figure out how to fetch metrics for each and service health checks.
4. Put in a dummy condition and
    1. Scale up pods
    2. Monitor services
    3. Monitor health Checks
5. Understand how to arrive at previous dummy condition by
    1. Reading Metrics like CPU, Memory, Network I/O, for now.
6. Scale up by implementing the actual condition
7. Read Policy that specifies what service to monitor and till what metrics.
"""
from kubernetes import client, config
from yaml import nodes

# Functions


# kube_config_contexts = config.list_kube_config_contexts()
# print(type(kube_config_contexts))
# # print(kube_config_contexts)
# for context in kube_config_contexts:
#     print(context[0])
#     print(context[1])


# Load Kube Config
config.load_kube_config()

k8s_client_api = client.CoreV1Api()
k8s_client_custom = client.CustomObjectsApi()
k8s_client_apps = client.AppsV1Api()
# print(k8s_client_api_beta)

# print("Listing pods with their IPs:")

# response = k8s_client_api.call_api('/apis/metrics.k8s.io/k8s_client_apibeta1/pods/',
#                        'GET', preaload_content=False)
# print(response.text)  # raw HTTPResponse

# List Functions
#


def scale_deployment_by_count(namespace, deployment, replicas):
    deployment.spec.replicas = replicas
    # patch the deployment
    resp = k8s_client_apps.patch_namespaced_deployment(
        name=deployment.metadata.name, namespace=namespace, body=deployment
    )

    print("\n[INFO] deployment's container image updated.\n")
    print("%s\t%s\t\t\t%s\t%s" % ("NAMESPACE", "NAME", "REVISION", "IMAGE"))
    print(
        "%s\t\t%s\t%s\t\t%s\n"
        % (
            resp.metadata.namespace,
            resp.metadata.name,
            resp.metadata.generation,
            resp.spec.replicas,
        )
    )


# List Namespaces
namespaces = k8s_client_api.list_namespace()
# for namespace in namespaces.items:
#     print(namespace.metadata.name)

# List Nodes
nodes = k8s_client_api.list_node()
# for node in nodes.items:
#     print(node.metadata.name)

selected_namespace = "microservices"

# List Deployments Per Namesapce
deployments_per_namespace = k8s_client_apps.list_namespaced_deployment(
    namespace=selected_namespace)
# for deployment in deployments_per_namespace.items:
#     print(type(deployment))
#     print(deployment.metadata.name)
#     print("SCALING UP ")
#     scale_deployment_by_count(selected_namespace, deployment, 1)


# List Pods Per Namespace
pods_per_namespce = k8s_client_api.list_namespaced_pod(
    namespace=selected_namespace)
# for pod in pods_per_namespce.items:
#     print(pod.metadata.name)

# List Pod Requests and Limits

# List Pod Metrics
print("--pod metrics--")
resource = k8s_client_custom.list_namespaced_custom_object(
    group="metrics.k8s.io", version="v1beta1", namespace=selected_namespace, plural="pods")
# print(resource["items"])
print(f'Number of Pods :{len(resource["items"])}')
for pod in resource["items"]:
    # Available, metadata, tiemstamp , window , containers.
    print(pod['containers'], "\n")


# Scale up one pod by scaling deployment

# pods = k8s_client_api.list_namespaced_pod()
# ret = k8s_client_api.list_pod_for_all_namespaces(watch=False)
# for i in ret.items:
#     print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

# print(local_config)
# local_config = config.new_client_from_config # This returns an API Object , can talk to multiple clusters at once.
# local_config = config.load_kube_config_from_dict(local_config_dict) # This takes kubeonfig file
