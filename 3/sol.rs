// everytime i write
// debug as a comment
// the next line will be
// println!("{:?}", )

use std::io::{self, BufRead};
use std::collections::HashSet;

// Lowercase item types a through z have priorities 1 through 26.
// Uppercase item types A through Z have priorities 27 through 52.
fn priority(c: char) -> usize {
    match c {
        'a'..='z' => c as usize - 'a' as usize + 1,
        'A'..='Z' => c as usize - 'A' as usize + 27,
        _ => panic!("invalid"),
    }
}

fn part1(s: &str) -> usize {
    let (h1, h2) = s.split_at(s.len() >> 1);
    let hs1 = h1.chars().collect::<HashSet<_>>();
    let hs2 = h2.chars().collect::<HashSet<_>>();
    hs1.intersection(&hs2).map(|c| priority(*c)).sum()
}

fn part2<T: AsRef<str>>(group: &[T]) -> usize {
    let hss = group
        .iter()
        .map(|s| s.as_ref().chars().collect::<HashSet<_>>());
    let tmp = hss
        .reduce(|hs1, hs2| hs1.intersection(&hs2).cloned().collect())
        .unwrap();
    let c = tmp
        .iter()
        .next()
        .unwrap();

    priority(*c)
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let rucksacks = stdin
        .lock()
        .lines()
        .collect::<io::Result<Vec<_>>>()?;

    let p1 = rucksacks
        .iter()
        .map(|s| part1(&s))
        .sum::<usize>();

    let p2 = rucksacks
        .chunks(3)
        .map(|s| part2(s))
        .sum::<usize>();

    println!("part 1: {}", p1);
    println!("part 2: {}", p2);

    Ok(())
}
