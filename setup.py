import subprocess
import yaml
import os
from jinja2 import Environment, FileSystemLoader

def get_vagrant_vms():
    result = subprocess.run(['vagrant', 'status'], capture_output=True, text=True)

    vms = {}
    for line in result.stdout.splitlines():
        if "running" in line:
            vm_name = line.split()[0]
            # usually for private network vagrant uses eth1 interface
            vm_ip = subprocess.run(['vagrant', 'ssh', vm_name, "--", "-t", "ip address show eth1 | grep 'inet ' | sed -e 's/^.*inet //' -e 's/\/.*$//'"], capture_output=True, text=True)
            vms[vm_name] = vm_ip.stdout[:-1]
    return vms

def get_ssh_config(machine_name):
    result = subprocess.run(['vagrant', 'ssh-config', machine_name], capture_output=True, text=True)
    config = {}
    for line in result.stdout.splitlines():
        if line.strip().startswith("HostName"):
            config['ansible_host'] = line.split()[1]
        elif line.strip().startswith("Port"):
            config['ansible_port'] = line.split()[1]
        elif line.strip().startswith("IdentityFile"):
            config['ansible_ssh_private_key_file'] = line.split()[1].strip('"')
    return config

def generate_inventory(machines):
    inventory = {
        'all': {
            'hosts': {},
            'children': {
                'kibana': {'hosts': {}},
                'master': {'hosts': {}},
                'workers': {'hosts': {}}
            }
        }
    }

    for machine in machines:
        config = get_ssh_config(machine)
        if 'master' in machine:
            inventory['all']['children']['master']['hosts'][machine] = config
        elif 'kibana' in machine:
            inventory['all']['children']['kibana']['hosts'][machine] = config
        else:
            inventory['all']['children']['workers']['hosts'][machine] = config

    # Write inventory.yaml
    with open('inventory.yaml', 'w') as file:
        yaml.dump(inventory, file, default_flow_style=False)

    print("inventory.yaml has been generated successfully!")

def generate_kibana_config(kibana_host, elasticsearch_hosts):
    # Path to the template
    template_path = './configs/templates/kibana.yml.j2'

    #output_dir = './roles/copy_config_to_kibana/files/'
    output_dir = './roles/setup_kibana/files/'
    os.makedirs(output_dir, exist_ok=True)
    os.system(f"rm -rf {output_dir}/*")

    filename = 'kibana.yaml'
    file_path = os.path.join(output_dir, filename)
    
    # Create Jinja2 environment
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    
    # Load template
    template = env.get_template(os.path.basename(template_path))
    
    # Render template with passed variables
    config_content = template.render(
        kibana_host=kibana_host,
        elasticsearch_hosts=elasticsearch_hosts
    )
    
    # Write generated file
    with open(file_path, 'w') as config_file:
        config_file.write(config_content)
    
    print(f'Configuration file {filename} has been created successfully.')

def generate_nginx_config(domain):
    template_loader = FileSystemLoader(searchpath="./configs/templates/")
    env = Environment(loader=template_loader)

    template = env.get_template('kibana.conf.j2')

    nginx_config = template.render(kibana_domain=domain)

    output_dir = './roles/setup_nginx/files/'
    os.makedirs(output_dir, exist_ok=True)
    os.system(f"rm -rf {output_dir}/*")
    filename = 'kibana.conf'

    file_path = os.path.join(output_dir, filename)

    with open(file_path, 'w') as config_file:
        config_file.write(nginx_config)

    print(f"Nginx configuration for {domain} generated successfully.")

def generate_elasticsearch_configs(hosts):
    # Path to the template
    template_path = './configs/templates/elasticsearch.yml.j2'
    
    # Create Jinja2 environment
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    
    # Load template
    template = env.get_template(os.path.basename(template_path))
    
    # Directory for configuration files
    output_dir = './roles/copy_config_to_server/files/'
    os.makedirs(output_dir, exist_ok=True)
    os.system(f"rm -rf {output_dir}/*")

    # Form groups for template
    groups = {
        'elasticsearch': [{'host': host, 'ip': ip} for host, ip in hosts.items()],
        'elasticsearch_master': [hosts.get('elasticsearch-master')],
        'elasticsearch_workers': [hosts.get(f'elasticsearch-worker-{i}') for i in range(1, len(hosts) - 1)]
    }
    
    # Create configuration files
    for host, ip in hosts.items():
        if host != "kibana":
            config = template.render(
                ansible_hostname=host,
                ansible_eth1={'ipv4': {'address': ip}},
                groups=groups
            )
            
            filename = f'{host}.yaml'
            
            file_path = os.path.join(output_dir, filename)
            
            # Write configuration to file
            with open(file_path, 'w') as f:
                f.write(config)
            
            print(f'Configuration file {filename} has been created successfully.')

def add_host_to_etc_hosts(ip, hostname):
    hosts_file = "/etc/hosts"
    
    new_entry = f"{ip} {hostname}\n"

    try:
        with open(hosts_file, 'r') as file:
            content = file.read()
            if new_entry.strip() in content:
                print(f"String {new_entry.strip()} alredy exist in {hosts_file}.")
                return
    except FileNotFoundError:
        print(f"File {hosts_file} doesn`t exist.")
        return

    try:
        command = f'echo "{new_entry.strip()}" | sudo tee -a {hosts_file}'
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Host {new_entry.strip()} added to {hosts_file}.")
        else:
            print(f"Error while updating {hosts_file}:  {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    domain = input("Enter the Kibana domain name: ")
    machines = get_vagrant_vms()
    kibana_host = machines['kibana']
    elasticsearch_hosts = [value for key, value in machines.items() if 'elasticsearch' in key]
    generate_inventory(machines)
    generate_elasticsearch_configs(machines)
    generate_kibana_config(kibana_host, elasticsearch_hosts)
    generate_nginx_config(domain)
    add_host_to_etc_hosts(machines['kibana'], domain)
