use std::io::{self, BufRead};
// import necessaries for implementing display

fn format(option: Option<usize>) -> String {
    if option.is_none() {
        return "_".to_string();
    } else {
        return option.unwrap().to_string();
    }
}

// first larger after, depends on iter order
fn calc<I, F>(iter: I, f: F, size: usize) -> Vec<Option<isize>> 
where
    I: Iterator<Item = (usize, usize)>,
    F: Fn(usize, usize) -> bool,
{
    let mut res = vec![None; size];

    let mut s: Vec<(usize, usize)> = Vec::new();

    for (i, n) in iter {
        while !s.is_empty() && f(n, s.last().unwrap().1) {
            let j = s.pop().unwrap().0;
            res[j] = Some(i as isize);
        }
        s.push((i, n));
    }
    res
}

fn transpose<T: std::clone::Clone>(a: Vec<Vec<T>>) -> Vec<Vec<T>> {
    let mut res = vec![vec![]; a[0].len()];
    for i in 0..a.len() {
        for j in 0..a[i].len() {
            res[j].push(a[i][j].clone());
        }
    }
    res
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();

    let lines = stdin
        .lock()
        .lines()
        .collect::<io::Result<Vec<String>>>()?;

    let grid: Vec<Vec<usize>> = lines
        .iter()
        .map(|line|
             line
                .chars()
                .map(|c| c.to_digit(10).unwrap() as usize)
                .collect())
        .collect();

    
    let n = grid.len();
    let m = grid[0].len();

    // l2r basically means, first larger after
    let l2r: Vec<Vec<_>> = grid
        .iter()
        .map(|row| calc(
                row.iter().enumerate().map(|(a,b)| (a, *b)),
                |a, b| a>=b,
                n)
        )
        .collect();

    // r2l basically means, first larger before
    let r2l: Vec<Vec<_>> = grid
        .iter()
        .map(|row| calc(
                row.iter().enumerate().rev().map(|(a,b)| (a, *b)),
                |a, b| a>=b,
                n)
        )
        .collect();

    
    // u2d basically means, first larger after
    let u2d: Vec<Vec<_>> = transpose((0..m)
        .map(|i| calc(
                (0..n).map(|j| (j, grid[j][i])),
                |a, b| a >= b,
                m)
        )
        .collect());

    // d2u basically means, first larger before
    let d2u: Vec<Vec<_>> = transpose((0..m)
        .map(|i| calc(
                (0..n).map(|j| (j, grid[j][i])).rev(),
                |a, b| a >= b,
                m)
        )
        .collect());

    let p1 = (0..n)
        .map(|i| (0..m)
             .map(|j| {

             })
             .sum()
        .sum()
        .unwrap();

    /*println!("{:?}\n", l2r);
    println!("{:?}\n", r2l);
    println!("{:?}\n", u2d);
    println!("{:?}\n", d2u);*/

    /*let res = (0..n)
        .map(|r| (0..m)
             .map(|c| {
                *let left = c - (r2l[r][c] as isize);
                let right = (l2r[r][c] as isize) - ();
                let up = r - (d2u[r][c] as isize);
                let down = (u2d[r][c] as isize) - r;
                println!("({}, {}) l: {} r: {} u: {} d: {}", r, c, left, right, up, down);
                right * left * up * down
             })
             .max()
             .unwrap())
        .max()
        .unwrap();*/

    grid
        .iter()
        .for_each(|row| println!("{:?}", row));

    Ok(())
}
