use std::io::{self, BufRead};

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let mut v = stdin
        .lock()
        .lines()
        .collect::<io::Result<Vec<String>>>()?
        .split(|s| s == "")
        .map(|slice| slice
             .iter()
             .map(|sn| sn.parse::<usize>().unwrap()).sum::<usize>())
        .collect::<Vec<usize>>();

    v.sort();

    println!("part 1: {}", v.last().unwrap());
    println!("part 2: {}", v.iter().rev().take(3).sum::<usize>());

    Ok(())
}
