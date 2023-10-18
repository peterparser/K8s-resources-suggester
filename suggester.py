import time

from urllib3.exceptions import InsecureRequestWarning

import querier

class Suggester:
    def __init__(self, prometheus_host, token, k8s_flavour, time_range='7d', step='3h'):
        self.prometheus_host = prometheus_host
        self.token = token
        self.time_range = time_range
        self.queries = querier.queries[k8s_flavour]
        self.end = int(time.time())
        self.start = self.end - 24 * 60 * 60 * int(time_range[:-1])
        self.step = step
        self.aggregator = {}

        for metric, query_struct in self.queries.items():
            if query_struct["query_type"] == 'query_range':
                self.aggregator[metric] = querier.aggregators[metric]


    def build_query(self, k8s_object, metric):
        host = f"{self.prometheus_host}/api/v1/{self.queries[metric]['query_type']}"
        match self.queries[metric]["query_type"]:
            case "query":
                params = {
                    "query": self.queries[metric]["query"].format(
                        workload=k8s_object[9],
                        namespace=k8s_object[0],
                        time_range=self.time_range
                        )
                }
            case "query_range":
                params = {
                    "query": self.queries[metric]["query"].format(
                        workload=k8s_object[9],
                        namespace=k8s_object[0],
                        time_range=self.time_range
                        ),
                    "start": self.start,
                    "end": self.end,
                    "step": self.step
                }

        return host, params


    def suggest_values(self, k8s_object):
        
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        results = {}

        for metric, query_struct in self.queries.items():
            host, params = self.build_query(k8s_object, metric)
            result = querier.run_query(host, headers, params)
            results[metric] = querier.handle_response(metric, result, self.aggregator.get(metric, None))

        return [
            k8s_object[0], # Namespace
            k8s_object[1], # type
            k8s_object[2], # Name
            k8s_object[3], # Container
            k8s_object[4], # Replicas
            k8s_object[5], # Request CPU
            results["cpu_request"], # suggested
            k8s_object[6], # CPU LIMIT,
            results["cpu_limit"],
            k8s_object[7], # Memory request
            results["memory_request"], # suggest
            k8s_object[8], # memory limit
            results["memory_limit"] # suggest
        ]


