gsap.registerPlugin(ScrollTrigger, ScrollToPlugin);

function scrollToSection(sectionClass) {
    const section = document.querySelector(`.${sectionClass}`);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

function toggleSection(headerElement) {
  const section = headerElement.nextElementSibling;
  if (section.style.display === "none" || !section.style.display) {
    section.style.display = "block"; // Expand the section
  } else {
    section.style.display = "none"; // Collapse the section
  }
}

function togglePopup() {
    const popup = document.getElementById("popup");
    popup.style.display = popup.style.display === "flex" ? "none" : "flex";
}

function togglePopup1() {
    const popup = document.getElementById("popup");
    popup.style.display = popup.style.display === "none" || popup.style.display === "" ? "block" : "none";
}

function togglePopup(popupId) {
    const popup = document.getElementById(popupId);
    if (popup) {
        popup.style.display = popup.style.display === "none" || popup.style.display === "" ? "block" : "none";
    }
}
