import subprocess
import yaml

def get_vagrant_vms():
    result = subprocess.run(['vagrant', 'status'], capture_output=True, text=True)

    vms = {}
    for line in result.stdout.splitlines():
        if "running" in line:
            vm_name = line.split()[0]
            # usually for private network vagrant use eth1 interface
            vm_ip = subprocess.run(['vagrant', 'ssh', vm_name, "--", "-t", "ip address show eth1 | grep 'inet ' | sed -e 's/^.*inet //' -e 's/\/.*$//'"], capture_output=True, text=True)
            vms[vm_name] = vm_ip.stdout[:-1]
    return vms

import subprocess
import yaml

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
                'master': {'hosts': {}},
                'workers': {'hosts': {}}
            }
        }
    }

    for machine in machines:
        config = get_ssh_config(machine)
        if 'master' in machine:
            inventory['all']['children']['master']['hosts'][machine] = config
        else:
            inventory['all']['children']['workers']['hosts'][machine] = config

    # Записываем inventory.yaml
    with open('inventory.yaml', 'w') as file:
        yaml.dump(inventory, file, default_flow_style=False)

    print("inventory.yaml has been generated successfully!")

if __name__ == "__main__":
    machines = get_vagrant_vms()
    generate_inventory(machines)
