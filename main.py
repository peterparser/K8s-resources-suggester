# This is a sample Python script.
from retriever import Retriever
from kubernetes import config
from suggester import Suggester
from reporter import Reporter
import argparse
import getpass

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press the green button in the gutter to run the script.


header = [
    "Namespace",
    "Object Type",
    "Name",
    "Container Name",
    "Replicas",
    "CPU Request",
    "Suggested CPU Request",
    "CPU Limit",
    "Suggested CPU Limit",
    "Memory Request",
    "Suggested Memory Request",
    "Memory Limit",
    "Suggested Memory Limit"

]

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Resource Reporter Suggester',
        description='It creates a Report of resources declared and suggested',
        epilog='RRS')

    parser.add_argument("-u", "--url", help="Prometheus URL", type=str, required=True)
    parser.add_argument("-t", "--type", choices=['kubernetes', 'openshift'], default="kubernetes", help="Kubernetes flavour", type=str)
    parser.add_argument("-n", "--namespaces", help="Comma separated list of namespaces", type=str, required=True)
    parser.add_argument("-o", "--output", default="output.xlsx", help="Output file", type=str)

    args = parser.parse_args()
    token = getpass.getpass("Insert SA Token here:")

    config.load_kube_config()
    retriever = Retriever()
    suggester = Suggester(args.url, token, args.type)
    namespaces = args.namespaces.split(",")

    data = []
    for ns in namespaces:
        data.extend(retriever.get_mem_cpu_req_lim(ns))
    print("Data obtained from K8s APIs...")
    print("Obtaining and calculating data from Prometheus...")

    # Filter replicas = 0
    suggested = list(map(lambda x: suggester.suggest_values(x), filter(lambda x: x[4] != 0, data)))

    reporter = Reporter(header)

    reporter.write_data_to_table(suggested)
    reporter.write_data(args.output)
    print("DONE!")
    print(f"Data written to {args.output}")



