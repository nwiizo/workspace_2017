#![feature(plugin, decl_macro)]
#![plugin(rocket_codegen)]

extern crate rocket;

#[get("/")]
fn hello() -> &'static str {
    "Hello, world!"
}

fn rocket() -> rocket::Rocket {
    rocket::ignite().mount("/", routes![hello])
}

fn main() {
    rocket().launch();
}

#[cfg(test)]
mod test {
    use super::rocket;
    use rocket::local::Client;
    use rocket::http::Status;

    #[test]
    fn test_hello() {
        let client = Client::new(rocket()).unwrap();
        let mut response = client.get("/").dispatch();
        assert_eq!(response.status(), Status::Ok);
        assert_eq!(response.body_string(), Some("Hello, world!".into()));
    }
}
