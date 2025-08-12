// Инициализация Telegram WebApp
const tg = window.Telegram.WebApp;

// Развернуть приложение на весь экран (опционально)
tg.expand();

// Обработчик кнопки
document.getElementById("btn-alert").addEventListener("click", () => {
    tg.showAlert("Кнопка нажата!");
});

// Получение данных пользователя (если нужно)
const user = tg.initDataUnsafe?.user;
console.log("User:", user);

// Закрыть приложение (например, после выполнения действия)
// tg.close();