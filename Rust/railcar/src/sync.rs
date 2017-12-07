use nix::fcntl::O_CLOEXEC;
use nix::unistd::{pipe2, read, close};
use std::os::unix::io::RawFd;
use super::Result;

pub struct Cond {
    rfd: RawFd,
    wfd: RawFd,
}

impl Cond {
    pub fn new() -> Result<Cond> {
        let (rfd, wfd) = pipe2(O_CLOEXEC)?;
        Ok(Cond { rfd: rfd, wfd: wfd })
    }

    pub fn wait(&self) -> Result<()> {
        close(self.wfd)?;
        let data: &mut [u8] = &mut [0];
        while read(self.rfd, data)? != 0 {}
        close(self.rfd)?;
        Ok(())
    }
    pub fn notify(&self) -> Result<()> {
        close(self.rfd)?;
        close(self.wfd)?;
        Ok(())
    }
}
