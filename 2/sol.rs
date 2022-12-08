use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let stdin = stdin.lock();
    let lines = stdin.lines();
    let v: Vec<_> = lines
        .map(|line| line
             .unwrap()
             .split(" ")
             .map(|c| c.to_owned())
             .collect::<Vec<_>>())
        .collect();

    for line in v {
        println!("{} {}", line[0], line[1]);
    }
}
