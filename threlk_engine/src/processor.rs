extern crate chrono;

use serde_json::{Value, json, to_vec};
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, Serialize, Deserialize, ElasticType)]
struct Beats {
    hostname: String
}

#[derive(Debug, Clone, Serialize, Deserialize, ElasticType)]
pub struct BashLog {
    message: String,
    agent: Beats,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BashMsg {
    pub user: String,
    pub cmd: String,
    pub cwd: String,
    pub time: String,
    pub user_ip: String,
    pub hostname: String
}

pub fn clean_bash_log(i: BashLog) -> BashMsg {
    let data = i.message
        .split(" : ")
        .collect::<Vec<&str>>();

    assert_eq!(data.len(), 4);

    let usr_host = data[1]
        .split("@")
        .collect::<Vec<&str>>();

        assert_eq!(usr_host.len(), 2);

    BashMsg {
        user: usr_host[0].to_string(),
        cmd: data[3].to_string(),
        cwd: data[2].to_string(),
        time: data[0].to_string(),
        user_ip: usr_host[1].to_string(),
        hostname: i.agent.hostname.to_string()
    }
}