# K8s request/limit suggester

This tool simplifies the gathering of data about the resource consumption of your pods.
In particular, it outputs an excel table with the current configuration of your deployments and statefulsets and their resources, also the tool estimates the requests and the limits based on prometheus data.

# Requirements
To run the script you need:
* An authenticated kubectl session
* A jwt token with the roles to grab data from prometheus

All the required libraries can be found in requirements.txt

To install the requirements:
```commandline
pip3 install -r requirements.txt
```

# Invocation
```commandline
python3 main.py -u <prometheus URL> -n <comma separated list of namespaces> [-o <output-file>]
```
Example
```commandline
python3 main.py -u https://mypromehtues.prometheus -n bar,foo -o myexcel.xlsx
```
