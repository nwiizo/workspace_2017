fn main() {
    let x: i32 = 17;
    {
        let y: i32 = 3;
        println!("The value of x is {} and value of y is {}", x, y);
    }
        let y: i32 = 13;
    println!("The value of x is {} and value of y is {}", x, y); // これは動きません
}
