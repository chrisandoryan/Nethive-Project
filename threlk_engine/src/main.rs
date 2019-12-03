#[macro_use]
extern crate crossbeam;
use crossbeam::channel;

extern crate elastic;
#[macro_use]
extern crate elastic_derive;

#[macro_use]
extern crate serde_derive;
extern crate serde;

#[macro_use] 
extern crate log;

extern crate kafka;

use std::time::Duration;
use std::thread;
use threadpool::ThreadPool;

mod es;
mod processor;

use kafka::producer::{Producer, Record, RequiredAcks};
use serde_json::{Value, json, to_vec};
use processor::BashLog;

const KAFKA_SERVER_ADDR: &str = "localhost:9092";
const TOPIC: &str = "LEXY";

fn main() {
    println!("Initiating.");
    env_logger::init();

    let (s_raw, r_raw) = channel::unbounded();
    let (s, r) = channel::unbounded();
    let tick = crossbeam::tick(Duration::from_millis(1000));
    let tpool = ThreadPool::new(4);

    let t0 = thread::spawn(move || {
        loop {
            tick.recv().unwrap();
            
            let resp = es::fetch_data::<BashLog>(String::from("nethive-bash-*"), json!({
                "query": {
                    "match": {
                        "log_type": "TYPE_BASH_CENTRALIZED"
                    }
                }
            }));

            for hit in resp.hits() {
                let doc = hit.document().unwrap().clone();
                s_raw.send(doc).unwrap();
            }
        }
    });
    info!("es data input thread started");

    let t1 = thread::spawn(move || {
        loop {
            let data = r_raw.recv().unwrap();

            let ss = s.clone();
            tpool.execute(move || {
                let output = processor::clean_bash_log(data);
                ss.send(output).unwrap();
            });
        }
    });
    info!("correlation thread pool started");

    let t2 = thread::spawn(move || {
        let mut producer = Producer::from_hosts(vec!(String::from(KAFKA_SERVER_ADDR)))
            .with_ack_timeout(Duration::from_secs(1))
            .with_required_acks(RequiredAcks::One)
            .create()
            .unwrap();

        loop {
            let data = r.recv().unwrap();

            println!("Get: {}", data.cmd);

            let status = producer.send(&Record::from_value(TOPIC, serde_json::to_vec(&data).unwrap())).unwrap();
            println!("LEXY: {:?}", status);
        }
    });
    info!("kafka producer thread started");

    t0.join().unwrap();
    t1.join().unwrap();
    t2.join().unwrap();
}