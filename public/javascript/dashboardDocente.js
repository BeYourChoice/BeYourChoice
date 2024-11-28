

// Effetto di animazione al clic sui pulsanti
document.querySelectorAll('.button').forEach(button => {
    button.addEventListener('click', () => {
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 200);
    });
});
