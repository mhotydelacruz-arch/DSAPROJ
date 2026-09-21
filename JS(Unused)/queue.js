export class Queue {
  #items = {};
  #head = 0;
  #tail = 0;

  enqueue(item) {
    this.#items[this.#tail] = item;
    this.#tail++;
  }

  dequeue() {
    if (this.isEmpty) return undefined;
    const item = this.#items[this.#head];
    delete this.#items[this.#head];
    this.#head++;
    return item;
  }

  get front() {
    return this.isEmpty ? undefined : this.#items[this.#head];
  }

  get isEmpty() {
    return this.#head === this.#tail;
  }

  get size() {
    return this.#tail - this.#head;
  }

  toArray() {
    const arr = [];
    for (let i = this.#head; i < this.#tail; i++) arr.push(this.#items[i]);
    return arr;
  }
}

export class Deque {
  #items = {};
  #head = 0;
  #tail = 0;

  enqueue(item) {
    this.#items[this.#tail] = item;
    this.#tail++;
  }

  addFront(item) {
    this.#head--;
    this.#items[this.#head] = item;
  }

  dequeue() {
    if (this.isEmpty) return undefined;
    const item = this.#items[this.#head];
    delete this.#items[this.#head];
    this.#head++;
    return item;
  }

  get front() {
    return this.isEmpty ? undefined : this.#items[this.#head];
  }

  get isEmpty() {
    return this.#head === this.#tail;
  }

  get size() {
    return this.#tail - this.#head;
  }

  toArray() {
    const arr = [];
    for (let i = this.#head; i < this.#tail; i++) arr.push(this.#items[i]);
    return arr;
  }
}