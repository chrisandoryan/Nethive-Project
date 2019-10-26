<?php

// function shutdown()
// {
    
// }

// This is our shutdown function, in 
// here we can do any last operations
// before the script is complete.
$ipAddress = $_SERVER['REMOTE_ADDR'];
$port      = $_SERVER['REMOTE_PORT'];
$execOn = $_SERVER["SCRIPT_FILENAME"];
// if ($execOn == "/var/www/html/DVWA/vulnerabilities/sqli/source/low.php") {
//     echo "HERE!";
//     die("HEHE");
// }
echo $ipAddress . ":" . $port;
uopz_set_hook('mysqli_fetch_assoc', function() {
    print("HEHEHEHEHEHEHEHEHE");
    print_r($result);
    $link = $GLOBALS["___mysqli_ston"];
    $thread_id = mysqli_thread_id($link);
    // $result = mysqli_query($link,"SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST");
    // $proc = mysqli_fetch_assoc($result);
    // print_r($link);
    // print_r($proc);
}); 
// print_r(mysqli_get_links_stats());
// mysqli_options ($link , MYSQLI_INIT_COMMAND, "show full processlist" );
// if (isset($GLOBALS["___mysqli_ston"])) {
//     print_r($GLOBALS["___mysqli_ston"]);
//     die(mysqli_get_host_info($GLOBALS["___mysqli_ston"]));
// }
// else {
//     print_r("GADA!");
// }
// die($ipAddress);

// shutdown();

// register_shutdown_function('shutdown');