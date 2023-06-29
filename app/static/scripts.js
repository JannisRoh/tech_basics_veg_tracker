
// Animation effect triggered when object is visible. Code from this tutorial: https://www.youtube.com/watch?v=T33NN_pPeNI
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    console.log(entry);
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
});

const hiddenElements = document.querySelectorAll('.invisibleanimate');
hiddenElements.forEach((el) => observer.observe(el));

// Making images non-draggable. There are so many images used in the background, that their draggability becomes annoying.
$('img').attr('draggable', false);
