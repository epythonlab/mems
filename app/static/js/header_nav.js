// JavaScript to control the profile navigation drawer
document.addEventListener("DOMContentLoaded", function() {
  console.log("DOM content loaded");
  let profile = document.querySelector(".profile");
  let menu = document.querySelector(".menu");

  profile.onclick = function () {
    menu.classList.toggle("active");
    if (menu.classList.contains("active")) {
      profile.style.height = "100%"; // Expand profile height when menu is active
    } else {
      profile.style.height = "5%"; // Reset profile height when menu is inactive
    }
  };
});

// toggle side bar
function toggleMenu() {
  let container = document.querySelector(".container-fluid");
  container.classList.toggle("nav-closed");
}

function hideSidebarOnSmallScreens() {
  let container = document.querySelector(".container-fluid");
  if (window.innerWidth <= 991) {
    container.classList.add("nav-closed");
  } else {
    container.classList.remove("nav-closed");
  }
}

hideSidebarOnSmallScreens();

window.addEventListener("resize", hideSidebarOnSmallScreens);

// clock js
const currentHour = new Date().getHours();
const greetingElement = document.getElementById("greeting");
let greetingMessage = "";
if (currentHour >= 5 && currentHour < 12) {
  greetingMessage = "Good Morning";
} else if (currentHour >= 12 && currentHour < 18) {
  greetingMessage = "Good Afternoon";
} else {
  greetingMessage = "Good Evening";
}

greetingElement.textContent = greetingMessage;

function updateClock() {
  const nowUTC = new Date();
  const nowGMT3 = new Date(nowUTC.getTime() + (3 * 60 * 60 * 1000));
  const hours = nowGMT3.getUTCHours().toString().padStart(2, '0');
  const minutes = nowGMT3.getUTCMinutes().toString().padStart(2, '0');
  const seconds = nowGMT3.getUTCSeconds().toString().padStart(2, '0');
  const timeString = `${hours}:${minutes}:${seconds}`;
  document.getElementById('clock').innerText = timeString;
}

setInterval(updateClock, 1000);
updateClock();
