use std::io::{self, BufRead};

fn first_non_repeating_window(s: &str, size: usize) -> Option<usize>{
    let chars = s
        .chars()
        .collect::<Vec<_>>();

    let mut counts = [0; 26];
    for c in &chars[..size] {
        let i = (*c as u8 - b'a') as usize;
        counts[i] += 1;
    }
    let mut uniq = counts.iter().filter(|&&c| c == 1).count();

    if uniq == size {
        return Some(size);
    }

    for (i, c) in chars.iter().enumerate().skip(size) {
        let ic = (*c as u8 - b'a') as usize;
        counts[ic] += 1;
        if counts[ic] == 1 {
            uniq += 1;
        } else if counts[ic] == 2 {
            uniq -= 1;
        }

        let jc = (chars[i - size] as u8 - b'a') as usize;
        counts[jc] -= 1;
        if counts[jc] == 1 {
            uniq += 1;
        } else if counts[jc] == 0 {
            uniq -= 1;
        }

        if uniq == size {
            return Some(i + 1);
        }
    }
    return None;
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let line = stdin
        .lock()
        .lines()
        .next()
        .unwrap()
        .unwrap();

    let p1 = first_non_repeating_window(&line, 4).unwrap();
    let p2 = first_non_repeating_window(&line, 14).unwrap();

    println!("part 1: {}", p1);
    println!("part 2: {}", p2);

    Ok(())
}

