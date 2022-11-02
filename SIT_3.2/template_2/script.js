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



        switch(a) {
            case '0':
    test.insertAdjacentHTML('afterbegin', 'f(x) = + x<small><sup>3</sup></small> ' +
        '- 6x<small><sup>2</sup></small>' +
        ' + x + 5</span>');
    break;
        case '1':
    test.insertAdjacentHTML('afterbegin', 'y(x) = x<small><sup>2</sup></small> - 5x + 1');
    break;

        case '2':
    test.insertAdjacentHTML('afterbegin', '<div>  z(x) = <span style="opacity: 0">" </span>  </div> ' +
        '<div class="frac"> <span>1</span>\n' +
        '<span class="symbol">/</span>\n' +
        '<span class="bottom">x<small><sup>2</sup></small> + 1</span></div>');
    break;

}
