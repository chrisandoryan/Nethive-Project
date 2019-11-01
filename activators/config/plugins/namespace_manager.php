<?php
    namespace blackhead;

    //MAGIC: if I put include memcache_manager here (on the global scope), I cannot use them inside the function even if global $mem has been declared.

    function mysqli_query($link, $query) {

        $result = $link->query($query);

        if (mysqli_num_rows($result) > 0) {

            $data = $result->fetch_all(MYSQLI_ASSOC);

            $ipAddress = $_SERVER['REMOTE_ADDR'];
            $port      = $_SERVER['REMOTE_PORT'];
            $execOn = $_SERVER["SCRIPT_FILENAME"];
            
            echo $ipAddress . ":" . $port;

            //TODO: sync with python engine

            if (count($data) > 0) {
                $package = array(
                    'client_ip' => $ipAddress,
                    'client_port' => $port,
                    'sql_response' => $data
                );

                // print_r($package);
            
                $fp = fsockopen("127.0.0.1", 5128, $errno, $errstr, 30);
                if (!$fp) {
                    echo "$errstr ($errno)<br />\n";
                } else {
                    fwrite($fp, json_encode($package));
                    fclose($fp);
                }
            }

            $result->data_seek(0); // reset result pointer back to 0
        }

        return $result;        
    }