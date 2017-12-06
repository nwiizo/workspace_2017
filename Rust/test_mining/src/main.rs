use std::fmt;
use sha2::Sha256;

fn main() {
    let version = 4;
    let prev_block = "0000000000000000005629ef6b683f8f6301c7e6f8e796e7c58702a079db14e8";
    let markle_root = "efb8011cb97b5f1599b2e18f200188f1b8207da2884392672f92ac7985534eeb";
    let timestamp = "2016-01-30 13:23:09";
    let bits = "403253488";
    let nonce = "1448681410";

    let mut version_h = format!("{:08}", version);
    version_h = version_h.chars().rev().collect::<String>();    
    let prev_block_h = prev_block.chars().rev().collect::<String>();
    let markle_root_h = markle_root.chars().rev().collect::<String>();
// python timestamp_s = int((datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")-datetime(1970,1,1)).total_seconds())
    let mut timestamp_h = "1454160189";
    timestamp_h = format!("{:x}",timestamp_h);
    timestamp_h = timestamp_h.chars().rev().collect::<String>();
    let mut bits_h = format!("{:x}",bits);
    let mut nonce_h = format!("{:x}",nonce);
    bits_h = bits_h.chars().rev().collect::<String>();
    nonce_h = nonce_h.chars().rev().collect::<String>();
    
    let header = format!("{}{}{}{}{}{}",version_h,prev_block_h,markle_root_h,timestamp_h,bits_h,nonce_h)
    let mut hasher = Sha256::default();
    let mut output = hasher.input(hasher.input(header));
    output_h = format!("{:x}",output);
    output_h = output.chars().rev().collect::<String>();
    println!("{}",output_h);
}
