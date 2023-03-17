// cargo-deps: regex="1"
extern crate regex;

use std::io::{self, BufRead};
use regex::Regex;

fn parse_crates(crates: &[String]) -> Vec<Vec<char>>{
    let mut v = crates
        .iter()
        .rev();

    let indices = v
        .next()
        .unwrap()
        .chars()
        .enumerate()
        .filter(|(_, c)| c.is_digit(10))
        .map(|(i, c)| (i, (c as usize) - ('0' as usize) - 1))
        .collect::<Vec<_>>();

    let mut stacks = vec![vec![]; indices.len()];
    for line in v {
        let lv = line.chars().collect::<Vec<_>>(); 
        for (i, s) in &indices {
            if !lv[*i].is_whitespace() {
                stacks[*s].push(lv[*i]);
            }
        }
    }
    stacks
 }

fn parse_move(s: &str) -> (usize, usize, usize) {
    let res = "move ([0-9]+) from ([0-9]+) to ([0-9]+)";
    let re = Regex::new(res).unwrap();
    let caps = re.captures(s).unwrap();

    let n = caps.get(1).unwrap().as_str().parse::<usize>().unwrap();
    let f = caps.get(2).unwrap().as_str().parse::<usize>().unwrap();
    let t = caps.get(3).unwrap().as_str().parse::<usize>().unwrap();

    (n, f - 1, t - 1)
}

fn part1(mut stacks: Vec<Vec<char>>, n: usize, f: usize, t: usize) -> Vec<Vec<char>> {
    let size = stacks[f].len();
    let mut v = stacks[f]
        .drain((size - n)..)
        .collect::<Vec<_>>();
    v.reverse();
    stacks[t].append(&mut v);
    stacks
}

fn part2(mut stacks: Vec<Vec<char>>, n: usize, f: usize, t: usize) -> Vec<Vec<char>> {
    let size = stacks[f].len();
    let mut v = stacks[f]
        .drain((size - n)..)
        .collect::<Vec<_>>();
    stacks[t].append(&mut v);
    stacks
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let lines = stdin
        .lock()
        .lines()
        .collect::<io::Result<Vec<_>>>()?;

    let mut iter = lines.split(|line| line.is_empty());
    let crates_text = iter.next().unwrap();
    let moves_text = iter.next().unwrap();

    let mut stacks = parse_crates(&crates_text[..]);
    let moves = moves_text
        .iter()
        .map(|s| parse_move(s))
        .collect::<Vec<_>>();

    let p1v = moves
        .iter()
        .fold(stacks.clone(), |ss, &(n, f, t)| part1(ss, n, f, t));
    let p1 = p1v
        .iter()
        .map(|v| v.last().unwrap())
        .collect::<String>();

    let p2v = moves
        .iter()
        .fold(stacks.clone(), |ss, &(n, f, t)| part2(ss, n, f, t));
    let p2 = p2v
        .iter()
        .map(|v| v.last().unwrap())
        .collect::<String>();

    println!("part 1: {}", p1);
    println!("part 2: {}", p2);

    Ok(())
}
