param(
    [String] $ProjectName,
    [String] $HostName,
    [String] $BranchName = "master"
)

# Run this script to deploy your project to a host
# This script wraps fab because PowerShell is nice to invoke.

if ($ProjectName -and $HostName)
{
    & fab deploy --set host_name=$HostName,project_name=$ProjectName,branch_name=$BranchName
}
else 
{
   # Print all projects and hosts
    Write-Host "`nHosts:"
    $hostDir = Join-Path $PSScriptRoot "hosts"
    $hostFiles = Get-ChildItem -Path $hostDir
    ForEach ($hostFile in $hostFiles)
    {
        Write-Host "`n"(([String]$hostFile).Split('.'))[0]
        Get-Content (Join-Path $hostDir $hostFile)
    }

    Write-Host "`nProjects:"
    $projectDir = Join-Path $PSScriptRoot "projects"
    $projectFiles = Get-ChildItem -Path $projectDir
    ForEach ($projectFile in $projectFiles)
    {
        Write-Host "`n"(([String]$projectFile).Split('.'))[0]
        Get-Content (Join-Path $projectDir $projectFile)
    }
}