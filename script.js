gsap.registerPlugin(ScrollTrigger, ScrollToPlugin);

let allowScroll = true;
let scrollTimeout = gsap.delayedCall(1, () => allowScroll = true).pause();
let currentIndex = 0;
let swipePanels = gsap.utils.toArray(".swipe-section .panel");

gsap.set(swipePanels, { zIndex: i => swipePanels.length - i });

let intentObserver = ScrollTrigger.observe({
    type: "wheel,touch",
    onUp: () => allowScroll && gotoPanel(currentIndex - 1, false),
    onDown: () => allowScroll && gotoPanel(currentIndex + 1, true),
    tolerance: 10,
    preventDefault: true,
    onEnable(self) {
        allowScroll = false;
        scrollTimeout.restart(true);
        let savedScroll = self.scrollY();
        self._restoreScroll = () => self.scrollY(savedScroll);
        document.addEventListener("scroll", self._restoreScroll, { passive: false });
    },
    onDisable: self => document.removeEventListener("scroll", self._restoreScroll)
});
intentObserver.disable();

function gotoPanel(index, isScrollingDown) {
    if ((index === swipePanels.length && isScrollingDown) || (index === -1 && !isScrollingDown)) {
        intentObserver.disable();
        return;
    }
    allowScroll = false;
    scrollTimeout.restart(true);

    let target = isScrollingDown ? swipePanels[currentIndex] : swipePanels[index];
    gsap.to(target, {
        yPercent: isScrollingDown ? -100 : 0,
        duration: 0.75
    });

    currentIndex = index;
}

ScrollTrigger.create({
    trigger: ".swipe-section",
    pin: true,
    start: "top top",
    end: "+=200",
    onEnter: (self) => {
        if (intentObserver.isEnabled) { return; }
        self.scroll(self.start + 1);
        intentObserver.enable();
    },
    onEnterBack: (self) => {
        if (intentObserver.isEnabled) { return; }
        self.scroll(self.end - 1);
        intentObserver.enable();
    }
});

function scrollToSection(sectionClass) {
    const section = document.querySelector(`.${sectionClass}`);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Add event listeners to anchor links
document.querySelectorAll(".anchor").forEach(anchor => {
    anchor.addEventListener("click", function (e) {
        e.preventDefault(); // Prevent default anchor link behavior

        // Get the target section based on the href attribute of the clicked link
        let targetElem = document.querySelector(e.target.getAttribute("href"));
        console.log("Anchor clicked:", anchor.getAttribute("href"));
        
        if (targetElem && (targetElem.id === "beginning-page" || targetElem.id === "references")) {
            disableAllScrollTriggers(); // Disable scroll triggers if outside swipe panels
            targetElem.scrollIntoView({ behavior: 'smooth' });
        } else if (targetElem) {
            // Scroll smoothly to the target section
            gsap.to(window, {
                duration: 1,
                scrollTo: {
                    y: targetElem
                }
            });
        }
    });
});

// Adjust scroll effect for Data Analysis section
const textThree = document.getElementById("textThree");

gsap.to(textThree, {
    y: 400 - textThree.clientHeight - 32,
    scrollTrigger: {
        trigger: "#data-analysis",
        pin: "#data-analysis",
        scrub: true,
        start: "top top",
        end: "+=700px",
        markers: true // Optional: remove in production
    }
});
document.querySelectorAll('.scrollable-content').forEach(content => {
  ScrollTrigger.create({
    trigger: content,
    start: "top top",
    end: "bottom bottom",
    scrub: true,
    markers: false, // Set to true for debugging
    onEnter: () => gsap.to(content, { y: 0, duration: 0.5 }), // Smooth scroll start
    onLeave: () => gsap.to(content, { y: -content.scrollHeight, duration: 0.5 }) // Smooth scroll end
  });
});



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
