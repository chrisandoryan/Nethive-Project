<?php
    $FUNCOVERRIDE_MODE = 1;
    $TRACEPACKET_MODE = 2;
    $NAMESPACE_MODE = 3;

    //TODO: change this to the desired mode
    $MODE = $NAMESPACE_MODE; 

    switch ($MODE) {
        case $TRACEPACKET_MODE:
            packet_traces();
            break;
        case $FUNCOVERRIDE_MODE:
            function_overrides();
            break;
        case $NAMESPACE_MODE:
            use_namespace();
            break;
    }

    function function_overrides() {
        // need BFR/APD. less reliable, less resource needs.

        if (!function_exists('fetch_assoc_override')) {
            function fetch_assoc_override($result) {
                $ipAddress = $_SERVER['REMOTE_ADDR'];
                $port      = $_SERVER['REMOTE_PORT'];
                $execOn = $_SERVER["SCRIPT_FILENAME"];
            
                echo $ipAddress . ":" . $port;
                $array = fetch_assoc_original($result);
                print_r($array);
                return $array;
            }
        }
        if (function_exists('mysqli_fetch_assoc')) {
            rename_function('mysqli_fetch_assoc', 'fetch_assoc_original');
        }   
        override_function('mysqli_fetch_assoc', '$result', 'return fetch_assoc_override($result);');

    }
    
    function packet_traces() {
        // need UOPZ. more reliable, more resource needs.

        uopz_set_hook('mysqli_query', function() {
            $link = $GLOBALS["___mysqli_ston"];
            $thread_id = mysqli_thread_id($link);
            print_r($link);
            // print_r($thread_id); // Thread ID always the same as when PHP executed the query.
            // $procs = mysqli_fetch_assoc(mysqli_query($link, "SHOW FULL PROCESSLIST"));
            // print_r($procs);
        }); 
    }

    function use_namespace() {
        require "namespace_manager.php";
        //TODO: make every file with db interaction to declare namespace blackhead.

    }