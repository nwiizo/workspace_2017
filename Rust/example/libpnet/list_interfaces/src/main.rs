
extern crate pnet_datalink;

fn main() {
    for interface in pnet_datalink::interfaces() {
        let mac = interface.mac.map(|mac| mac.to_string()).unwrap_or("N/A".to_owned());
        println!("{}:", interface.name);
        println!("  index: {}", interface.index);
        println!("  flags: {}", interface.flags);
        println!("  MAC: {}", mac);
        println!("  IPs:");
        for ip in interface.ips {
            println!("    {:?}", ip);
        }
    }
}
