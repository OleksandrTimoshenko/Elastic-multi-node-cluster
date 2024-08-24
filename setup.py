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
            # usually for private network vagrant use eth1 interface
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

    # Записываем inventory.yaml
    with open('inventory.yaml', 'w') as file:
        yaml.dump(inventory, file, default_flow_style=False)

    print("inventory.yaml has been generated successfully!")

def generate_elasticsearch_configs(hosts):
    # Путь к шаблону
    template_path = './configs/templates/elasticsearch.yml.j2'
    
    # Создание среды Jinja2
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    
    # Загрузка шаблона
    template = env.get_template(os.path.basename(template_path))
    
    # Папка для конфигурационных файлов
    output_dir = './roles/copy_config_to_server/files/'
    os.makedirs(output_dir, exist_ok=True)
    os.system(f"rm -rf {output_dir}/*")

    # Формируем группы для шаблона
    groups = {
        'elasticsearch': [{'host': host, 'ip': ip} for host, ip in hosts.items()],
        'elasticsearch_master': [hosts.get('elasticsearch-master')],
        'elasticsearch_workers': [hosts.get(f'elasticsearch-worker-{i}') for i in range(1, len(hosts) - 1)]
    }
    
    # Создание конфигурационных файлов
    for host, ip in hosts.items():
        if host != "kibana":
            config = template.render(
                ansible_hostname=host,
                ansible_eth1={'ipv4': {'address': ip}},
                groups=groups
            )
            
            filename = f'{host}.yaml'
            
            file_path = os.path.join(output_dir, filename)
            
            # Запись конфигурации в файл
            with open(file_path, 'w') as f:
                f.write(config)
            
            print(f'Конфигурационный файл {filename} успешно создан.')

if __name__ == "__main__":
    machines = get_vagrant_vms()
    generate_inventory(machines)
    generate_elasticsearch_configs(machines)