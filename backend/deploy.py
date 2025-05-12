"""
Quick script to deploy updated backend to Azure Container Apps
"""
import os
import subprocess
import sys

def run_command(command):
    """Run a shell command and print output"""
    print(f"Running: {command}")
    process = subprocess.Popen(
        command, 
        shell=True, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    
    if stdout:
        print(f"STDOUT: {stdout.decode()}")
    if stderr:
        print(f"STDERR: {stderr.decode()}")
        
    return process.returncode

def main():
    # Build the Docker image
    print("Building Docker image...")
    build_cmd = "docker build -t storyteller-backend ."
    if run_command(build_cmd) != 0:
        print("Error building Docker image")
        sys.exit(1)
    
    # Tag the image for the Azure Container Registry
    acr_name = os.environ.get("ACR_NAME", "storytellerregistry")
    print(f"Tagging image for {acr_name}...")
    tag_cmd = f"docker tag storyteller-backend {acr_name}.azurecr.io/storyteller-backend:latest"
    if run_command(tag_cmd) != 0:
        print("Error tagging image")
        sys.exit(1)
        
    # Login to Azure Container Registry (ensure you're logged into Azure CLI)
    print("Logging into Azure Container Registry...")
    login_cmd = f"az acr login --name {acr_name}"
    if run_command(login_cmd) != 0:
        print("Error logging into ACR. Make sure you're logged into Azure CLI first.")
        sys.exit(1)
    
    # Push the image to ACR
    print("Pushing image to ACR...")
    push_cmd = f"docker push {acr_name}.azurecr.io/storyteller-backend:latest"
    if run_command(push_cmd) != 0:
        print("Error pushing image to ACR")
        sys.exit(1)
    
    # Update the Azure Container App
    print("Updating Azure Container App...")
    update_cmd = "az containerapp update --name storyteller-backend --resource-group storyteller-rg --image {acr_name}.azurecr.io/storyteller-backend:latest"
    if run_command(update_cmd) != 0:
        print("Error updating Azure Container App")
        sys.exit(1)
    
    print("Deployment completed successfully!")

if __name__ == "__main__":
    main()
