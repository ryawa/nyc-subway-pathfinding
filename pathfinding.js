import mnemonist from "https://cdn.jsdelivr.net/npm/mnemonist@0.39.8/+esm";

function heuristic(x, y) {
  const r = 6371;
  const p = Math.PI / 180;
  const a =
    0.5 -
    Math.cos((y[0] - x[0]) * p) / 2 +
    (Math.cos(x[0] * p) *
      Math.cos(y[0] * p) *
      (1 - Math.cos((y[1] - x[1]) * p))) /
      2;

  const dist = 2 * r * Math.asin(Math.sqrt(a));
  return dist / 8; // 8 m/s avg speed
}

function aStar(graph, start, goal) {
  const openSet = new mnemonist.FibonacciHeap((a, b) => {
    if (a[1] < b[1]) return -1;
    if (a[1] > b[1]) return 1;
    return 0;
  });
  openSet.push([start, 0]);
  const prev = {};
  const costTo = {};
  costTo[start] = 0;
  while (openSet.size > 0) {
    let [current, _] = openSet.pop();
    if (current === goal) {
      const path = [];
      while (current in prev) {
        path.push(current);
        current = prev[current];
      }
      path.push(start);
      return [path.reverse(), costTo[goal]];
    }
    for (const [neighbor, cost] of Object.entries(graph[current])) {
      if (neighbor === "coords") {
        continue;
      }
      const newCost = costTo[current] + graph[current][neighbor];
      if (!(neighbor in costTo) || newCost < cost[neighbor]) {
        costTo[neighbor] = newCost;
        prev[neighbor] = current;
        openSet.push([
          neighbor,
          newCost + heuristic(graph[goal].coords, graph[neighbor].coords),
        ]);
      }
    }
  }
}

export default aStar;
