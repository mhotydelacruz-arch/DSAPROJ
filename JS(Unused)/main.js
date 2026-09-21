import { initNav } from "./nav.js";
import { Stack } from "./stack.js";
import { Deque } from "./queue.js";
import { areaGrids } from "./grid.js";
import { Inventory } from "./inventory.js";
import { TreeNode, UnlockTree } from "./tree.js";
import { Plant, Fish, LivestockAnimal, Product } from "./entity.js";

let currentArea = "garden";
let playerCoins = 100;
let selectedCell = null;

const actionHistory = new Stack();
const productionQueue = new Deque();
const inventory = new Inventory(8);

// Garden
const carrot = new Plant("carrot", "Carrot", "carrot", 0, 20);
const tomato = new Plant("tomato", "Tomato", "apple", 50, 30);
const pumpkin = new Plant("pumpkin", "Pumpkin", "circle", 150, 60);
const wheat = new Plant("wheat", "Wheat", "wheat", 80, 25);

const carrotNode = new TreeNode(carrot);
const tomatoNode = new TreeNode(tomato, ["carrot"]);
const pumpkinNode = new TreeNode(pumpkin, ["tomato"]);
const wheatNode = new TreeNode(wheat, ["carrot"]);
carrotNode.addChild(tomatoNode);
carrotNode.addChild(wheatNode);
tomatoNode.addChild(pumpkinNode);
const gardenTree = new UnlockTree(carrotNode);

// Fish Pond
const tilapia = new Fish("tilapia", "Tilapia", "fish", 0, 40);
const salmon = new Fish("salmon", "Salmon", "fish", 100, 90);
const tuna = new Fish("tuna", "Tuna", "fish", 250, 120);

const tilapiaNode = new TreeNode(tilapia);
const salmonNode = new TreeNode(salmon, ["tilapia"]);
const tunaNode = new TreeNode(tuna, ["salmon"]);
tilapiaNode.addChild(salmonNode);
salmonNode.addChild(tunaNode);
const fishTree = new UnlockTree(tilapiaNode);

// Livestock
const chicken = new LivestockAnimal("chicken", "Chicken", "egg", 0, 30);
const cow = new LivestockAnimal("cow", "Cow", "beef", 120, 60);
const pig = new LivestockAnimal("pig", "Pig", "circle", 200, 45);

const chickenNode = new TreeNode(chicken);
const cowNode = new TreeNode(cow, ["chicken"]);
const pigNode = new TreeNode(pig, ["chicken"]);
chickenNode.addChild(cowNode);
chickenNode.addChild(pigNode);
const livestockTree = new UnlockTree(chickenNode);

const unlockTrees = {
  garden: gardenTree,
  fishpond: fishTree,
  livestock: livestockTree,
};

const SAMPLE_PRODUCTS = [
  new Product("egg", "Egg", "egg"),
  new Product("milk", "Milk", "milk"),
  new Product("fish", "Fish", "fish"),
  new Product("wheat", "Wheat", "wheat"),
  new Product("carrot", "Carrot", "carrot"),
];

function refreshIcons() {
  if (window.lucide) lucide.createIcons();
}

function setStatus(msg) {
  document.getElementById("grid-status").textContent = msg;
}

function updateCoins() {
  document.getElementById("coin-count").textContent = playerCoins;
}

function renderGrid() {
  const grid = areaGrids[currentArea];
  const container = document.getElementById("area-grid");
  container.innerHTML = "";
  container.style.gridTemplateColumns = `repeat(${grid.cols}, minmax(0, 1fr))`;

  document.getElementById("grid-label").textContent =
    currentArea === "garden"
      ? "Garden Grid (6×6)"
      : currentArea === "fishpond"
        ? "Fish Pond Grid (5×5)"
        : "Livestock Grid (5×6)";

  for (let r = 0; r < grid.rows; r++) {
    for (let c = 0; c < grid.cols; c++) {
      const cell = document.createElement("div");
      const entity = grid.get(r, c);
      const isSelected =
        selectedCell && selectedCell.row === r && selectedCell.col === c;

      cell.className = `farm-cell w-12 h-12 sm:w-14 sm:h-14 bg-white border border-green-200 rounded-lg flex items-center justify-center cursor-pointer transition ${
        isSelected ? "selected" : ""
      }`;
      if (entity) {
        cell.innerHTML = `<i data-lucide="${entity.icon}" class="w-5 h-5 text-green-700"></i>`;
        cell.title = entity.name;
      }

      cell.addEventListener("click", () => {
        selectedCell = { row: r, col: c };
        renderGrid();
        setStatus(
          `Selected (${r}, ${c})` + (entity ? ` — ${entity.name}` : " — empty")
        );
        refreshIcons();
      });
      container.appendChild(cell);
    }
  }
  refreshIcons();
}

function renderInventory() {
  const container = document.getElementById("inventory-slots");
  container.innerHTML = "";
  inventory.slots.forEach((item) => {
    const slot = document.createElement("div");
    slot.className =
      "w-10 h-10 border border-gray-200 rounded-lg flex items-center justify-center bg-gray-50";
    if (item) {
      slot.innerHTML = `<i data-lucide="${item.icon}" class="w-5 h-5 text-amber-700"></i>`;
      slot.title = item.name;
    }
    container.appendChild(slot);
  });
  document.getElementById("inv-count").textContent =
    `${inventory.count} / ${inventory.capacity}`;
  refreshIcons();
}

