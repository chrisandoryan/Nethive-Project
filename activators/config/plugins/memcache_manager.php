<?php
    $mem = new Memcached();
    $mem->addServer("127.0.0.1", 11211);

    $foo = "HEHEHEHE";