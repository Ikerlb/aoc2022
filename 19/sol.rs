// cargo-deps: regex="0.1.8", ndarray="0.15.6"
extern crate regex;
extern crate ndarray;
use std::collections::HashSet;
use regex::Regex;
use std::str::FromStr;
use ndarray::{Array, Ix1};
use std::rc::Rc;

#[derive(Debug)]
struct ResourceAmount {
    resource: String,
    amount: usize,
}

impl FromStr for ResourceAmount {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut iter_s = s.split_whitespace();
        let amount = iter_s.next().unwrap().parse::<usize>().unwrap();
        let resource = iter_s.next().unwrap().to_string();
        Ok(ResourceAmount{
            resource,
            amount
        })
    }
}

// create an alias from Array<usize, Ix1>
type Arr = Array<usize, Ix1>;

fn parse_input(order: &Vec<String>, line: &str) -> Vec<Arr> {
    let mut result = Vec::new();

    let mut s_iter = line.split(":");
    let blueprint = s_iter.next().unwrap().to_string();
    let rest = s_iter.next().unwrap().to_string();

    for robot_s in rest.split(" Each ") {
        if robot_s == "" {
            continue;
        }
        let mut robot_v = vec![0; order.len()];
        let robot = robot_s.get(0..robot_s.len()-1).unwrap().to_string();
        let mut robot_iter = robot.split(" robot costs ");
        let robot_name = robot_iter.next().unwrap().to_string();
        let costs = robot_iter
            .next()
            .unwrap()
            .split(" and ")
            .map(|s| ResourceAmount::from_str(s).unwrap())
            .for_each(|ra| robot_v[order.iter().position(|r| r == &ra.resource).unwrap()] = ra.amount);

        result.push(Array::from(robot_v));
    }
    result
}

#[derive(PartialEq, Eq, Hash, Clone)]
struct State {
    resources: Arr,
    robots: Arr,
    mins: usize,
}

// create display for State
// that simply prints the default display
// for resources and robots and mins
impl std::fmt::Debug for State {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "(res: {}, robs: {}, mins: {})", self.resources, self.robots, self.mins)
    }
}

fn max(a: usize, b: usize) -> usize {
    if a > b {
        a
    } else {
        b
    }
}

fn incr(a: &Arr, k: usize) -> Arr {
    let mut nv = a.clone();
    for (i, v) in nv.iter_mut().enumerate() {
        if i == k {
            *v += 1;
        }
    }
    return nv
}


fn dfs(blueprint: Vec<Arr>, robs: Arr, ress: Arr, mins: usize) -> usize {
    let mut mv = Array::from(vec![0; robs.len()]);
    for i in 0..ress.len() {
        mv[i] = (0..blueprint.len())
            .map(|j| blueprint[j][i])
            .max()
            .unwrap();
    }

    let n = mv.len();
    mv[n - 1] = 10000000;

    println!("{}", mv);

    let mut used = HashSet::new();
    let mut s =  Vec::new();
    let ss = Rc::new(State{
        resources: ress,
        robots: robs,
        mins
    });
    used.insert(ss.clone());
    s.push(ss.clone());
    let mut res = 0;
    while s.len() > 0 {
        let mut st = s.pop().unwrap();
        if st.mins <= 0 {
            res = max(res, st.resources[st.resources.len() - 1]);
            continue;
        }

        if mv.iter().zip(st.robots.iter()).any(|(a, b)| a < b) {
            continue;
        }

        for i in 0..(n - 1) {
            if st.resources[i] > ((st.mins * mv[i]) - (st.robots[i] * (st.mins - 1))) {
                continue;
            }
        }

        let ns1 = Rc::new(State{
            resources: st.resources.clone() + &st.robots,
            robots: st.robots.clone(),
            mins: st.mins - 1,
        });

        if !used.contains(&ns1) {
            used.insert(ns1.clone());
            s.push(ns1.clone());
        }

        for (r, robot) in blueprint.iter().enumerate() {
            if robot.iter().zip(st.resources.iter()).all(|(bp, rs)| bp <= rs) {
                let ns2 = Rc::new(State{
                    resources: (st.resources.clone() - robot) + &st.robots,
                    robots: incr(&st.robots, r), 
                    mins: st.mins - 1,
                });

                if used.contains(&ns2) {
                    continue;
                }

                used.insert(ns2.clone());
                s.push(ns2.clone());
            }
        }
    }
    res
}

fn main() {
    let input = "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.";
    let order = vec!["ore".to_string(), "clay".to_string(), "obsidian".to_string(), "geode".to_string()];

    let blueprint = parse_input(&order, input);
    let mut zv = vec![0; order.len()];
    let resources = Array::from(zv.clone());
    zv[0] = 1;
    let mut robots = Array::from(zv);
    println!("{}", dfs(blueprint, robots, resources, 24));
}
