param
(
    [Parameter(Mandatory=$true)]
    [String] $HostName,
    [Int] $NumLines=10
)

& fab print_error_logs:num_lines=$NumLines --set host_name=$HostName
