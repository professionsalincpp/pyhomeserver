const elementsWithRipple = document.querySelectorAll('.ripple');
console.log(elementsWithRipple);
elementsWithRipple.forEach(elementWithRipple => {
  elementWithRipple.addEventListener('pointerdown', (mouseEvent) => {
    // Create a ripple element <div class="ripple">
    const rippleEl = document.createElement('span');
    rippleEl.classList.add('ripple-span');
    
    // Position the ripple
    const x = mouseEvent.offsetX + elementWithRipple.offsetLeft;
    const y = mouseEvent.offsetY + elementWithRipple.offsetTop;
    
    rippleEl.style.left = `${x}px`;
    rippleEl.style.top = `${y}px`;
    
    elementWithRipple.appendChild(rippleEl);
    
    requestAnimationFrame(() => {
      rippleEl.classList.add('run');
    });
    
    // Remove ripple element when the transition is done
    rippleEl.addEventListener('transitionend', () => {
      rippleEl.remove();
    });
  });
})
