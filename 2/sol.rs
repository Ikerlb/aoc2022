use std::io::{BufRead, BufReader};

fn main() {
    let stdin = std::io::stdin();
    let reader = BufReader::new(stdin);

    let lines: Vec<Vec<String>> = reader
        .lines()
        .map(|line| line.unwrap().split(" ").collect())
        .collect();

    // do something with the lines
    for line in lines {
        println!("{} {}", line[0], line[1]);
    }
}
