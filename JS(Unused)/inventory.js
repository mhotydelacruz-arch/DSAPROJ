export class Inventory {
  constructor(capacity) {
    this.capacity = capacity;
    this.slots = new Array(capacity).fill(null);
  }

  addItem(item) {
    const freeIndex = this.slots.indexOf(null);
    if (freeIndex === -1) return false;
    this.slots[freeIndex] = item;
    return true;
  }

  removeAt(index) {
    if (index < 0 || index >= this.capacity) return null;
    const item = this.slots[index];
    this.slots[index] = null;
    return item;
  }

  get isFull() {
    return !this.slots.includes(null);
  }

  get count() {
    return this.slots.filter((s) => s !== null).length;
  }
}