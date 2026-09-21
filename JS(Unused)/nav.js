export function initNav(onAreaChange) {
  const sideNav = document.getElementById("side-nav");
  const backdrop = document.getElementById("nav-backdrop");
  const areaTitle = document.getElementById("area-title");

  function openMenu() {
    sideNav.classList.remove("hidden");
    backdrop.classList.remove("hidden");
  }

  function closeMenu() {
    sideNav.classList.add("hidden");
    backdrop.classList.add("hidden");
  }

  document.getElementById("menu-toggle").addEventListener("click", openMenu);
  document.getElementById("menu-close").addEventListener("click", closeMenu);
  backdrop.addEventListener("click", closeMenu);

  const titles = {
    garden: "🌱 Garden",
    fishpond: "🐟 Fish Pond",
    livestock: "🐔 Livestock Farm",
  };

  document.querySelectorAll(".nav-item").forEach((btn) => {
    btn.addEventListener("click", () => {
      const area = btn.dataset.area;
      areaTitle.textContent = titles[area];
      closeMenu();
      onAreaChange(area);
    });
  });
}