extern crate curl;

use std::io::{stdout, Write};

use curl::easy::Easy;

// Print a web page onto stdout
fn main() {
    let mut easy = Easy::new();
    let mut target_url = "https://gmo.jp/";
    easy.url(target_url).unwrap();
    easy.write_function(|data| {Ok(stdout().write(data).unwrap())}).unwrap();
    easy.perform().unwrap();    
    println!("URL:{} response:{}",target_url,easy.response_code().unwrap());
}
