param
(
    [Parameter(Mandatory=$true)]
    [String] $HostName
)

& fab restart_apache --set host_name=$HostName
