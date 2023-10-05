from kubernetes import client
from urllib3.exceptions import InsecureRequestWarning
import requests


class Retriever:

    def __init__(self):
        self.resources = client.AppsV1Api()
        self.retrieve_function = {
            "deployment": self.resources.list_namespaced_deployment,
            "statefulset": self.resources.list_namespaced_stateful_set,
            "daemonset": self.resources.list_namespaced_daemon_set
        }

    def get_mem_cpu_req_lim(self, namespace):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        results = []
        for object_type, function in self.retrieve_function.items():
            k8s_objects = function(namespace)
            for k8s_object in k8s_objects.items:
                replicas = k8s_object.spec.replicas
                name = k8s_object.metadata.name
                for container in k8s_object.spec.template.spec.containers:
                    if container.resources.requests:
                        request_cpu = container.resources.requests.get("cpu", "Not defined")
                        request_memory = container.resources.requests.get("memory", "Not defined")
                    else:
                        request_cpu = "Not Defined"
                        request_memory = "Not Defined"
                    if container.resources.limits:
                        limit_cpu = container.resources.limits.get("cpu", "Not defined")
                        limit_memory = container.resources.limits.get("memory", "Not defined")
                    else:
                        limit_cpu = "Not Defined"
                        limit_memory = "Not Defined"
                    results.append((namespace, object_type, name,
                                    container.name, replicas,
                                    request_cpu, limit_cpu,
                                    request_memory, limit_memory))

        return results
