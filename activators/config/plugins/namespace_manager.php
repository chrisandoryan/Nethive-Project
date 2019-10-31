<?php
    namespace blackhead;
    use mysqli;

    //MAGIC: if I put include memcache_manager here (on the global scope), I cannot use them inside the function even if global $mem has been declared.

    function mysqli_query($link, $query) {
        include_once "memcache_manager.php";

        $result = $link->query($query);
        $data = $result->fetch_all(MYSQLI_ASSOC);
        
        // use the data here
        $ipAddress = $_SERVER['REMOTE_ADDR'];
        $port      = $_SERVER['REMOTE_PORT'];
        $execOn = $_SERVER["SCRIPT_FILENAME"];
    
        echo $ipAddress . ":" . $port;
        print_r($data);

        //TODO: sync with memcache

        $memres = $mem->get($ipAddress);
        print_r($memres);

        // end here

        $result->data_seek(0); // reset result pointer back to 0
        return $result;
    }

    function mysqli_fetch_assoc($result) {
        return $result->fetch_assoc();
    }