fn main() {
let mut x = 5; // mut x: i32
let mut done = false; // mut done: bool
//loop {
//        println!("Loop forever!");
//}

println!("run while");

while !done {
    x += x - 3;

    println!("{}", x);

    if x % 5 == 0 {
        done = true;
        }
    }  

println!("Not run for format C");
//for (c = 0; c < 10; c++) {
//    printf( "%d\n", c );
//}

for z in 0..10 {
        println!("{}", z); // x: i32
    }

println!("run enumerate");
for (i,j) in (5..10).enumerate() {
        println!("i = {} and j = {}", i, j);
        }

    }
