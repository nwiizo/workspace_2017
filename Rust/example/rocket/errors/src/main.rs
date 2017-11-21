#![feature(plugin, decl_macro)]
#![plugin(rocket_codegen)]

extern crate rocket;

#[cfg(test)] mod tests;

use rocket::response::content;

#[get("/hello/<name>/<age>")]
fn hello(name: String, age: i8) -> String {
    format!("Hello, {} year old named {}!", age, name)
}

#[catch(404)]
fn not_found(req: &rocket::Request) -> content::Html<String> {
    content::Html(format!("<p>Sorry, but '{}' is not a valid path!</p>
            <p>Try visiting /hello/&lt;name&gt;/&lt;age&gt; instead.</p>",
            req.uri()))
}

fn main() {
    let e = rocket::ignite()
        // .mount("/", routes![hello, hello]) // uncoment this to get an error
        .mount("/", routes![hello])
        .catch(catchers![not_found])
        .launch();

    println!("Whoops! Rocket didn't launch!");
    println!("This went wrong: {}", e);
}
