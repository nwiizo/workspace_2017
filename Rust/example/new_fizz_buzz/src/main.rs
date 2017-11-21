fn main() {
    let rangest = (0..100).map(|x| x + 1);
    rangest.filter(|x| x % 15 == 0).for_each(|i| println!("Fizzbuzz:{}", i));
}
