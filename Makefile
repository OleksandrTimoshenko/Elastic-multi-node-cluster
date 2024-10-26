# Vagrant commands
VAGRANT_UP = vagrant up
VAGRANT_DESTROY = vagrant destroy -f

# Python setup script and domain input
PYTHON_SETUP = /usr/bin/python3 ./setup.py
PIP_REQUIREMENTS = pip3 install -r ./requirements.txt

DOMAIN ?= kibana.com
NUM_WORKERS ?= 3

# Ansible playbook
ANSIBLE_PLAYBOOK = ansible-playbook -i inventory.yaml playbook.yaml

# Target for setting up everything (1-3 together)
all: vagrant_up pip setup ansible

# Bring up Vagrant
pip:
	${PIP_REQUIREMENTS}

vagrant_up:
	NUM_WORKERS=$(NUM_WORKERS) vagrant up

# Run Python setup script with domain argument
setup:
	$(PYTHON_SETUP) $(DOMAIN)

# Run Ansible playbook
ansible:
	$(ANSIBLE_PLAYBOOK)

# Destroy Vagrant machines
destroy:
	$(VAGRANT_DESTROY)

# Run Vagrant up, Python setup, and Ansible playbook in sequence
all: vagrant_up setup ansible

# Help output for convenience
help:
	@echo "Available targets:"
	@echo "  pip            - Install python dependencies"
	@echo "  vagrant_up     - Bring up the Vagrant machines (use NUM_WORKERS=<int> to specify number of elasticsearch workers)"
	@echo "  setup          - Run Python setup script (use DOMAIN=<domain> to specify domain)"
	@echo "  ansible        - Run Ansible playbook"
	@echo "  all            - Run Vagrant up, Python setup, and Ansible playbook in sequence"
	@echo "  destroy        - Destroy Vagrant machines"
	@echo
	@echo "  example:       make all DOMAIN=kibana.com NUM_WORKERS=3"

.PHONY: pip vagrant_up setup ansible destroy all help
