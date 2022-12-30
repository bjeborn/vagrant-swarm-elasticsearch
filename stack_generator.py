import os
import argparse
from jinja2 import FileSystemLoader, Environment


parser = argparse.ArgumentParser(
    description='Parser description.')

parser.add_argument('cluster_name')
parser.add_argument('--elastic_password', required=True)
parser.add_argument('--elastic_port', required=True, type=int)
parser.add_argument('--kibana_password', required=True)
parser.add_argument('--kibana_port', required=True, type=int)

args = parser.parse_args()

template_dir = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template("stack.yml.jinja")

output_from_parsed_template = template.render(
    cluster_name=args.cluster_name,
    elastic_password=args.elastic_password,
    elastic_port=args.elastic_port,
    kibana_password=args.kibana_password,
    kibana_port=args.kibana_port)

os.makedirs("stacks", exist_ok=True)
with open(os.path.join("stacks", f"{args.cluster_name}.yml"), "w") as fh:
    fh.write(output_from_parsed_template)