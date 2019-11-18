#[macro_use]
extern crate crossbeam;

extern crate elastic;
#[macro_use]
extern crate elastic_derive;

#[macro_use]
extern crate serde_derive;
extern crate serde;

use std::error::Error;
use base64::{encode, decode};

#[derive(Debug, Serialize, Deserialize, ElasticType)]
struct MyType {
    name: String
}

fn main() -> Result<(), Box<dyn Error>>{
    use elastic::http::header::{self, AUTHORIZATION, HeaderValue};
    use elastic::client::SyncClientBuilder;
    use serde_json::json;

    let creds = base64::encode("elastic:changeme");
    let auth = HeaderValue::from_str(&format!("Basic {}", creds))?;

    println!("{:?}", auth);

    let builder = SyncClientBuilder::new()
        .static_node("http://192.168.56.104:9200")
        .params_fluent(move |p| p
            .url_param("pretty", true)
            .header(AUTHORIZATION, auth.clone()));

    let client = builder.build()?;
    
    println!("sending request");

    let query = "Jean Doe";

    let response = client.search::<MyType>()
                     .index("customer")
                     .body(json!({
                         "query": {
                             "query_string": {
                                 "query": query
                             }
                         }
                     }))
                     .send()?;

    for hit in response.hits() {
        println!("{:?}", hit);
    }

    Ok(())
}

#[test]
fn test_chan_timer() {
    use std::time::Duration;

    println!("Hello, timer");

    let tick = crossbeam::tick(Duration::from_millis(1000));
    let tock = crossbeam::tick(Duration::from_millis(3000));

    

    loop {
        select! {
            recv(tick) -> _ => sleep_print("tick"),
            recv(tock) -> _ => sleep_print("tock")
        }
    }
}

fn sleep_print(s: &str) {
    use std::time::Duration;
    use std::{thread, time};

    thread::sleep(Duration::from_millis(5000));
    println!("{}", s);
}

#[test]
fn test_threadpool() {
    use threadpool::ThreadPool;
    use std::time::Duration;
    use std::thread::sleep;

    let tick = crossbeam::tick(Duration::from_millis(1000));
    let tock = crossbeam::tick(Duration::from_millis(3000));

    let pool = ThreadPool::new(10);
    loop {
        select! {
            recv(tick) -> _ => pool.execute(|| sleep_print("tick")),
            recv(tock) -> _ => pool.execute(|| sleep_print("tock"))
        }
    }

    //sleep(Duration::from_secs(1)); // wait for threads to start
}
