param(
    [string] $ProjectName,
    [string] $HostName
)

# Run this script to deploy your project to a host
# This script just a workaround because I can't be bothered using
# Fabric the way it was intended yet

# Print all projects and hosts is parameters are not provided
if ((-not $ProjectName) -or (-not $HostName))
{
    Write-Host "`nHosts:"
    $hostDir = Join-Path $PSScriptRoot "hosts"
    $hostFiles = Get-ChildItem -Path $hostDir
    foreach ($hostFile in $hostFiles)
    {
        Write-Host "`n"(([String]$hostFile).Split('.'))[0]
        Get-Content (Join-Path $hostDir $hostFile)
    }
    Write-Host "`nProjects:"
    $projectDir = Join-Path $PSScriptRoot "projects"
    $projectFiles = Get-ChildItem -Path $projectDir
    foreach ($projectFile in $projectFiles)
    {
        Write-Host "`n"(([String]$projectFile).Split('.'))[0]
        Get-Content (Join-Path $projectDir $projectFile)
    }
}
else 
{
    & fab set_host:host_name=$HostName deploy:project_name=$ProjectName
}
