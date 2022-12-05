package main

import (
    "fmt"
    "os"
    "bufio"
    "strconv"
    "sort"
    "golang.org/x/exp/constraints"
)

func Sum[T constraints.Integer](slice []T) {
    s := 0
    for i := 0; i < len(slice); i += 1 {
        s += slice[i]
    }
    return s;
}

func main() {
    sc := bufio.NewScanner(os.Stdin)

    g := 0
    groups := make([]int, 0)

    for sc.Scan() {
        line = sc.Text();
        if line == "" {
            groups = append(groups, g)
            g = 0
        } else {
            n, _ := strconv.Atoi(line)
            g += n
        }
    }
    groups = append(groups, g)
    
    sort.Ints(groups)

    fmt.Println("%s", groups[len(groups) - 1])
    fmt.Println("%s", Sum(groups[len(groups) - 3:])]))
}
