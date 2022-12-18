package main

import (
    "fmt"
    "os"
    "bufio"
    "sort"
)

type Coord struct {
    row, col int
}

type RowInterval struct {
    row int
    interval Coord
}

func manhattan(a, b Coord) int {
    return abs(a.row - b.row) + abs(a.col - b.col)
}

func abs(x int) int {
    if x < 0 {
        return -x
    }
    return x
}

func max(a, b int) int {
    if a > b {
        return a
    }
    return b
}

func createIntervals(sp, bp Coord) []RowInterval {
    res := make([]RowInterval, 0)
    d := manhattan(sp, bp)

    res = append(res, RowInterval{sp.row, Coord{sp.col - d, sp.col + d}})

    for dr := 1; dr <= d; dr++ {
        res = append(res, RowInterval{sp.row + dr, Coord{sp.col - d + dr, sp.col + d - dr + 1}})
        res = append(res, RowInterval{sp.row - dr, Coord{sp.col - d + dr, sp.col + d - dr + 1}})
    }

    return res
}

// merge intervals
func mergeIntervals(intervals []Coord) []Coord {
    sort.Slice(intervals, func(i, j int) bool {
        return intervals[i].row < intervals[j].row ||
            (intervals[i].row == intervals[j].row && intervals[i].col < intervals[j].col)
    })
    merged := make([]Coord, 0)
    for _, interval := range intervals {
        if len(merged) == 0 || merged[len(merged)-1].col < interval.row {
            merged = append(merged, interval)
        } else {
            merged[len(merged)-1] = Coord{merged[len(merged)-1].row, max(merged[len(merged)-1].col, interval.col)}
        }
    }
    return merged
}

func beaconsInRowRange(beacons map[Coord]bool, row, c1, c2 int) int {
    res := 0
    for b := range beacons {
        if b.row == row && c1 <= b.col && b.col < c2 {
            res++
        }
    }
    return res
}

func part1(rows map[int][]Coord, beacons map[Coord]bool, row int) int {
    res := 0
    for _, intervals := range rows[row] {
        res += intervals.col - intervals.row - beaconsInRowRange(beacons, row, intervals.row, intervals.col)
    }
    return res
}

func part2(rows map[int][]Coord, lo, hi int) int {
    for r := lo; r <= hi; r++ {
        if intervals, ok := rows[r]; ok {
            prev := intervals[0]
            for _, interval := range intervals[1:] {
                if interval.row - prev.col == 1 && lo <= interval.row - 1 && interval.row - 1 <= hi {
                    return (interval.row - 1) * hi + r
                }
            }
        }
    }
    return 0
}

func main() {
    scr := bufio.NewScanner(os.Stdin)
    beacons := make(map[Coord]bool)
    rows := make(map[int][]Coord)
    
    format := "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d"

    for scr.Scan() {
        sc := Coord{0, 0}
        bc := Coord{0, 0}
        fmt.Sscanf(scr.Text(), format, &sc.col, &sc.row, &bc.col, &bc.row)

        beacons[bc] = true
        for _, ri := range createIntervals(sc, bc) {
            rows[ri.row] = append(rows[ri.row], ri.interval)
        }
    }

    for k, intervals := range rows {
        rows[k] = mergeIntervals(intervals)
    }

    fmt.Println(part1(rows, beacons, 2000000))
    fmt.Println(part2(rows, 0, 4000000))
}