function renderQueue() {
  const container = document.getElementById("queue-display");
  container.innerHTML = "";
  const items = productionQueue.toArray();
  if (items.length === 0) {
    container.innerHTML =
      '<span class="text-xs text-gray-400">Queue empty</span>';
    return;
  }
  items.forEach((p, i) => {
    const chip = document.createElement("span");
    chip.className =
      "inline-flex items-center gap-1 bg-green-100 text-green-800 text-xs px-2.5 py-1 rounded-full";
    chip.innerHTML = `<i data-lucide="${p.icon}" class="w-3.5 h-3.5"></i> ${p.name}`;
    if (i === 0) chip.classList.add("ring-2", "ring-green-400");
    container.appendChild(chip);
  });
  refreshIcons();
}

function renderUnlockCards() {
  const container = document.getElementById("unlock-cards");
  container.innerHTML = "";
  const tree = unlockTrees[currentArea];
  const nodes = tree.flatten();

  nodes.forEach((node) => {
    const { entity } = node;
    const card = document.createElement("button");
    card.className = `entity-card text-left p-3 rounded-xl border transition ${
      entity.unlocked
        ? "bg-white border-green-300 hover:border-green-500 hover:shadow-md cursor-pointer"
        : "bg-gray-100 border-gray-200 locked cursor-pointer"
    }`;

    card.innerHTML = `
      <div class="flex items-center gap-2">
        <i data-lucide="${entity.unlocked ? entity.icon : "lock"}" class="w-5 h-5 ${
          entity.unlocked ? "text-green-600" : "text-gray-400"
        }"></i>
        <div>
          <p class="font-semibold text-sm">${entity.name}</p>
          <p class="text-xs text-gray-500">
            ${
              entity.unlocked
                ? "Unlocked · click to place"
                : `<span class="inline-flex items-center gap-0.5"><i data-lucide="coins" class="w-3 h-3"></i>${entity.unlockCost}</span>`
            }
          </p>
        </div>
      </div>
    `;

    card.addEventListener("click", () => {
      if (!entity.unlocked) {
        const result = tree.tryUnlock(entity.id, playerCoins);
        if (result.success) {
          playerCoins -= result.coinsSpent;
          updateCoins();
          setStatus(`Unlocked ${entity.name} (−${result.coinsSpent} coins)`);
          renderUnlockCards();
        } else {
          setStatus(`⚠️ ${result.reason}`);
        }
        refreshIcons();
        return;
      }
      tryPlaceEntity(entity);
    });

    container.appendChild(card);
  });
  refreshIcons();
}

function renderActionLog() {
  const list = document.getElementById("action-log");
  list.innerHTML = "";
  const actions = actionHistory.toArray().reverse();
  if (actions.length === 0) {
    list.innerHTML = '<li class="text-gray-400 text-xs">No actions yet</li>';
    return;
  }
  actions.forEach((a) => {
    const li = document.createElement("li");
    li.className = "text-xs";
    if (a.type === "place") {
      li.textContent = `Place ${a.entity.name} @ ${a.area} (${a.row},${a.col})`;
    } else {
      li.textContent = JSON.stringify(a);
    }
    list.appendChild(li);
  });
}

function renderAll() {
  updateCoins();
  renderGrid();
  renderInventory();
  renderQueue();
  renderUnlockCards();
  renderActionLog();
}

function tryPlaceEntity(entity) {
  if (!selectedCell) {
    setStatus("⚠️ Select a cell first!");
    return;
  }
  const grid = areaGrids[currentArea];
  const { row, col } = selectedCell;

  const placed = Object.assign(
    Object.create(Object.getPrototypeOf(entity)),
    entity
  );

  if (!grid.place(placed, row, col)) {
    setStatus("⚠️ Cell already occupied!");
    return;
  }

  actionHistory.push({
    type: "place",
    entity: placed,
    row,
    col,
    area: currentArea,
  });
  setStatus(`Placed ${entity.name} at (${row}, ${col})`);

  const product =
    SAMPLE_PRODUCTS[Math.floor(Math.random() * SAMPLE_PRODUCTS.length)];
  inventory.addItem(product);

  renderAll();
}

function undoLastAction() {
  if (actionHistory.isEmpty) return;
  const action = actionHistory.pop();
  if (action.type === "place") {
    areaGrids[action.area].remove(action.row, action.col);
    setStatus(`Undid ${action.entity.name}`);
  }
  renderAll();
}

function enqueueNormal() {
  const p = SAMPLE_PRODUCTS[Math.floor(Math.random() * SAMPLE_PRODUCTS.length)];
  productionQueue.enqueue(p);
  renderQueue();
}

function enqueueRush() {
  const p = SAMPLE_PRODUCTS[Math.floor(Math.random() * SAMPLE_PRODUCTS.length)];
  productionQueue.addFront(p);
  renderQueue();
}

function dequeueOne() {
  const item = productionQueue.dequeue();
  if (item) {
    inventory.addItem(item);
    renderInventory();
  }
  renderQueue();
}

initNav((area) => {
  currentArea = area;
  selectedCell = null;
  setStatus(`Switched to ${area}`);
  renderAll();
});

document.getElementById("btn-undo").addEventListener("click", undoLastAction);
document.getElementById("btn-enqueue").addEventListener("click", enqueueNormal);
document.getElementById("btn-rush").addEventListener("click", enqueueRush);
document.getElementById("btn-dequeue").addEventListener("click", dequeueOne);

renderAll();
setTimeout(refreshIcons, 80);