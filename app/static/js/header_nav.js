//<!-- JavaScript to control the profile navigation drawer -->

let profile = document.querySelector(".profile");
let menu = document.querySelector(".menu");

profile.onclick = function () {
  menu.classList.toggle("active");
};

/* Custom JavaScript for Material Style Navigation Drawer */
function openNav() {
  document.getElementById("myNav").classList.add("drawer-open");
}

function closeNav() {
  document.getElementById("myNav").classList.remove("drawer-open");
}

// Function to toggle the navigation menu
function toggleMenu() {
  let container = document.querySelector(".container-fluid");
  container.classList.toggle("nav-closed");
}

// Function to hide the sidebar on small screens
function hideSidebarOnSmallScreens() {
  let container = document.querySelector(".container-fluid");
  if (window.innerWidth <= 991) {
    container.classList.add("nav-closed");
  } else {
    container.classList.remove("nav-closed");
  }
}

// Call the function initially to hide the sidebar if needed
hideSidebarOnSmallScreens();

// Adding resize event listener to toggle sidebar on small screens
window.addEventListener("resize", hideSidebarOnSmallScreens);

// greating messages based on the current time
// Get the current hour
const currentHour = new Date().getHours();

// Get the greeting element
const greetingElement = document.getElementById("greeting");

// Define the greeting messages based on the time of day
let greetingMessage = "";
if (currentHour >= 5 && currentHour < 12) {
  greetingMessage = "Good Morning";
} else if (currentHour >= 12 && currentHour < 18) {
  greetingMessage = "Good Afternoon";
} else {
  greetingMessage = "Good Evening";
}

// Update the greeting message in the HTML
greetingElement.textContent = greetingMessage;


// js to display the clock
function updateClock() {
  // Get current UTC time
  const nowUTC = new Date();

  // Convert UTC time to GMT+3 time
  const nowGMT3 = new Date(nowUTC.getTime() + (3 * 60 * 60 * 1000));

  // Extract hours, minutes, and seconds from GMT+3 time
  const hours = nowGMT3.getUTCHours().toString().padStart(2, '0');
  const minutes = nowGMT3.getUTCMinutes().toString().padStart(2, '0');
  const seconds = nowGMT3.getUTCSeconds().toString().padStart(2, '0');

  // Format time string
  const timeString = `${hours}:${minutes}:${seconds}`;

  // Update the clock element
  document.getElementById('clock').innerText = timeString;
}

// Update the clock every second
setInterval(updateClock, 1000);

// Initial update to prevent delay in displaying clock
updateClock();
