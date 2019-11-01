<?php
    $mem = new Memcached();
    if (!count($mem->getServerList()))
    {
        $mem->addServer("127.0.0.1", 11211);
    }
    $mem->setOption(Memcached::OPT_COMPRESSION, false);
