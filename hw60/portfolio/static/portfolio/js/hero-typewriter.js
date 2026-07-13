document.addEventListener('DOMContentLoaded', () => {
    const terminalBody = document.getElementById('terminal-content');
    if (!terminalBody) return;

    // Перевіряємо уподобання користувача щодо зменшення анімації
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const devName = terminalBody.getAttribute('data-name') || 'Кірілл';
    const devRole = terminalBody.getAttribute('data-role') || 'Python Backend & Web3 Automation Developer';

    // Дані для друку
    const commandText = 'python manage.py runserver';
    const serverOutput = [
        'Watching for file changes with StatReloader',
        'Performing system checks...',
        'System check identified no issues (0 silenced).',
        `Django version 6.0.6, using settings "DevPortfolio.settings"`,
        'Starting development server at http://127.0.0.1:8000/',
        'Quit the server with CONTROL-C.',
        '',
        '[INFO] Welcome to the Evening Terminal.',
        `[SUCCESS] Loaded Profile: ${devName} — ${devRole}.`,
        'Status: Active & ready for new projects.'
    ];

    if (prefersReducedMotion) {
        // Якщо увімкнено "prefers-reduced-motion", показуємо все одразу без анімації
        let fullHTML = `<span class="terminal-prompt">$ </span><span class="terminal-command">${commandText}</span>\n`;
        serverOutput.forEach(line => {
            if (line.startsWith('[SUCCESS]')) {
                fullHTML += `<span class="terminal-success">${line}</span>\n`;
            } else if (line.startsWith('[INFO]')) {
                fullHTML += `<span class="terminal-info">${line}</span>\n`;
            } else {
                fullHTML += `${line}\n`;
            }
        });
        fullHTML += `<span class="terminal-prompt">$ </span><span class="cursor"></span>`;
        terminalBody.innerHTML = fullHTML;
        return;
    }

    // Починаємо анімацію друку
    terminalBody.innerHTML = '<span class="terminal-prompt">$ </span><span id="typing-command" class="terminal-command"></span><span class="cursor"></span>';
    const typingSpan = document.getElementById('typing-command');
    const cursor = terminalBody.querySelector('.cursor');

    let charIndex = 0;
    
    function typeCommand() {
        if (charIndex < commandText.length) {
            typingSpan.textContent += commandText.charAt(charIndex);
            charIndex++;
            setTimeout(typeCommand, 60); // Швидкість друку команди
        } else {
            // Після того, як надрукували команду, робимо невелику паузу та виводимо лог сервера
            setTimeout(showServerOutput, 600);
        }
    }

    let lineIndex = 0;
    function showServerOutput() {
        // Видаляємо курсор перед тим, як додавати нові рядки
        if (cursor) cursor.remove();

        if (lineIndex < serverOutput.length) {
            const line = serverOutput[lineIndex];
            const lineDiv = document.createElement('div');
            
            if (line.startsWith('[SUCCESS]')) {
                lineDiv.className = 'terminal-success';
                lineDiv.textContent = line;
            } else if (line.startsWith('[INFO]')) {
                lineDiv.className = 'terminal-info';
                lineDiv.textContent = line;
            } else {
                lineDiv.textContent = line;
            }
            
            terminalBody.appendChild(lineDiv);
            lineIndex++;
            
            // Ефект швидкого рядкового виводу як при запуску реального сервера
            setTimeout(showServerOutput, 150);
        } else {
            // В кінці додаємо фінальний промпт $ з мигаючим курсором
            const finalPrompt = document.createElement('div');
            finalPrompt.innerHTML = '<span class="terminal-prompt">$ </span><span class="cursor"></span>';
            terminalBody.appendChild(finalPrompt);
        }
    }

    // Запускаємо першу фазу
    setTimeout(typeCommand, 400);
});
