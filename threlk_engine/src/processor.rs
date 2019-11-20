#[derive(Debug, Clone, Serialize, Deserialize, ElasticType)]
pub struct MyType {
    name: String
}

pub fn example(i: MyType) -> MyType {
    MyType {
        name: format!("aero! {}", i.name)
    }
}