# PastePlain

**Вставка без форматирования.** Скопировал жирный/цветной текст — **Ctrl+Alt+V** вставляет голый текст.

**Автор:** darkshade ([@vlx0](https://github.com/vlx0))

**365 дней open source** · **неделя 3 — «Окна и рабочий стол»** · день 20.

---

## Возможности

- **Ctrl+Alt+V** — вставить буфер как plain text
- Чистит формат (оставляет только текст в буфере и шлёт Ctrl+V)
- Трей

## Установка

```powershell
git clone https://github.com/vlx0/PastePlain.git
cd PastePlain
python -m pip install -r requirements.txt
pythonw run_pasteplain.pyw
```

Или `setup.bat` / `start.bat`.

Нужен Windows 10+ и Python 3.10+.

## Лицензия

MIT. См. [LICENSE](LICENSE).
