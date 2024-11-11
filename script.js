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

function togglePopup(popupId) {
    const popup = document.getElementById(popupId);
    if (popup) {
        popup.style.display = popup.style.display === "none" || popup.style.display === "" ? "block" : "none";
    }
}


document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const targetElement = document.querySelector(this.getAttribute('href'));
      if (targetElement) {
          window.scrollTo({
              top: targetElement.offsetTop,
              behavior: 'smooth'
          });
      }
  });
});

document.addEventListener('DOMContentLoaded', (event) => {
  const smoothScroll = (targetElement, duration) => {
      const targetPosition = targetElement.getBoundingClientRect().top + window.scrollY;
      const startPosition = window.scrollY;
      const distance = targetPosition - startPosition;
      let startTime = null;

      const animation = (currentTime) => {
          if (startTime === null) startTime = currentTime;
          const timeElapsed = currentTime - startTime;
          const run = ease(timeElapsed, startPosition, distance, duration);
          window.scrollTo(0, run);
          if (timeElapsed < duration) requestAnimationFrame(animation);
      };

      const ease = (t, b, c, d) => {
          t /= d / 2;
          if (t < 1) return c / 2 * t * t + b;
          t--;
          return -c / 2 * (t * (t - 2) - 1) + b;
      };

      requestAnimationFrame(animation);
  };

  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
          e.preventDefault();
          const targetElement = document.querySelector(this.getAttribute('href'));
          if (targetElement) {
              smoothScroll(targetElement, 1500); // Adjust the duration here
          }
      });
  });
});

document.addEventListener("DOMContentLoaded", function() {
  const sections = document.querySelectorAll(".panel");
  
  const options = {
      root: null,
      rootMargin: "0px",
      threshold: 0.1
  };

  const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
          const header = entry.target.querySelector("h1");
          if (entry.isIntersecting) {
              header.classList.add("sticky-heading");
          } else {
              header.classList.remove("sticky-heading");
          }
      });
  }, options);

  sections.forEach(section => {
      observer.observe(section);
  });
});

function scrollToFigureInColumn(figureId) {
  const figure = document.getElementById(figureId);
  const figuresColumn = document.getElementById("figuresColumn");

  if (figure && figuresColumn) {
    // Calculate the offset of the figure within figuresColumn
    const offsetTop = figure.offsetTop - figuresColumn.scrollTop;
    
    // Smoothly scroll figuresColumn to the figure's position
    figuresColumn.scrollTo({
      top: offsetTop,
      behavior: "smooth"
    });
  }
}
 document.addEventListener('DOMContentLoaded', () => {
            fetch('https://raw.githubusercontent.com/elhuang04/cs299-project4/main/README.md')
                .then(response => response.text())
                .then(markdown => {
                    const converter = new showdown.Converter();
                    const html = converter.makeHtml(markdown);
                    document.getElementById('markdown-content').innerHTML += html;
                })
                .catch(error => console.error('Error fetching markdown:', error));

            document.getElementById('expand-link').addEventListener('click', function () {
                const card = document.getElementById('markdown-content');
                card.classList.add('expanded');
                document.getElementById('expand-link').style.display = 'none';
                document.getElementById('minimize-link').style.display = 'block';
            });

            document.getElementById('minimize-link').addEventListener('click', function () {
                const card = document.getElementById('markdown-content');
                card.classList.remove('expanded');
                document.getElementById('expand-link').style.display = 'block';
                document.getElementById('minimize-link').style.display = 'none';
            });
        });






