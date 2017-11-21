#![feature(plugin, decl_macro)]
#![plugin(rocket_codegen)]
extern crate rocket;

#[cfg(test)]
mod tests;

use rocket::response::Redirect;
use rocket::http::RawStr;

#[get("/")]
fn root() -> Redirect {
    Redirect::to("/users/login")
}

#[get("/users/<name>")]
fn user(name: &RawStr) -> Result<&'static str, Redirect> {
    match name.as_str() {
        "Sergio" => Ok("Hello, Sergio!"),
        _ => Err(Redirect::to("/users/login")),
    }
}

#[get("/users/login")]
fn login() -> &'static str {
    "Hi! That user doesn't exist. Maybe you need to log in?"
}

fn main() {
    rocket::ignite().mount("/", routes![root, user, login]).launch();
}
