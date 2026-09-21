export class TreeNode {
  constructor(entity, prerequisiteIds = []) {
    this.entity = entity;
    this.prerequisiteIds = prerequisiteIds;
    this.children = [];
  }

  addChild(node) {
    this.children.push(node);
  }
}

export class UnlockTree {
  constructor(rootNode) {
    this.root = rootNode;
  }

  findPathDFS(targetId, node = this.root, path = []) {
    path.push(node);
    if (node.entity.id === targetId) return [...path];
    for (const child of node.children) {
      const result = this.findPathDFS(targetId, child, path);
      if (result) return result;
    }
    path.pop();
    return null;
  }

  getWithinDepth(maxDepth) {
    const result = [];
    const queue = [{ node: this.root, depth: 0 }];
    while (queue.length > 0) {
      const { node, depth } = queue.shift();
      if (depth > maxDepth) continue;
      if (depth > 0) result.push(node);
      for (const child of node.children) {
        queue.push({ node: child, depth: depth + 1 });
      }
    }
    return result;
  }

  flatten(node = this.root, list = []) {
    list.push(node);
    for (const child of node.children) this.flatten(child, list);
    return list;
  }

  tryUnlock(entityId, playerCoins) {
    const target = this.#findNode(entityId);
    if (!target || target.entity.unlocked) {
      return { success: false, reason: "invalid or already unlocked" };
    }
    for (const preId of target.prerequisiteIds) {
      const pre = this.#findNode(preId);
      if (pre && !pre.entity.unlocked) {
        return { success: false, reason: `requires ${pre.entity.name}` };
      }
    }
    if (playerCoins < target.entity.unlockCost) {
      return { success: false, reason: "not enough coins" };
    }
    target.entity.unlocked = true;
    return { success: true, coinsSpent: target.entity.unlockCost };
  }

  #findNode(entityId, node = this.root) {
    if (node.entity.id === entityId) return node;
    for (const child of node.children) {
      const found = this.#findNode(entityId, child);
      if (found) return found;
    }
    return null;
  }
}