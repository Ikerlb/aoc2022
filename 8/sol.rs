use std::io::{self, BufRead};

// first larger after, depends on iter order
fn calc<I>(iter: I, size: usize) -> Vec<Option<isize>> 
where
    I: Iterator<Item = (usize, usize)>
{
    let mut res = vec![None; size];

    let mut s: Vec<(usize, usize)> = Vec::new();

    for (i, n) in iter {
        while !s.is_empty() && (n >= s.last().unwrap().1) {
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

    let l2r: Vec<Vec<_>> = grid
        .iter()
        .map(|row| calc(
                row.iter().enumerate().map(|(a,b)| (a, *b)),
                n)
        )
        .collect();

    let r2l: Vec<Vec<_>> = grid
        .iter()
        .map(|row| calc(
                row.iter().enumerate().rev().map(|(a,b)| (a, *b)),
                n)
        )
        .collect();

    
    let u2d: Vec<Vec<_>> = transpose((0..m)
        .map(|i| calc(
                (0..n).map(|j| (j, grid[j][i])),
                m)
        )
        .collect());

    let d2u: Vec<Vec<_>> = transpose((0..m)
        .map(|i| calc(
                (0..n).map(|j| (j, grid[j][i])).rev(),
                m)
        )
        .collect());

    let p1: usize = (0..n)
        .map(|i| (0..m)
             .map(|j| {
                (l2r[i][j].is_none() ||
                 r2l[i][j].is_none() || 
                 u2d[i][j].is_none() ||
                 d2u[i][j].is_none()) as usize
             })
             .sum::<usize>()
        )
        .sum();

    let p2 = (0..n)
        .map(|row| (0..m)
             .map(|col| {
                let l2ri = l2r[row][col].unwrap_or((n - 1) as isize);
                let r2li = r2l[row][col].unwrap_or(0);
                let u2di = u2d[row][col].unwrap_or((m - 1) as isize);
                let d2ui = d2u[row][col].unwrap_or(0);
                let l = l2ri - (col as isize);
                let r = (col as isize) - r2li;
                let u = u2di - (row as isize);
                let d = (row as isize) - d2ui;
                l * r * u * d
            })
            .max()
            .unwrap()
        )
        .max()
        .unwrap();

    println!("part 1: {}", p1);
    println!("part 2: {}", p2);

    Ok(())
}
