<#
.SYNOPSIS
Reads environment variables from an EXISTING Azure Container App and creates a NEW
test Container App using those variables, with specific overrides.

.DESCRIPTION
This script fetches the environment variable configuration from a specified source
Azure Container App. It then creates a new test Container App, copying the environment
variables from the source but overriding the DATABASE_URL for the test app's
persistent storage mount. Uses Docker Hub as the default registry.

.NOTES
- Requires Azure CLI to be installed and logged in (`az login`).
- Requires PowerShell 5.1 or later.
- Adjust the source/target app names, resource group, ACA environment, image,
  and database URL override as needed.
- Assumes the source app exists and has environment variables configured.
- This script copies regular environment variables. If the source app uses
  secrets (secretRef), this script currently doesn't copy the secret definitions,
  only the reference. You'd need to ensure secrets with the same names exist
  in the target environment or add logic to create them.
#>

param(
    [string]$SourceResourceGroup = "storyteller-rg",
    [string]$SourceAppName = "storyteller-backend",       # <-- Name of your EXISTING app to copy from
    [string]$TargetResourceGroup = "storyteller-rg",      # <-- RG for the NEW test app
    [string]$TargetAppName = "storyteller-backend-test", # <-- Name for the NEW test app
    [string]$ContainerAppEnv = "storyteller-env",          # <-- Your ACA Environment name
    [string]$TargetDockerImage = "ajmalrasouli/storyteller-backend:test", # <-- Image for the NEW test app (from Docker Hub)
    [string]$DatabaseUrlOverride = "sqlite:////data/stories.db" # <-- Specific DB path for NEW test app
    # Optional: Add parameters for Docker Hub credentials if needed for private repos
    # [string]$RegistryUsername = "",
    # [string]$RegistryPassword = "" # Use a Personal Access Token (PAT) here
)

# --- Configuration ---
Write-Host "Source App: $SourceAppName (in RG: $SourceResourceGroup)"
Write-Host "Target App: $TargetAppName (in RG: $TargetResourceGroup)"
Write-Host "Target Image: $TargetDockerImage (from Docker Hub)"
Write-Host "ACA Environment: $ContainerAppEnv"
Write-Host "Database URL Override for Target: $DatabaseUrlOverride"

# --- Validate Required Parameters ---
if ([string]::IsNullOrWhiteSpace($TargetAppName)) { throw "Script Error: Target App Name parameter is missing or empty." }
if ([string]::IsNullOrWhiteSpace($TargetResourceGroup)) { throw "Script Error: Target Resource Group parameter is missing or empty." }
if ([string]::IsNullOrWhiteSpace($ContainerAppEnv)) { throw "Script Error: Target ACA Environment parameter is missing or empty." }
if ([string]::IsNullOrWhiteSpace($TargetDockerImage)) { throw "Script Error: Target Docker Image parameter is missing or empty." }


# --- Get Environment Variables from Source App ---
Write-Host "Fetching environment variables from source app '$SourceAppName'..."
try {
    $sourceEnvJson = az containerapp show --name $SourceAppName --resource-group $SourceResourceGroup --query "properties.template.containers[0].env" --output json --only-show-errors
    if ($null -eq $sourceEnvJson -or $sourceEnvJson -eq "") {
         Write-Warning "Warning: Could not retrieve environment variables from source app '$SourceAppName'. It might not exist, have containers, or env vars defined. Continuing with defaults."
         $sourceEnvVars = @()
    } else {
        $sourceEnvVars = $sourceEnvJson | ConvertFrom-Json
    }
}
catch {
    Write-Error "Error executing 'az containerapp show' or parsing JSON: $($_.Exception.Message)"
    exit 1
}
if ($null -eq $sourceEnvVars) { $sourceEnvVars = @() }
Write-Host "Successfully processed environment variables from source."

