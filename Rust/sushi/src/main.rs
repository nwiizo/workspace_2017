use std::thread;
use std::io::Write;
use std::io::stdout;
use std::string::String;

fn main(){
    let interval = 400;
    for x in 1i32..180{
        thread::sleep_ms(interval);
        //print!("\r{:?}", fb(x));
        print!("\r\r{:?}", fb(x));
        stdout().flush();
    }
}

fn fb(i: i32) {    
    if i % 15 == 0 {
        print!("FizzBuzz");
    } else if i % 5 == 0 {
        print!("Buzz    ");
    } else if i % 3 == 0 {
        print!("Fizz    ");
    } else {
        print!("{:08}",i);
    };
}

