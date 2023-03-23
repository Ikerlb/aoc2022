use std::io::{self, BufRead};
use std::str::FromStr;
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
struct Node {
    name: String,
    children: Vec<Rc<RefCell<Node>>>,
    is_file: bool,
    size: Option<usize>,
}

struct NodeIter {
    stack: Vec<Rc<RefCell<Node>>>,
}

impl Iterator for NodeIter {
    type Item = Rc<RefCell<Node>>;

    fn next(&mut self) -> Option<Self::Item> {
        if let Some(node) = self.stack.pop() {
            self.stack.extend(node.borrow().children.iter().rev().cloned());
            Some(node)
        } else {
            None
        }
    }
}

#[derive(Debug)]
enum FileResult {
    File(String, usize),
    Dir(String),
}

fn build_tree(commands: &Vec<Command>) -> Rc<RefCell<Node>> {
    let mut root = Rc::new(RefCell::new(Node {
        name: String::from("/"),
        children: Vec::new(),
        is_file: false,
        size: None,
    }));

    commands
        .iter()
        .fold(vec![root.clone()], |mut stack, command| {
            match command {
                Command::Cd{path: path} if path == "/" => (),
                Command::Cd{path: path} if path == ".." => {
                    stack.pop();
                },
                Command::Cd{path: path} => {
                     let tmp= stack
                        .last()
                        .unwrap()
                        .borrow();
                    let child = tmp
                        .children
                        .iter()
                        .find(|node| node.borrow().name == *path)
                        .unwrap()
                        .clone();
                    drop(tmp);
                    stack.push(child);
                },
                Command::Ls { result: v } => {
                    let children = v
                        .iter()
                        .map(|result| {
                            match result {
                                FileResult::File(name, size) => Rc::new(RefCell::new(Node {
                                    name: name.clone(),
                                    children: Vec::new(),
                                    is_file: true,
                                    size: Some(*size),
                                })),
                                FileResult::Dir(name) => Rc::new(RefCell::new(Node {
                                    name: name.clone(),
                                    children: Vec::new(),
                                    is_file: false,
                                    size: None,
                                })),
                            }
                        })
                        .collect();
                    stack
                        .iter_mut()
                        .last()
                        .unwrap()
                        .borrow_mut()
                        .children = children;
                },
            }
            stack
        });
    root
}

impl FromStr for FileResult {
    type Err = io::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut parts = s.split_whitespace();

        let first = parts.next().ok_or(io::Error::new(
            io::ErrorKind::InvalidData,
            "No first part",
        ))?;

        let second = parts.next().ok_or(io::Error::new(
            io::ErrorKind::InvalidData,
            "No second part",
        ))?;

        if first == "dir" {
            Ok(FileResult::Dir(second.to_string()))
        } else {
            let size = first.parse::<usize>().unwrap();
            Ok(FileResult::File(second.to_string(), size))
        }

    }
}

#[derive(Debug)]
enum Command {
    Cd { path: String },
    Ls { result: Vec<FileResult> },
}

fn parse_commands(lines_vec: &Vec<String>) -> Vec<Command> {
    let mut commands = Vec::new();
    let mut lines = lines_vec.iter().peekable();

    while let Some(line) = lines.next().clone() {
        let mut parts = line.split_whitespace();

        parts.next(); // burn '$'
        let comm = match (parts.next(), parts.next()) {
            (Some("cd"), Some(path)) => Command::Cd {
                path: path.to_string()
            },
            (Some("ls"), None) => {
                let mut results = Vec::new();
                while let Some(ls_res) = lines.peek() {
                    if ls_res.starts_with("$") {
                        break;
                    }
                    results.push(ls_res.parse::<FileResult>().unwrap());
                    lines.next();
                }
                Command::Ls {
                    result: results
                }
            },
            _ => todo!("invalid command {}", line),
        };
        commands.push(comm);
    }
    commands
}

fn dfs(root: &mut Rc<RefCell<Node>>) -> usize {
    if root.borrow().is_file {
        return root.borrow().size.unwrap();
    } else {
        let mut size = 0;
        for child in root.borrow_mut().children.iter_mut() {
            size += dfs(child);
        }
        root.borrow_mut().size = Some(size);
        size
    }
}

fn new_iter(root: Rc<RefCell<Node>>) -> NodeIter {
    NodeIter {
        stack: vec![root],
    }
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let lines = stdin
        .lock()
        .lines()
        .collect::<io::Result<Vec<String>>>()?;

    let commands = parse_commands(&lines);
    let mut root = build_tree(&commands);

    dfs(&mut root);

    let treshold = 100000;
    let p1 = new_iter(root.clone()) 
        .filter(|node| !node.borrow().is_file && node.borrow().size.unwrap() <= treshold)
        .map(|node| node.borrow().size.unwrap())
        .sum::<usize>();

    let total = 70000000;
    let unused = total - root.borrow().size.unwrap();
    let needed = 30000000;

    let p2 = new_iter(root.clone())
        .filter(|node| !node.borrow().is_file && unused + node.borrow().size.unwrap() > needed)
        .min_by_key(|node| node.borrow().size.unwrap())
        .unwrap()
        .borrow()
        .size
        .unwrap();

    println!("part 1: {}", p1);
    println!("part 2: {}", p2);

    Ok(())
}
