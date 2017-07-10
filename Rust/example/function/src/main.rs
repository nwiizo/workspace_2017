fn main() {
        print_sum(5, 6);
        println!("input plus one:{}",add_one(16));
}

fn print_sum(x: i32, y: i32) {
        println!("sum is: {}", x + y);
}

fn add_one(z: i32) -> i32 {
        //-> で返り値の型を定義します。
        z+1
        //z+1;
        //セミコロンを付ければ、それは代わりに () を返します。

}
