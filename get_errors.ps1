param
(
    [Parameter(Mandatory=$true)]
    [String] $HostName,
    [Int] $NumLines
)

& fab get_error_logs:num_lines=$NumLines --set host_name=$HostName
