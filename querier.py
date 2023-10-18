import requests

from urllib3.exceptions import InsecureRequestWarning 

from statistics import mean

queries = {
    "kubernetes": {
        "memory_request": {
            "query": "avg_over_time(container_memory_working_set_bytes{{pod=~'{workload}.*',namespace='{namespace}',container=''}}[{time_range}])",
            "query_type": "query"
        },
        "memory_limit": {
            "query": "max_over_time(container_memory_working_set_bytes{{pod=~'{workload}.*',namespace='{namespace}',container=''}}[{time_range}])",
            "query_type": "query"
        },
        "cpu_request": {
            "query": "sum(rate(container_cpu_usage_seconds_total{{pod=~'{workload}.*',namespace='{namespace}'}}[2m]))",
            "query_type": "query_range"
        },
        "cpu_limit": {
            "query": "sum(rate(container_cpu_usage_seconds_total{{pod=~'{workload}.*',namespace='{namespace}'}}[2m]))",
            "query_type": "query_range"
        }

    },
    "openshift": {
        "memory_request": {
            "query": "avg_over_time(container_memory_working_set_bytes{{pod=~'{workload}.*',namespace='{namespace}',container=''}}[{time_range}])",
            "query_type": "query"
        },
        "memory_limit": {
            "query": "max_over_time(container_memory_working_set_bytes{{pod=~'{workload}.*',namespace='{namespace}',container=''}}[{time_range}])",
            "query_type": "query"
        },
        "cpu_request": {
            "query": "avg_over_time(pod:container_cpu_usage:sum{{pod=~'{workload}.*',namespace='{namespace}'}}[{time_range}])",
            "query_type": "query"
        },
        "cpu_limit": {
            "query": "max_over_time(pod:container_cpu_usage:sum{{pod=~'{workload}.*',namespace='{namespace}'}}[{time_range}])",
            "query_type": "query"
        }
    }

}


aggregators = {
    "cpu_limit": max,
    "cpu_request": mean
}

def handle_memory(result):
    return f'{round(float(result[0]["value"][1]) / 1000000)} M'

def handle_cpu(result, aggregator):
    if result[0]["values"]:
        return  f'{round(aggregator(result[0]["values"][1]), 2)}'
    else:
        return f'{round(float(result[0]["value"][1]), 2)}'
    

def handle_response(metric, result, aggregator=None):
    
    match metric:
        case "memory_request" | "memory_limit":
            return handle_memory(result)
    
    
        case "cpu_request" | "cpu_limit":
            return handle_cpu(result, aggregator)
    

def run_query(url, headers, params):
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    response = requests.get(url, headers=headers, params=params, verify=False)
    return response.json()["data"]["result"]