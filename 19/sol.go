package main

import (
    "fmt"
    "os"
    "bufio"
    "strings"
	"regexp"
    "strconv"
)

type typeAmount struct {
    Type string
    Amount int
}

var RESOURCES = []string {"ore", "clay", "obsidian", "geode"}

func pos[K comparable](l []K, v K) int {
    for i, e := range l {
        if e == v {
            return i
        }
    }
    return -1
}

func parseLine(input string) []typeAmount {
    l := make([]typeAmount, 0)

	// Define the regular expression pattern.
	pattern := "(\\d+)\\s([a-zA-Z]+)"

	// Compile the regular expression.
	re, err := regexp.Compile(pattern)
	if err != nil {
		return l
	}

	// Find all matches in the input string.
	matches := re.FindAllStringSubmatch(input, -1)
	if matches == nil {
		return l
	}

	for _, match := range matches {
        n, _ := strconv.Atoi(match[1])
        l = append(l, typeAmount{match[2], n})
	}
    return l
}

type vector []int

func add(v1, v2 vector) vector {
    v := make(vector, len(v1))
    for i := 0; i < len(v1); i += 1 {
        v[i] = v1[i] + v2[i]
    }
    return v
}

func subs(v1, v2 vector) vector {
    v := make(vector, len(v1))
    for i := 0; i < len(v1); i += 1 {
        v[i] = v1[i] - v2[i]
    }
    return v
}

func incr(v1 vector, k int) vector {
    v := make(vector, len(v1))
    for i := 0; i < len(v1); i += 1 {
        v[i] = v1[i]
        if i == k {
            v[i] += 1
        }
    }
    return v
}

type state struct {
    robots, resources vector
    minutes int
}

func (st state) String() string {
    return fmt.Sprintf("%v %v %d", st.robots, st.resources, st.minutes)
}

func max(a, b int) int {
    if a > b {
        return a
    }
    return b
}

func Max(l ...int) int {
    m := l[0]
    for _, e := range l {
        m = max(m, e)
    }
    return m
}

func canCreate(bp []int, ress vector) bool {
    for i := 0; i < len(bp); i += 1 {
        if bp[i] > ress[i] {
            return false
        }
    }
    return true
}

func exceeds(v1, v2 vector) bool {
    for i := 0; i < len(v1); i += 1 {
        if v1[i] > v2[i] {
            return true
        }
    }
    return false
}

func dfs(bp [][]int, robs, ress vector, mins int) int {
    res := 0
    s := make([]state, 0)
    s = append(s, state{robs, ress, mins})

    used := make(map[string]bool)
    used[s[0].String()] = true

    mv := make(vector, len(ress))
    for _, robot := range bp {
        for i := 0; i < len(robot); i += 1 {
            mv[i] = max(mv[i], robot[i])
        }
    }

    mv[len(mv) - 1] = 1000000

    for len(s) > 0 {
        st := s[len(s)-1]
        s = s[:len(s)-1]
        if st.minutes <= 0 {
            res = max(res, st.resources[len(st.resources)-1])
            continue
        }

        if exceeds(st.robots, mv) {
            continue
        }

        for i := 0; i < len(ress) - 1; i += 1 {
            if st.resources[i] > (st.minutes * mv[i]) - (st.robots[i] * (st.minutes - 1)) {
                //st.resources[i] = (st.minutes * mv[i]) - (st.robots[i] * (st.minutes - 1))
                continue;
            }
        }

        s = append(s, state{st.robots, add(st.resources, st.robots), st.minutes - 1})
        for b, robot := range bp {
            if canCreate(robot, st.resources) {
                nrobs := incr(st.robots, b)
                nress := add(subs(st.resources, robot), st.robots)
                ns := state{nrobs, nress, st.minutes - 1}
                nss := ns.String()
                if !used[nss] {
                    s = append(s, ns)
                    used[nss] = true
                }
            }
        }
    }
    return res
}

func main() {
    sc := bufio.NewScanner(os.Stdin)
    blueprints := make([][][]int, 0)
    for sc.Scan() {
        l := strings.Split(sc.Text(), " Each ")
        var robot int 
        fmt.Sscanf(l[0], "Blueprint %d:", &robot)
        bp := make([][]int, len(RESOURCES))
        for _, line := range l[1:] {
            ll := strings.Split(line, " robot costs ")
            arr := make([]int, len(RESOURCES))
            for _, ta := range parseLine(ll[1]) {
                arr[pos(RESOURCES, ta.Type)] = ta.Amount
            }
            bp[pos(RESOURCES, ll[0])] = arr
        }
        blueprints = append(blueprints, bp)
    }

    s := 0
    for i := 0; i < len(blueprints); i += 1 {
        robots := []int {1, 0, 0, 0}
        resources := []int {0, 0, 0, 0}
        s += (i + 1) * dfs(blueprints[i], robots, resources, 24)
    }
    fmt.Println(s)

    p := 1
    for i := 0; i < 3; i += 1 {
        robots := []int {1, 0, 0, 0}
        resources := []int {0, 0, 0, 0}
        p *= dfs(blueprints[i], robots, resources, 32)
    }
    fmt.Println(p)
}
