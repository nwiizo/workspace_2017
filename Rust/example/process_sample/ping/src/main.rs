use std::error::Error;
use std::io::prelude::*;
use std::process::{Command, Stdio};

fn main() {
    let output = Command::new("ping")
    .arg("-c 1")
    .arg("8.8.8.8")
    .output()
    .expect("failed to execute process");

    let ping = output.stdout;
    println!("{}", std::str::from_utf8(&ping).unwrap());
    let pong = output.stderr;
    println!("{}", std::str::from_utf8(&pong).unwrap());
}
