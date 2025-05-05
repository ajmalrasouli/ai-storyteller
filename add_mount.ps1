<#
.SYNOPSIS
Mounts Azure Blob Storage to Container App using direct YAML configuration
#>

param(
    [string]$AppName = "storyteller-backend-test",
    [string]$ResourceGroup = "storyteller-rg",
    [string]$StorageAccountName = "storytellerdata2025",
    [string]$StorageContainerName = "sqlitedata",
    [string]$VolumeName = "sqlite-data",
    [string]$MountPath = "/data"
)

# Verify Azure CLI is available
try {
    $null = az version
}
catch {
    Write-Error "Azure CLI not found. Please install and log in with 'az login'"
    exit 1
}

# Get storage account key
Write-Host "Retrieving storage account key..."
$storageAccountKey = az storage account keys list `
    --account-name $StorageAccountName `
    --resource-group $ResourceGroup `
    --query "[0].value" `
    --output tsv

if ([string]::IsNullOrWhiteSpace($storageAccountKey)) {
    Write-Error "Failed to retrieve storage account key"
    exit 1
}

# Get current container name
$containerName = az containerapp show `
    --name $AppName `
    --resource-group $ResourceGroup `
    --query "properties.template.containers[0].name" `
    --output tsv

if ([string]::IsNullOrWhiteSpace($containerName)) {
    $containerName = $AppName
    Write-Warning "Using app name as container name"
}

# Create YAML configuration
$yamlContent = @"
properties:
  template:
    volumes:
    - name: $VolumeName
      storageType: AzureBlob
      storageName: $VolumeName
      azureBlob:
        accountName: $StorageAccountName
        accountKey: $storageAccountKey
        containerName: $StorageContainerName
    containers:
    - name: $containerName
      volumeMounts:
      - volumeName: $VolumeName
        mountPath: $MountPath
"@

# Create temporary file
$yamlFile = New-TemporaryFile
$yamlContent | Out-File -FilePath $yamlFile.FullName -Encoding utf8

# Apply configuration
Write-Host "Applying storage mount configuration..."
az containerapp update `
    --name $AppName `
    --resource-group $ResourceGroup `
    --yaml $yamlFile.FullName

# Clean up
Remove-Item $yamlFile.FullName -ErrorAction SilentlyContinue

Write-Host "Storage mount configuration completed successfully."
Write-Host "Allow a few minutes for the new revision to deploy."
