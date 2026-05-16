#!/bin/bash

# Assign arguments
images_file="images.txt"
container_registry="699955796816.dkr.ecr.ap-southeast-1.amazonaws.com"
platform="linux/amd64"  # Set default platform or make this a parameter

# Enable Docker BuildKit
export DOCKER_BUILDKIT=1

# Initialize builder
docker buildx create --use
docker buildx inspect --bootstrap

# Login to ECR
# aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin "$container_registry"

# Read images from file and build each one
while IFS= read -r name || [[ -n "$name" ]]; do
    # Skip empty lines and comments
    [[ -z "$name" || "$name" == \#* ]] && continue
    
    echo "Building $name..."
    
    # Construct and execute build command
    docker_build_command="docker buildx build -f $name/Dockerfile --platform $platform -t $container_registry/$name:v1.0.8 . --push"
    
    if ! $docker_build_command; then
        echo "Error building $name"
        exit 1
    fi
    
    echo "Successfully built and pushed $name"
done < "$images_file"

echo "All images built and pushed successfully"

### Test 01