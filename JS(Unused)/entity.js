export class Entity {
  constructor(id, name, icon, unlockCost = 0) {
    this.id = id;
    this.name = name;
    this.icon = icon;
    this.unlockCost = unlockCost;
    this.unlocked = unlockCost === 0;
  }
}

export class Plant extends Entity {
  constructor(id, name, icon, unlockCost, growTimeSeconds) {
    super(id, name, icon, unlockCost);
    this.growTimeSeconds = growTimeSeconds;
  }
}

export class Fish extends Entity {
  constructor(id, name, icon, unlockCost, growTimeSeconds) {
    super(id, name, icon, unlockCost);
    this.growTimeSeconds = growTimeSeconds;
  }
}

export class LivestockAnimal extends Entity {
  constructor(id, name, icon, unlockCost, produceIntervalSeconds) {
    super(id, name, icon, unlockCost);
    this.produceIntervalSeconds = produceIntervalSeconds;
  }
}

export class Product extends Entity {
  constructor(id, name, icon) {
    super(id, name, icon, 0);
  }
}