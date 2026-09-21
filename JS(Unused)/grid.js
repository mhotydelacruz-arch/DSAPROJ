export class AreaGrid {
  constructor(areaName, rows, cols) {
    this.areaName = areaName;
    this.rows = rows;
    this.cols = cols;
    this.grid = Array.from({ length: rows }, () => Array(cols).fill(null));
  }

  place(entity, row, col) {
    if (row < 0 || row >= this.rows || col < 0 || col >= this.cols) return false;
    if (this.grid[row][col] !== null) return false;
    this.grid[row][col] = entity;
    return true;
  }

  remove(row, col) {
    if (row < 0 || row >= this.rows || col < 0 || col >= this.cols) return null;
    const entity = this.grid[row][col];
    this.grid[row][col] = null;
    return entity;
  }

  get(row, col) {
    if (row < 0 || row >= this.rows || col < 0 || col >= this.cols) return null;
    return this.grid[row][col];
  }
}

export const areaGrids = {
  garden: new AreaGrid("garden", 6, 6),
  fishpond: new AreaGrid("fishpond", 5, 5),
  livestock: new AreaGrid("livestock", 5, 6),
};