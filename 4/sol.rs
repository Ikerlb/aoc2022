use std::str::FromStr;
use std::io::{self, BufRead};

#[derive(Debug)]
struct Interval {
    start: i32,
    end: i32,
}

#[derive(Debug)]
struct ParseIntervalError;

impl FromStr for Interval {
    type Err = ParseIntervalError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut it = s.split("-");

        match (it.next().unwrap().parse(), it.next().unwrap().parse()) {
            (Err(_), _) => Err(ParseIntervalError),
            (_, Err(_)) => Err(ParseIntervalError),
            (Ok(start), Ok(end)) => Ok(Interval { start, end }),
        }
    }
}

impl Interval {
    fn is_contained(&self, other: &Interval) -> bool {
        other.start >= self.start && other.end <= self.end
    }

    fn intersects(&self, other: &Interval) -> bool {
        self.start <= other.start && other.start <= self.end
            || self.start <= other.end && other.end <= self.end
    }
}

fn parse_line(s: &str) -> (Interval, Interval) {
    let mut iter = s.split(",");
    let first = iter.next().unwrap().parse().unwrap();
    let second = iter.next().unwrap().parse().unwrap();
    (first, second)
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let lines = stdin
        .lock()
        .lines()
        .collect::<Result<Vec<String>, _>>()?;

    let intervals = lines
        .iter()
        .map(|s| parse_line(&s))
        .collect::<Vec<_>>();

    let p1 = intervals
        .iter()
        .filter(|(i1, i2)| i1.is_contained(i2) || i2.is_contained(i1))
        .count();

    let p2 = intervals
        .iter()
        .filter(|(i1, i2)| i1.intersects(i2) || i2.intersects(i1))
        .count();

    println!("part 1: {}", p1);
    println!("part 2: {}", p2);

    Ok(())
}
