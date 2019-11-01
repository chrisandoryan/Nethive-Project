<?php
// This is our shutdown function, in 
// here we can do any last operations
// before the script is complete.

// function shutdown() {}

// NEED APD PLUGIN
if (function_exists('imap_open')) {
    rename_function('mysqli_fetch_assoc', 'fetch_assoc_original');
    override_function('mysqli_fetch_assoc', '$result', 'return fetch_assoc_override($result);');
}

function fetch_assoc_override($result) {
    $array = fetch_assoc_original($result);
    return $array;
}

$ipAddress = $_SERVER['REMOTE_ADDR'];
$port      = $_SERVER['REMOTE_PORT'];
$execOn = $_SERVER["SCRIPT_FILENAME"];




// if ($execOn == "/var/www/html/DVWA/vulnerabilities/sqli/source/low.php") {
//     echo "HERE!";
//     die("HEHE");
// }


echo $ipAddress . ":" . $port;

// NEED UOPZ PLUGIN
// uopz_set_hook('mysqli_query', function() {
//     $link = $GLOBALS["___mysqli_ston"];
//     $thread_id = mysqli_thread_id($link);
//     print_r($thread_id); // Thread ID always the same as when PHP executed the query.
//     $procs = mysqli_fetch_assoc(mysqli_query($link, "SHOW FULL PROCESSLIST"));
//     print_r($procs['Host']);
// }); 


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