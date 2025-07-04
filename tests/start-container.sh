#!/bin/bash

# Check if Docker Desktop is running, and start it if it is not
if docker info >/dev/null 2>&1; then
    echo "Docker is running."
else
    echo "Starting Docker Desktop..."
    open -a "Docker"
    echo "Waiting for Docker Desktop to start..."
    while ! docker info >/dev/null 2>&1; do
        sleep 2
    done
    echo "Docker Desktop is now running."
fi

docker run  --rm -it \
            --name ansible-dev \
            -v "$(pwd):/my-ansible-project/ansible_collections/pcg/alpaca_operator" \
            -v "$(pwd)/templates:/my-ansible-project/templates" \
            -v "$(pwd)/tests:/my-ansible-project/tests" \
            python:3.8-slim bash -c "apt-get update && \
                                     apt-get install -y --no-install-recommends sshpass openssh-client && \
                                     pip install --upgrade pip && \
                                     pip install ansible-core requests && \
                                     cd /my-ansible-project/tests && \
                                     clear && \
                                     echo 'You can now run e.g.: \"ansible-playbook ../templates/playbooks/template_stack_create.yml\"' && \
                                     bash"