<?php
die("HEHEHE");

function shutdown()
{
    // This is our shutdown function, in 
    // here we can do any last operations
    // before the script is complete.
    $ipAddress = $_SERVER['REMOTE_ADDR'];
    $port      = $_SERVER['REMOTE_PORT'];

    echo 'Script executed with success', PHP_EOL;
    die();
}

register_shutdown_function('shutdown');