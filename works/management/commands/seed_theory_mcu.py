"""Наполнить раздел микроконтроллеров теорией Arduino / ESP32."""
from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson


MODULES = [
    {
        'title': 'Введение в Arduino',
        'icon': 'fas fa-microchip',
        'order': 1,
        'description': 'Что такое Arduino, структура скетча, первые шаги.',
        'lessons': [
            {
                'title': 'Что такое Arduino?',
                'order': 1,
                'estimated_minutes': 10,
                'content': '''<h2>Что такое Arduino?</h2>
<p><strong>Arduino</strong> — открытая платформа прототипирования на основе микроконтроллера AVR (Uno, Nano) или ARM (Due, MKR). Плата содержит:</p>
<ul>
  <li><strong>Микроконтроллер</strong> — ATmega328P (Uno), тактовая частота 16 МГц</li>
  <li><strong>14 цифровых пинов</strong> (0-13), 6 из них поддерживают ШИМ (3, 5, 6, 9, 10, 11)</li>
  <li><strong>6 аналоговых входов</strong> (A0-A5), 10-битный АЦП (0-1023)</li>
  <li><strong>USB-интерфейс</strong> для загрузки кода и монитора порта</li>
  <li><strong>Питание</strong>: 5 В от USB или 7-12 В через разъём питания</li>
</ul>
<h3>Среда разработки</h3>
<p>Код пишется в <strong>Arduino IDE</strong> или PlatformIO. Язык — C++ с упрощённым API (Arduino framework). Готовый скетч загружается в память контроллера по USB.</p>''',
                'code_example': '''// Минимальный скетч Arduino
void setup() {
  // Вызывается один раз при старте
  pinMode(13, OUTPUT);  // LED на пине 13
  Serial.begin(9600);   // Инициализация порта
}

void loop() {
  // Выполняется бесконечно
  digitalWrite(13, HIGH);  // LED включить
  delay(500);               // Пауза 500 мс
  digitalWrite(13, LOW);   // LED выключить
  delay(500);
}''',
            },
            {
                'title': 'GPIO: цифровые входы и выходы',
                'order': 2,
                'estimated_minutes': 15,
                'content': '''<h2>GPIO — General Purpose Input/Output</h2>
<p>Каждый цифровой пин может работать в режиме:</p>
<table>
  <thead><tr><th>Режим</th><th>Функция</th><th>Типичное применение</th></tr></thead>
  <tbody>
    <tr><td>OUTPUT</td><td>Управление нагрузкой</td><td>LED, реле, мотор через ключ</td></tr>
    <tr><td>INPUT</td><td>Чтение сигнала</td><td>Кнопка (с внешним резистором)</td></tr>
    <tr><td>INPUT_PULLUP</td><td>Чтение с подтяжкой к +5В</td><td>Кнопка без внешнего резистора</td></tr>
  </tbody>
</table>
<h3>Функции</h3>
<ul>
  <li><code>pinMode(pin, mode)</code> — настроить пин</li>
  <li><code>digitalWrite(pin, HIGH/LOW)</code> — выставить уровень</li>
  <li><code>digitalRead(pin)</code> — считать уровень (0 или 1)</li>
</ul>
<h3>Важно: защита пинов</h3>
<p>Максимальный ток с пина — <strong>40 мА</strong> (рекомендуется ≤20 мА). Светодиод подключают через резистор 220–470 Ом: <em>R = (Vcc − Vled) / Iled</em>.</p>''',
                'code_example': '''// Кнопка включает LED
const int BTN = 2;
const int LED = 13;

void setup() {
  pinMode(BTN, INPUT_PULLUP); // Внутренняя подтяжка к 5В
  pinMode(LED, OUTPUT);
}

void loop() {
  // Кнопка замыкает на GND → LOW = нажата
  if (digitalRead(BTN) == LOW) {
    digitalWrite(LED, HIGH);
  } else {
    digitalWrite(LED, LOW);
  }
}''',
            },
            {
                'title': 'ШИМ и аналоговые сигналы',
                'order': 3,
                'estimated_minutes': 15,
                'content': '''<h2>ШИМ — широтно-импульсная модуляция</h2>
<p>ШИМ имитирует аналоговый сигнал быстрым переключением пина. Параметр — <strong>скважность (duty cycle)</strong> от 0 до 255.</p>
<ul>
  <li>0 → 0 В, 255 → 5 В, 128 ≈ 2.5 В (среднее)</li>
  <li>Частота ШИМ на Uno: ~490 Гц (пины 5, 6 — ~980 Гц)</li>
</ul>
<h3>Аналоговый вход (АЦП)</h3>
<p>Пины A0-A5 читают напряжение 0-5 В и возвращают число 0-1023 (10 бит).</p>
<p>Формула перевода в вольты: <code>V = (analogRead(pin) / 1023.0) * 5.0</code></p>
<h3>Функции</h3>
<ul>
  <li><code>analogWrite(pin, 0-255)</code> — ШИМ-сигнал</li>
  <li><code>analogRead(pin)</code> — считать АЦП (A0-A5)</li>
</ul>''',
                'code_example': '''// Плавное изменение яркости LED
const int LED = 9;   // Пин с поддержкой ШИМ
const int POT = A0;  // Потенциометр

void setup() {
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int raw = analogRead(POT);          // 0-1023
  int brightness = raw / 4;           // 0-255
  float voltage = raw * 5.0 / 1023.0;
  analogWrite(LED, brightness);
  Serial.print("ADC="); Serial.print(raw);
  Serial.print("  V="); Serial.println(voltage);
  delay(50);
}''',
            },
        ],
    },
    {
        'title': 'Датчики и интерфейсы',
        'icon': 'fas fa-thermometer-half',
        'order': 2,
        'description': 'Работа с популярными датчиками и шинами I2C/SPI.',
        'lessons': [
            {
                'title': 'Датчик температуры DHT11/DHT22',
                'order': 1,
                'estimated_minutes': 15,
                'content': '''<h2>DHT11 / DHT22 — датчик температуры и влажности</h2>
<table>
  <thead><tr><th>Параметр</th><th>DHT11</th><th>DHT22</th></tr></thead>
  <tbody>
    <tr><td>Температура</td><td>0..50 °C ±2°C</td><td>-40..80 °C ±0.5°C</td></tr>
    <tr><td>Влажность</td><td>20-90 % ±5%</td><td>0-100 % ±2-5%</td></tr>
    <tr><td>Интерфейс</td><td colspan="2">1-wire (собственный протокол)</td></tr>
    <tr><td>Питание</td><td colspan="2">3.3-5 В</td></tr>
  </tbody>
</table>
<h3>Подключение</h3>
<ol>
  <li>VCC → 5В (или 3.3В для DHT22)</li>
  <li>DATA → цифровой пин + резистор 10 кОм к VCC</li>
  <li>GND → GND</li>
</ol>
<h3>Библиотека DHT</h3>
<p>Установить через <em>Менеджер библиотек</em>: «DHT sensor library» от Adafruit.</p>''',
                'code_example': '''#include <DHT.h>

#define DHTPIN  2
#define DHTTYPE DHT11  // или DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(2000);  // Датчику нужно 2 сек между измерениями
  float humidity    = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Ошибка чтения DHT!");
    return;
  }
  Serial.print("Влажность: ");  Serial.print(humidity);  Serial.println(" %");
  Serial.print("Температура: "); Serial.print(temperature); Serial.println(" °C");
}''',
            },
            {
                'title': 'Шина I2C — подключение нескольких устройств',
                'order': 2,
                'estimated_minutes': 20,
                'content': '''<h2>Интерфейс I2C</h2>
<p><strong>I2C</strong> (Inter-Integrated Circuit) — двухпроводная шина для связи микроконтроллера с периферией.</p>
<h3>Пины I2C на Arduino Uno</h3>
<ul>
  <li><strong>SDA</strong> — A4 (данные)</li>
  <li><strong>SCL</strong> — A5 (тактовый сигнал)</li>
</ul>
<h3>Особенности</h3>
<ul>
  <li>До 127 устройств на одной шине (у каждого — уникальный 7-битный адрес)</li>
  <li>Скорость: 100 кГц (стандарт) / 400 кГц (Fast Mode)</li>
  <li>Подтягивающие резисторы 4.7 кОм к VCC на SDA и SCL обязательны</li>
</ul>
<h3>Популярные I2C-устройства</h3>
<table>
  <thead><tr><th>Устройство</th><th>Адрес</th><th>Назначение</th></tr></thead>
  <tbody>
    <tr><td>OLED SSD1306</td><td>0x3C</td><td>Дисплей 128×64</td></tr>
    <tr><td>MPU-6050</td><td>0x68</td><td>Акселерометр + гироскоп</td></tr>
    <tr><td>BMP280</td><td>0x76/0x77</td><td>Давление + температура</td></tr>
    <tr><td>PCF8574</td><td>0x20-0x27</td><td>Расширитель GPIO</td></tr>
  </tbody>
</table>''',
                'code_example': '''#include <Wire.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_W  128
#define SCREEN_H   64
#define OLED_ADDR 0x3C

Adafruit_SSD1306 display(SCREEN_W, SCREEN_H, &Wire);

void setup() {
  Serial.begin(9600);
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println("OLED не найден!");
    while (true);
  }
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 20);
  display.println("Hello MCU!");
  display.display();
}

void loop() {}''',
            },
            {
                'title': 'Прерывания',
                'order': 3,
                'estimated_minutes': 15,
                'content': '''<h2>Прерывания (Interrupts)</h2>
<p>Прерывание — механизм немедленной реакции на событие без опроса в loop(). Контроллер приостанавливает основной код, выполняет <strong>ISR</strong> (Interrupt Service Routine), затем возвращается.</p>
<h3>Внешние прерывания на Arduino Uno</h3>
<ul>
  <li>Пин 2 → INT0</li>
  <li>Пин 3 → INT1</li>
</ul>
<h3>Режимы срабатывания</h3>
<ul>
  <li><code>RISING</code> — по нарастающему фронту (0→1)</li>
  <li><code>FALLING</code> — по спадающему фронту (1→0)</li>
  <li><code>CHANGE</code> — по любому изменению</li>
  <li><code>LOW</code> — пока пин LOW</li>
</ul>
<h3>Правила ISR</h3>
<ul>
  <li>Должна быть <strong>максимально короткой</strong> — нельзя использовать delay()</li>
  <li>Переменные, изменяемые в ISR, объявлять <code>volatile</code></li>
  <li>Serial.print() в ISR — нежелательно</li>
</ul>''',
                'code_example': '''volatile int counter = 0;  // volatile — важно!

void onButton() {
  counter++;  // ISR — только счётчик
}

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
  // Прерывание по спадающему фронту (кнопка замыкает на GND)
  attachInterrupt(digitalPinToInterrupt(2), onButton, FALLING);
}

void loop() {
  // Безопасное чтение volatile-переменной
  noInterrupts();
  int count = counter;
  interrupts();

  Serial.print("Нажатий: ");
  Serial.println(count);
  delay(500);
}''',
            },
        ],
    },
    {
        'title': 'ESP32 — WiFi и BLE',
        'icon': 'fas fa-wifi',
        'order': 3,
        'description': 'Подключение к WiFi, веб-сервер, BluetoothLE на ESP32.',
        'lessons': [
            {
                'title': 'Знакомство с ESP32',
                'order': 1,
                'estimated_minutes': 15,
                'content': '''<h2>ESP32 — мощный МК с WiFi и Bluetooth</h2>
<p>ESP32 (Espressif) — двухъядерный 32-битный процессор 240 МГц со встроенными WiFi и BLE. Популярен для IoT-проектов.</p>
<h3>Основные характеристики</h3>
<table>
  <thead><tr><th>Параметр</th><th>Arduino Uno</th><th>ESP32</th></tr></thead>
  <tbody>
    <tr><td>Частота</td><td>16 МГц</td><td>240 МГц (2 ядра)</td></tr>
    <tr><td>Flash</td><td>32 КБ</td><td>4 МБ</td></tr>
    <tr><td>RAM</td><td>2 КБ</td><td>520 КБ</td></tr>
    <tr><td>АЦП</td><td>10 бит</td><td>12 бит (18 каналов)</td></tr>
    <tr><td>WiFi/BT</td><td>Нет</td><td>2.4 ГГц WiFi + BLE 4.2</td></tr>
    <tr><td>Питание</td><td>5 В</td><td>3.3 В (USB 5В через LDO)</td></tr>
  </tbody>
</table>
<h3>Важно: ESP32 — 3.3 В!</h3>
<p>GPIO ESP32 работают на <strong>3.3 В</strong>. Подключение 5В-сигналов требует резисторного делителя или преобразователя уровней.</p>''',
                'code_example': '''// ESP32: аналог Blink
void setup() {
  Serial.begin(115200);
  pinMode(2, OUTPUT);   // Встроенный LED на большинстве плат
  Serial.println("ESP32 запущен!");
}

void loop() {
  digitalWrite(2, HIGH);
  Serial.println("LED вкл");
  delay(1000);
  digitalWrite(2, LOW);
  Serial.println("LED выкл");
  delay(1000);
}''',
            },
            {
                'title': 'Подключение ESP32 к WiFi',
                'order': 2,
                'estimated_minutes': 20,
                'content': '''<h2>WiFi на ESP32</h2>
<p>Библиотека <code>WiFi.h</code> уже включена в ядро ESP32 для Arduino IDE. Не нужно ничего устанавливать отдельно.</p>
<h3>Режимы WiFi</h3>
<ul>
  <li><strong>Station (STA)</strong> — подключается к существующей точке доступа</li>
  <li><strong>Access Point (AP)</strong> — создаёт свою точку доступа</li>
  <li><strong>STA+AP</strong> — оба режима одновременно</li>
</ul>
<h3>Полезные методы</h3>
<ul>
  <li><code>WiFi.begin(ssid, pass)</code> — подключиться</li>
  <li><code>WiFi.status()</code> — <code>WL_CONNECTED</code> если подключено</li>
  <li><code>WiFi.localIP()</code> — получить IP-адрес</li>
  <li><code>WiFi.RSSI()</code> — уровень сигнала (дБм)</li>
</ul>''',
                'code_example': '''#include <WiFi.h>

const char* SSID     = "ИмяСети";
const char* PASSWORD = "пароль";

void setup() {
  Serial.begin(115200);
  WiFi.begin(SSID, PASSWORD);
  Serial.print("Подключение");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi потерян, переподключение...");
    WiFi.reconnect();
    delay(5000);
  }
}''',
            },
        ],
    },
    {
        'title': 'Практические схемы',
        'icon': 'fas fa-project-diagram',
        'order': 4,
        'description': 'Типовые схемы подключения: LED-матрица, сервопривод, UART.',
        'lessons': [
            {
                'title': 'Сервопривод',
                'order': 1,
                'estimated_minutes': 12,
                'content': '''<h2>Сервопривод</h2>
<p>Сервопривод — мотор с обратной связью по положению. Управляется ШИМ-сигналом с периодом <strong>20 мс</strong>:</p>
<ul>
  <li>Импульс 1 мс → 0°</li>
  <li>Импульс 1.5 мс → 90° (центр)</li>
  <li>Импульс 2 мс → 180°</li>
</ul>
<h3>Подключение (SG90)</h3>
<ul>
  <li>Оранжевый/жёлтый → сигнальный пин (с ШИМ)</li>
  <li>Красный → 5 В (отдельный источник при нагрузке!)</li>
  <li>Коричневый/чёрный → GND</li>
</ul>
<p><strong>Важно:</strong> при нескольких сервоприводах или нагрузке — питать от внешнего источника, не от пина Arduino (ток до 500 мА!).</p>''',
                'code_example': '''#include <Servo.h>

Servo myServo;
const int SERVO_PIN = 9;  // Пин с ШИМ

void setup() {
  myServo.attach(SERVO_PIN);
  Serial.begin(9600);
}

void loop() {
  // Плавный поворот 0 → 180 → 0
  for (int angle = 0; angle <= 180; angle += 2) {
    myServo.write(angle);
    delay(15);
  }
  for (int angle = 180; angle >= 0; angle -= 2) {
    myServo.write(angle);
    delay(15);
  }
}''',
            },
            {
                'title': 'UART — последовательный порт',
                'order': 2,
                'estimated_minutes': 12,
                'content': '''<h2>UART — Universal Asynchronous Receiver-Transmitter</h2>
<p>UART — простейший последовательный интерфейс: два провода TX (передача) и RX (приём). Главный инструмент отладки Arduino.</p>
<h3>Пины на Arduino Uno</h3>
<ul>
  <li><strong>TX</strong> → пин 1</li>
  <li><strong>RX</strong> → пин 0</li>
</ul>
<p>Пины 0 и 1 используются для USB-загрузки прошивки. При подключении внешних устройств через UART загрузка прошивки может блокироваться — отключать на время прошивки.</p>
<h3>Типовые скорости (baud rate)</h3>
<p>9600 / 19200 / 57600 / <strong>115200</strong> / 230400 бит/с</p>
<h3>SoftwareSerial</h3>
<p>Для второго UART используют библиотеку <code>SoftwareSerial</code> — эмуляция UART на любых пинах.</p>''',
                'code_example': '''#include <SoftwareSerial.h>

// Второй UART на пинах 10 (RX) и 11 (TX)
SoftwareSerial mySerial(10, 11);

void setup() {
  Serial.begin(9600);      // Основной Serial (USB)
  mySerial.begin(9600);    // Второй Serial
  Serial.println("Готово!");
}

void loop() {
  // Пересылаем данные из второго Serial в первый
  if (mySerial.available()) {
    char c = mySerial.read();
    Serial.write(c);
  }
  // И обратно
  if (Serial.available()) {
    char c = Serial.read();
    mySerial.write(c);
  }
}''',
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Создать теоретические модули раздела Микроконтроллеры'

    def handle(self, *args, **options):
        try:
            mcu = Subject.objects.get(slug='mcu')
        except Subject.DoesNotExist:
            self.stdout.write(self.style.ERROR('Предмет "mcu" не найден. Сначала запустите seed_subjects.'))
            return

        for mod_data in MODULES:
            lessons_data = mod_data.pop('lessons')
            mod, created = TheoryModule.objects.update_or_create(
                title=mod_data['title'],
                subject=mcu,
                defaults={**mod_data, 'subject': mcu, 'is_active': True}
            )
            action = 'Создан' if created else 'Обновлён'
            self.stdout.write(f'{action}: {mod.title}')

            for lesson_data in lessons_data:
                lesson, lc = TheoryLesson.objects.update_or_create(
                    module=mod, order=lesson_data['order'],
                    defaults=lesson_data
                )
                la = 'Создан' if lc else 'Обновлён'
                self.stdout.write(f'  {la}: {lesson.title}')

        self.stdout.write(self.style.SUCCESS('Теория МК готова!'))
