use std::io::{self, BufRead};

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let handle = stdin.lock();


    let mut groups: Vec<_> = Vec::new();
    let mut group_sum = 0;
    for line_r in handle.lines() {
        let line = line_r.unwrap();
        if line != "" {
            let n = line.parse::<usize>().unwrap();
            group_sum += n;
        } else {
            groups.push(group_sum);
            group_sum = 0;
        }
    }

    groups.push(group_sum);

    groups.sort();

    println!("{}", groups.last().unwrap());
    println!("{}", groups.iter().rev().take(3).fold(0, |x, y| x + y));

    Ok(())
}
