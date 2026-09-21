export class Stack {
  #items = [];

  push(item) {
    this.#items.push(item);
  }

  pop() {
    return this.#items.pop();
  }

  peek() {
    return this.#items[this.#items.length - 1];
  }

  get isEmpty() {
    return this.#items.length === 0;
  }

  get size() {
    return this.#items.length;
  }

  toArray() {
    return [...this.#items];
  }
}