use std::io::{self, BufRead};

fn parse_line(line: &str) -> (&str, &str) {
    let mut iter = line.split(' ');
    (iter.next().unwrap(), iter.next().unwrap())
}

fn part1(p1: &str, p2: &str) -> usize {
    match (p1, p2) {
        ("A", "X") => 1 + 3,
        ("B", "X") => 1 + 0,
        ("C", "X") => 1 + 6,
        ("A", "Y") => 2 + 6,
        ("B", "Y") => 2 + 3,
        ("C", "Y") => 2 + 0,
        ("A", "Z") => 3 + 0,
        ("B", "Z") => 3 + 6,
        ("C", "Z") => 3 + 3,
        _          => todo!(),
    }
}

fn part2(p1: &str, p2: &str) -> usize {
    match (p1, p2) {
        ("A", "X") => 3 + 0,
        ("B", "X") => 1 + 0,
        ("C", "X") => 2 + 0,
        ("A", "Y") => 1 + 3,
        ("B", "Y") => 2 + 3,
        ("C", "Y") => 3 + 3,
        ("A", "Z") => 2 + 6,
        ("B", "Z") => 3 + 6,
        ("C", "Z") => 1 + 6,
        _          => todo!(),
    }
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let lines = stdin
        .lock()
        .lines()
        .collect::<io::Result<Vec<String>>>()?;

    let rounds = lines
        .iter()
        .map(|s| parse_line(s))
        .collect::<Vec<_>>();

    let p1 = rounds
        .iter()
        .map(|(p1, p2)| part1(p1, p2))
        .sum::<usize>();

    let p2 = rounds
        .iter()
        .map(|(p1, p2)| part2(p1, p2))
        .sum::<usize>();

    println!("part 1 {}", p1);
    println!("part 2 {}", p2);

    Ok(())
}
