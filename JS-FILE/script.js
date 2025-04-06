document.addEventListener("DOMContentLoaded", function () {
    const businessBoxes = document.querySelectorAll(".business-box");
  
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("animated");
          }
        });
      },
      { threshold: 0.1 }
    );
  
    businessBoxes.forEach((box) => observer.observe(box));
  });
  
  
    document.addEventListener("DOMContentLoaded", function() {
        const programs = document.querySelectorAll('.program');
  
        const inView = (el) => {
            const rect = el.getBoundingClientRect();
            return rect.top >= 0 && rect.top <= window.innerHeight;
        };
  
        const handleScroll = () => {
            programs.forEach(program => {
                if (inView(program)) {
                    program.classList.add('in-view');
                }
            });
        };
  
        // Initial check
        handleScroll();
  
        // Scroll event
        window.addEventListener('scroll', handleScroll);
    });