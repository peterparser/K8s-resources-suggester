import requests
from urllib3.exceptions import InsecureRequestWarning


class Suggester:

    def __init__(self, prometheus_host, token, time_range='7d'):
        self.prometheus_host = prometheus_host
        self.token = token
        self.time_range = time_range

    def suggest_values(self, k8s_object):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        #Pe i pod avg_over_time(container_memory_working_set_bytes{pod=~'snitch-jvm.*',namespace='snitch',container='snitch-jvm'}[7d])
        # Retrieve pod memory usage
        params_memory_request = {
            "query": f"avg_over_time(container_memory_working_set_bytes{{pod=~'{k8s_object[2]}.*',namespace='{k8s_object[0]}',container='{k8s_object[3]}'}}[{self.time_range}])"
        }
        response = requests.get(f"{self.prometheus_host}/api/v1/query", headers=headers, params=params_memory_request, verify=False)
        memoryRequest = f'{round(float(response.json()["data"]["result"][0]["value"][1]) / 1000000)} M'

        params_memory_limit = {
            "query": f"max_over_time(container_memory_working_set_bytes{{pod=~'{k8s_object[2]}.*',namespace='{k8s_object[0]}',container='{k8s_object[3]}'}}[{self.time_range}])"
        }

        response = requests.get(f"{self.prometheus_host}/api/v1/query", headers=headers, params=params_memory_limit,
                                verify=False)

        memoryLimit = f'{round(float(response.json()["data"]["result"][0]["value"][1]) / 1000000)} M'

        params_cpu_request = {
            "query": f"avg_over_time(pod:container_cpu_usage:sum{{pod=~'{k8s_object[2]}.*',namespace='{k8s_object[0]}'}}[{self.time_range}])"
        }

        response = requests.get(f"{self.prometheus_host}/api/v1/query", headers=headers, params=params_cpu_request,
                                verify=False)

        cpu_request = f'{round(float(response.json()["data"]["result"][0]["value"][1]), 3)}'

        params_cpu_limit = {
            "query": f"max_over_time(pod:container_cpu_usage:sum{{pod=~'{k8s_object[2]}.*',namespace='{k8s_object[0]}'}}[{self.time_range}])"
        }

        response = requests.get(f"{self.prometheus_host}/api/v1/query", headers=headers, params=params_cpu_limit,
                                verify=False)

        cpu_limit = f'{round(float(response.json()["data"]["result"][0]["value"][1]), 3)}'

        return [
            k8s_object[0], # Namespace
            k8s_object[1], # type
            k8s_object[2], # Name
            k8s_object[3], # Container
            k8s_object[4], # Replicas
            k8s_object[5], # Request CPU
            cpu_request, # suggested
            k8s_object[6], # CPU LIMIT,
            cpu_limit,
            k8s_object[7], # Memory request
            memoryRequest, # suggest
            k8s_object[8], # memory limit
            memoryLimit # suggest
        ]


