// cargo-deps: regex="1.4"
extern crate regex;

use regex::Regex;
use std::io;
use std::io::BufRead;
use std::collections::HashMap;
use std::fmt;

#[derive(Copy, Clone)]
struct Point {
    r: isize,
    c: isize,
}

struct Interval {
    start: isize,
    end: isize,
}

struct RowInterval {
    row: isize,
    interval: Interval,
}

impl fmt::Display for Interval {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.start, self.end)
    }
}

fn manhattan_distance(p1: Point, p2: Point) -> isize {
    (p1.r - p2.r).abs() + (p1.c - p2.c).abs()
}

fn generate_intervals(sp: Point, bp: Point) -> Vec<RowInterval> {
    let mut intervals = Vec::new();
    let d = manhattan_distance(sp, bp);
    intervals.push(RowInterval {
        row: sp.r,
        interval: Interval {
            start: sp.c - d,
            end: sp.c + d,
        },
    });

    for dr in 1..d {
        intervals.push(RowInterval {
            row: sp.r + dr,
            interval: Interval {
                start: sp.c - d + dr,
                end: sp.c + d - dr + 1,
            },
        });
        intervals.push(RowInterval {
            row: sp.r - dr,
            interval: Interval {
                start: sp.c - d + dr,
                end: sp.c + d - dr + 1,
            },
        });
    }

    intervals
}

fn parse_line(line: &str) -> Result<(Point, Point), &'static str> {
    let re = Regex::new(r"x=(-?\d+), y=(-?\d+)").unwrap();
    let mut points = Vec::new();
    for cap in re.captures_iter(line) {
        let x: isize = cap[1].parse().unwrap();
        let y: isize = cap[2].parse().unwrap();
        points.push(Point { r: y, c: x });
    }
    if points.len() != 2 {
        return Err("Invalid input format");
    }
    Ok((points[0], points[1]))
}

fn merge_intervals(intervals: &mut Vec<Interval>) {
    intervals.sort_by(|a, b| a.start.cmp(&b.start));
    let mut i = 0;
    while i < intervals.len() - 1 {
        if intervals[i].end >= intervals[i + 1].start {
            intervals[i].end = intervals[i].end.max(intervals[i + 1].end);
            intervals.remove(i + 1);
        } else {
            i += 1;
        }
    }
}

fn beacons_in_row_interval(beacons: &Vec<Point>, row: isize, inter: &Interval) -> isize {
    let mut count: isize = 0;
    for beacon in beacons {
        if beacon.r == row && beacon.c >= inter.start && beacon.c <= inter.end {
            count += 1;
        }
    }
    count
}

fn part1(rows: &HashMap<isize, Vec<Interval>>, row: isize, beacons: Vec<Point>) -> isize {
    let mut count: isize = 0;
    let intervals = rows.get(&row).unwrap();
    for interval in intervals {
        count += interval.end - interval.start;
        count -= beacons_in_row_interval(&beacons, row, interval);
    }
    count
}

fn in_range(x: isize, lo: isize, hi: isize) -> bool {
    x >= lo && x <= hi
}

fn part2(rows: &HashMap<isize, Vec<Interval>>, lo: isize, hi: isize) -> isize {
    for ri in lo..hi {
        if rows.contains_key(&ri) {
            let row = rows.get(&ri).unwrap();
            let mut prev = &row[0];
            for i in 1..row.len() {
                let curr = &row[i];
                if curr.start - prev.end == 1 && in_range(curr.start - 1, lo, hi) {
                    return (curr.start - 1) * hi + ri;
                }
                prev = &curr;
            }
        }
    }
    return 0
}

fn main() {
    let stdin = io::stdin();

    let mut rows: HashMap<isize, Vec<Interval>> = HashMap::new();
    let mut beacons = Vec::new();


    for line in stdin.lock().lines() {
        let line = line.unwrap();

        let (sp, gp) = parse_line(&line).unwrap();
        beacons.push(gp);

        for ri in generate_intervals(sp, gp) {
            if rows.contains_key(&ri.row) {
                rows.get_mut(&ri.row).unwrap().push(ri.interval);
            } else {
                rows.insert(ri.row, vec![ri.interval]);
            }
        }

    }

    for (k, v) in rows.iter_mut() {
        merge_intervals(v);
    }

    println!("{}", part1(&rows, 20, beacons));
    println!("{}", part2(&rows, 0, 4000000));
}