# --- Prepare Environment Variables for Target App ---
$targetAzEnvVarsList = [System.Collections.Generic.List[string]]::new()
foreach ($envVar in $sourceEnvVars) {
    if ($null -ne $envVar -and $envVar.PSObject.Properties.Match('name').Count -gt 0) {
        $varName = $envVar.name
        $varValue = $null; $secretRef = $null
        if ($envVar.PSObject.Properties.Match('value').Count -gt 0) { $varValue = $envVar.value }
        if ($envVar.PSObject.Properties.Match('secretRef').Count -gt 0) { $secretRef = $envVar.secretRef }

        if ([string]::IsNullOrWhiteSpace($varName)) { Write-Warning "Skipping environment variable with empty name found in source."; continue }

        if ($varName -eq "DATABASE_URL") {
            $targetAzEnvVarsList.Add("DATABASE_URL=$DatabaseUrlOverride")
            Write-Host "Overriding '$varName' with '$DatabaseUrlOverride'"
        } elseif ($null -ne $secretRef -and -not [string]::IsNullOrWhiteSpace($secretRef)) {
            $targetAzEnvVarsList.Add("$varName=secretref:$secretRef")
            Write-Host "Copying secret reference '$varName=secretref:$secretRef' (Ensure secret exists!)"
        } elseif ($envVar.PSObject.Properties.Match('value').Count -gt 0) {
            $targetAzEnvVarsList.Add("$varName=$varValue")
        } else {
             Write-Warning "Skipping variable '$varName' from source (no value/secretRef)."
        }
    } else { Write-Warning "Skipping potentially invalid environment variable entry found in source." }
}
if (-not ($targetAzEnvVarsList | Where-Object { $_.StartsWith("DATABASE_URL=") })) {
     $targetAzEnvVarsList.Add("DATABASE_URL=$DatabaseUrlOverride")
     Write-Host "Adding DATABASE_URL (was not found in source): $DatabaseUrlOverride"
}
$targetAzEnvVarsArray = $targetAzEnvVarsList.ToArray() # Get the final array for the command
Write-Host "Prepared environment variables for target app '$TargetAppName'."


# --- Create Target Azure Container App using Azure CLI (Manual Command Construction) ---
Write-Host "Attempting to create Azure Container App '$TargetAppName'..."

# Build the core command string manually, quoting values appropriately
# Using single quotes for simple string values, less likely to cause issues
$command = "az containerapp create --name '$TargetAppName' --resource-group '$TargetResourceGroup' --environment '$ContainerAppEnv' --image '$TargetDockerImage' --target-port 5000 --ingress external" # <-- SPECIFIES DOCKER HUB

# Add registry credentials IF provided via parameters (for private Docker Hub repos)
if (-not [string]::IsNullOrWhiteSpace($RegistryUsername)) {
    $command += " --registry-username '$RegistryUsername'"
    Write-Host "Adding Docker Hub username."
     if (-not [string]::IsNullOrWhiteSpace($RegistryPassword)) {
        # IMPORTANT: Use a Docker Hub Personal Access Token (PAT) here, not your actual password!
        $command += " --registry-password '$RegistryPassword'"
        Write-Host "Adding Docker Hub password/token."
     } else {
         Write-Warning "RegistryUsername provided but RegistryPassword is missing. Authentication might fail."
     }
}


# Add the environment variables using the --env-vars parameter.
if ($targetAzEnvVarsArray.Count -gt 0) {
    # Join the array elements with spaces, ensuring proper quoting if values have spaces
    $envVarsString = ($targetAzEnvVarsArray | ForEach-Object { "'$_'" }) -join " " # Quote each "KEY=VALUE" pair
    $command += " --env-vars $envVarsString"
}

Write-Host "Final command to execute: $command" # See the full command
Write-Host "Executing Azure CLI command..."

try {
    Invoke-Expression -Command $command

    # Check the exit code immediately
    if ($LASTEXITCODE -ne 0) {
        throw "Azure CLI command failed with exit code $LASTEXITCODE."
    }

    Write-Host "Azure Container App '$TargetAppName' creation command reported success (exit code 0)."
    Write-Host "Note: Provisioning might take a few minutes. Check Azure Portal or use 'az containerapp show' for status."
}
catch {
    Write-Error "Script Error or Azure CLI command failed: $($_.Exception.Message)"
    exit 1
}