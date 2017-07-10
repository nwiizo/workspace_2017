fn main() {
    s_copy();
    let a = 5;
    let _y = double(a);
    println!("{}",a);
    
    let b = true;
    let _y = change_truth(b);
    println!("{}",b)
}

fn foo() {
    let v_v = vec![1, 2, 3];
}
fn double(x: i32) -> i32 {
        x * 2
}
fn s_copy(){
    let v = 1;
    let v2 = v;
    println!("v is: {}", v);
}

fn change_truth(x: bool) -> bool {
        !x
}
//let v = vec![1, 2, 3];
//let v2 = v;
//所有権がなくうごかない元の束縛を使うことができない
//println!("v[0] is: {}", v[0]);
