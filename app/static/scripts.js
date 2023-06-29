const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    console.log(entry)
    if (entry.isIntersecting) {
        entry.target.classList.add('visible');
    }
  });
});

const hiddenElements = document.querySelectorAll('.invisibleanimate');
hiddenElements.forEach((el) => observer.observe(el));

$('img').attr('draggable', false);
