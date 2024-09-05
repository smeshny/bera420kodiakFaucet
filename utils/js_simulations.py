simulaion_mouse_move = """
// Функция для симуляции рваных движений мыши вокруг элемента
function simulateJaggedMouseMovement(element, steps, duration) {
    let centerX = element.getBoundingClientRect().left + element.offsetWidth / 2;
    let centerY = element.getBoundingClientRect().top + element.offsetHeight / 2;

    let step = 0;
    let interval = duration / steps;

    let mouseMoveInterval = setInterval(function() {
        // Генерируем случайное смещение в пределах 20 пикселей от центра
        let randomXOffset = (Math.random() - 0.5) * 20;  // Смещение влево-вправо
        let randomYOffset = (Math.random() - 0.5) * 20;  // Смещение вверх-вниз

        let x = centerX + randomXOffset;
        let y = centerY + randomYOffset;

        // Симулируем перемещение мыши в точку (x, y)
        let evt = new MouseEvent('mousemove', {
            clientX: x,
            clientY: y,
            bubbles: true
        });
        document.dispatchEvent(evt);

        step++;

        // Останавливаем движение после завершения всех шагов
        if (step > steps) {
            clearInterval(mouseMoveInterval);
        }
    }, interval);
}

// Находим элемент по XPath
let xpath = '//*[@id="root"]/div/div/div[2]/button';
let element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

// Симулируем рваное движение мыши вокруг элемента
simulateJaggedMouseMovement(element, 50, 2000);  // 50 шагов за 1 секунду
    """


simulaion_mouse_move_and_click = """
    // Функция для плавного перемещения мыши к элементу и симуляции клика
function simulateHumanClick(element) {
    let centerX = element.getBoundingClientRect().left + element.offsetWidth / 2;
    let centerY = element.getBoundingClientRect().top + element.offsetHeight / 2;

    // Шаги для плавного движения мыши к кнопке
    let steps = 30;
    let step = 0;
    let interval = 20;  // Интервал в миллисекундах для каждого шага

    let mouseMoveInterval = setInterval(function() {
        // Постепенно приближаемся к центру кнопки
        let randomXOffset = (Math.random() - 0.5) * 5;  // Небольшие отклонения при движении к центру
        let randomYOffset = (Math.random() - 0.5) * 5;

        let x = centerX + randomXOffset;
        let y = centerY + randomYOffset;

        // Симулируем перемещение мыши к кнопке
        let moveEvt = new MouseEvent('mousemove', {
            clientX: x,
            clientY: y,
            bubbles: true
        });
        document.dispatchEvent(moveEvt);

        step++;

        // Когда мышь "достигла" кнопки, симулируем клик
        if (step >= steps) {
            clearInterval(mouseMoveInterval);

            // Задержка перед кликом, чтобы имитировать паузу перед нажатием
            setTimeout(function() {
                // Симулируем наведение (mouseover)
                let overEvt = new MouseEvent('mouseover', {
                    clientX: centerX,
                    clientY: centerY,
                    bubbles: true
                });
                element.dispatchEvent(overEvt);

                // Симулируем нажатие мыши
                let downEvt = new MouseEvent('mousedown', {
                    clientX: centerX,
                    clientY: centerY,
                    bubbles: true
                });
                element.dispatchEvent(downEvt);

                // Симулируем отпускание мыши (click)
                let upEvt = new MouseEvent('mouseup', {
                    clientX: centerX,
                    clientY: centerY,
                    bubbles: true
                });
                element.dispatchEvent(upEvt);

                // Завершающий клик
                let clickEvt = new MouseEvent('click', {
                    clientX: centerX,
                    clientY: centerY,
                    bubbles: true
                });
                element.dispatchEvent(clickEvt);

                console.log('Клик выполнен!');
            }, 100 + Math.random() * 200);  // Небольшая случайная задержка перед кликом
        }
    }, interval);
}

// Находим элемент по XPath
let xpath = '//*[@id="root"]/div/div/div[2]/button';
let element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

// Имитация клика по элементу
simulateHumanClick(element);
    """