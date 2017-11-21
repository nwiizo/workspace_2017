#![feature(plugin, decl_macro, custom_derive)]
#![plugin(rocket_codegen)]

extern crate rocket_contrib;
extern crate rocket;

#[cfg(test)] mod tests;

use std::collections::HashMap;

use rocket::outcome::IntoOutcome;
use rocket::request::{self, Form, FlashMessage, FromRequest, Request};
use rocket::response::{Redirect, Flash};
use rocket::http::{Cookie, Cookies};
use rocket_contrib::Template;

#[derive(FromForm)]
struct Login {
    username: String,
    password: String
}

#[derive(Debug)]
struct User(usize);

impl<'a, 'r> FromRequest<'a, 'r> for User {
    type Error = ();

    fn from_request(request: &'a Request<'r>) -> request::Outcome<User, ()> {
        request.cookies()
            .get_private("user_id")
            .and_then(|cookie| cookie.value().parse().ok())
            .map(|id| User(id))
            .or_forward(())
    }
}

#[post("/login", data = "<login>")]
fn login(mut cookies: Cookies, login: Form<Login>) -> Flash<Redirect> {
    if login.get().username == "Sergio" && login.get().password == "password" {
        cookies.add_private(Cookie::new("user_id", 1.to_string()));
        Flash::success(Redirect::to("/"), "Successfully logged in.")
    } else {
        Flash::error(Redirect::to("/login"), "Invalid username/password.")
    }
}

#[post("/logout")]
fn logout(mut cookies: Cookies) -> Flash<Redirect> {
    cookies.remove_private(Cookie::named("user_id"));
    Flash::success(Redirect::to("/login"), "Successfully logged out.")
}

#[get("/login")]
fn login_user(_user: User) -> Redirect {
    Redirect::to("/")
}

#[get("/login", rank = 2)]
fn login_page(flash: Option<FlashMessage>) -> Template {
    let mut context = HashMap::new();
    if let Some(ref msg) = flash {
        context.insert("flash", msg.msg());
    }

    Template::render("login", &context)
}

#[get("/")]
fn user_index(user: User) -> Template {
    let mut context = HashMap::new();
    context.insert("user_id", user.0);
    Template::render("index", &context)
}

#[get("/", rank = 2)]
fn index() -> Redirect {
    Redirect::to("/login")
}

fn rocket() -> rocket::Rocket {
    rocket::ignite()
        .attach(Template::fairing())
        .mount("/", routes![index, user_index, login, logout, login_user, login_page])
}

fn main() {
    rocket().launch();
}
