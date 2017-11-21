use rocket::response::NamedFile;

use std::io;
use std::path::{Path, PathBuf};

#[get("/")]
fn index() -> io::Result<NamedFile> {
    NamedFile::open("static/index.html")
}

#[get("/<file..>", rank = 2)]
fn files(file: PathBuf) -> io::Result<NamedFile> {
    NamedFile::open(Path::new("static/").join(file))
}
