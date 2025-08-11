//let tg = window.Telegram.WebApp;
//
//// Показываем имя пользователя из Telegram
//tg.expand();
//document.getElementById("user").innerText =
//    tg.initDataUnsafe.user
//    ? `Ваше имя: ${tg.initDataUnsafe.user.first_name}`
//    : "Пользователь не найден";
//
//// Кнопка отправки данных в бота
//document.getElementById("sendData").addEventListener("click", () => {
//    let data = {
//        action: "test_action",
//        value: "Hello from Mini App"
//    };
//    tg.sendData(JSON.stringify(data));
//});
