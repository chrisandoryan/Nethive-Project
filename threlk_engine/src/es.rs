
use std::time::Duration;
use crossbeam;
use std::thread;
use crossbeam::channel;

use elastic::http::header::{self, AUTHORIZATION, HeaderValue};
use elastic::client::{responses::search, SyncClientBuilder};
use elastic::prelude::SearchResponse;
use serde_json::{Value, json};

pub fn fetch_data<T>(index: String, request: Value) -> SearchResponse<T> 
where for<'de> T: serde::Deserialize<'de> {
    let creds = base64::encode("elastic:changeme");
    let auth = HeaderValue::from_str(&format!("Basic {}", creds)).unwrap();

    println!("{:?}", auth);

    let builder = SyncClientBuilder::new()
        .static_node("http://192.168.56.104:9200")
        .params_fluent(move |p| p
            .url_param("pretty", true)
            .header(AUTHORIZATION, auth.clone()));

    let client = builder.build().unwrap();
    
    println!("sending request");

    let response = client.search()
                    .index(index)
                    .body(request)
                    .send()
                    .unwrap();

    return response;
} 

// pub fn periodic_data_fetch<T: std::marker::Sync + std::marker::Send + 'static>(sender: &'static channel::Sender<&T>, interval: Duration) 
// where for<'de> T: serde::Deserialize<'de> {
    // let tick = crossbeam::tick(interval);

    // thread::spawn(move || {
    //     loop {
    //         tick.recv().unwrap();
    //         let resp = fetch_data::<T>(String::from("customer"), json!({
    //             "query": {
    //                 "query_string": {
    //                     "query": "joan doe"
    //                 }
    //             }
    //         }));

    //         for hit in resp.hits() {
    //             let doc = hit.document().unwrap();
    //             sender.send(doc).unwrap();
    //         }
    //     }
    // });
// }