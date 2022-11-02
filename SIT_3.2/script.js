    const button = document.getElementById('1');
    const graph = document.getElementById('2');
    const inlineStyles = graph.style

    button.addEventListener('click', updateButton);
    function updateButton() {
        if (button.value === 'Построить') {
            button.value = 'Скрыть';
            graph.setAttribute('style', 'opacity:1;')
        } else {
            button.value = 'Построить';
            graph.setAttribute('style', 'opacity:0;')
        }
    }
