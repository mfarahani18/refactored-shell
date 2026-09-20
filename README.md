# 🐚 Python Shell

یک Shell ساده و آموزشی که با زبان **Python** پیاده‌سازی شده است.

هدف اصلی این پروژه، شبیه‌سازی بخشی از رفتار Shellهای رایج مانند Bash و همچنین تمرین مفاهیم مهم برنامه‌نویسی سیستم، پردازش‌ها، مدیریت ورودی/خروجی، Parsing، متغیرها و Command Completion است.

---

## 📌 فهرست مطالب

* [معرفی پروژه](#-معرفی-پروژه)
* [ویژگی‌ها](#-ویژگیهای-پروژه)
* [ساختار کلی Shell](#-ساختار-کلی-shell)
* [نحوه اجرای پروژه](#-نحوه-اجرای-پروژه)
* [چرخه اجرای یک دستور](#-چرخه-اجرای-یک-دستور)
* [کلاس Shell](#-کلاس-shell)
* [دستورات داخلی](#-دستورات-داخلی)
* [اجرای دستورات خارجی](#-اجرای-دستورات-خارجی)
* [Parser](#-parser)
* [متغیرها](#-متغیرها)
* [Redirection](#-redirection)
* [Pipeline](#-pipeline)
* [Background Jobs](#-background-jobs)
* [History](#-history)
* [Autocomplete](#-autocomplete)
* [ساختار داده‌های Shell](#-ساختار-دادههای-shell)
* [نمونه استفاده](#-نمونه-استفاده)
* [مثال‌های کامل](#-مثالهای-کامل)
* [معماری پروژه](#-معماری-پروژه)
* [اصول Refactoring](#-اصول-refactoring)
* [محدودیت‌های پروژه](#-محدودیتهای-پروژه)
* [جمع‌بندی](#-جمع‌بندی)

---

# 🎯 معرفی پروژه

این پروژه یک Shell کوچک است که با Python نوشته شده و کاربر می‌تواند از طریق آن دستورات مختلف را اجرا کند.

Shell وظیفه دارد:

1. ورودی کاربر را دریافت کند.
2. ورودی را Parse کند.
3. متغیرها را Expand کند.
4. نوع دستور را تشخیص دهد.
5. دستور داخلی یا خارجی را اجرا کند.
6. Redirection را مدیریت کند.
7. Pipeline ایجاد کند.
8. Background Process اجرا کند.
9. History دستورات را نگهداری کند.
10. Command و File Completion ارائه دهد.

ساختار اولیه پروژه تمام این مسئولیت‌ها را در کلاس `Shell` متمرکز کرده بود. در نسخه‌ی Refactor شده، بخش‌های بزرگ به متدهای کوچک‌تر تقسیم شده‌اند تا هر متد یک مسئولیت مشخص‌تر داشته باشد.

---

# ✨ ویژگی‌های پروژه

Shell از قابلیت‌های زیر پشتیبانی می‌کند:

* اجرای Built-in Commands
* اجرای External Commands
* `echo`
* `pwd`
* `cd`
* `type`
* `exit`
* `history`
* `declare`
* `complete`
* Background Jobs
* `jobs`
* Pipeline با `|`
* Output Redirection
* Error Redirection
* Append Redirection
* Variable Expansion
* Single Quotes
* Double Quotes
* Escape Character
* Command Completion
* File Completion
* History File
* خواندن و نوشتن History از فایل

لیست Built-inهای Shell در خود کلاس تعریف شده است.

---

# 🚀 نحوه اجرای پروژه

پس از آماده بودن محیط Python، برنامه را اجرا کنید:

```bash
python main.py
```

یا در صورتی که پروژه فایل اجرایی دارد:

```bash
./your_program.sh
```

پس از اجرا، Shell چیزی شبیه زیر نمایش می‌دهد:

```text
$
```

اکنون می‌توان دستورات را وارد کرد:

```bash
$ echo hello
hello
```

---

# 🔄 چرخه اجرای یک دستور

هنگامی که کاربر دستوری وارد می‌کند، Shell تقریباً این مراحل را طی می‌کند:

```text
User Input
    │
    ▼
parse_input()
    │
    ▼
expand_variables()
    │
    ▼
تشخیص نوع دستور
    │
    ├───────────────┐
    │               │
    ▼               ▼
Pipeline          Background
    │               │
    ▼               ▼
run_pipeline()   run_background()
    │
    │
    ▼
Redirection
    │
    ▼
_execute_command()
    │
    ├───────────────┐
    │               │
    ▼               ▼
Builtin          External
    │               │
    ▼               ▼
commands[]       run_not_found()
```

متد `execute_line` نقطه‌ی اصلی اجرای هر خط است. این متد ابتدا ورودی را Parse و سپس متغیرها را Expand می‌کند و بعد بر اساس وجود Pipeline، Background یا Redirection مسیر اجرای مناسب را انتخاب می‌کند.

---

# 🏗 کلاس Shell

هسته اصلی پروژه کلاس:

```python
class Shell:
```

است.

این کلاس وضعیت و رفتار اصلی Shell را نگهداری می‌کند.

---

# 📦 وضعیت داخلی Shell

در زمان ایجاد Shell، چند ساختار داده ساخته می‌شود:

```python
self.completions = {}
self.jobs_data = {}
self.history_data = []
self.last_append_index = 0
self.variables = {}
```

این ساختارها به ترتیب برای موارد زیر استفاده می‌شوند:

| متغیر               | کاربرد                                    |
| ------------------- | ----------------------------------------- |
| `completions`       | نگهداری Completionهای سفارشی              |
| `jobs_data`         | نگهداری Background Jobها                  |
| `history_data`      | نگهداری دستورات History                   |
| `last_append_index` | مشخص کردن آخرین دستور ذخیره‌شده در append |
| `variables`         | نگهداری متغیرهای Shell                    |

این وضعیت‌ها هنگام ساخت شیء `Shell` مقداردهی می‌شوند.

---

# 🧩 Built-in Commands

دستورات داخلی Shell عبارت‌اند از:

```python
builtin_commands = [
    "echo",
    "exit",
    "type",
    "pwd",
    "cd",
    "complete",
    "jobs",
    "history",
    "declare"
]
```

همچنین Shell یک Dictionary برای اتصال نام دستور به متد مربوطه دارد:

```python
self.commands = {
    "exit": self.exit,
    "echo": self.echo,
    "pwd": self.pwd,
    "cd": self.cd,
    "type": self.type,
    "complete": self.complete,
    "jobs": self.jobs,
    "history": self.history,
    "declare": self.declare,
}
```

به این ترتیب به جای استفاده از تعداد زیادی `if/elif` می‌توان متد مناسب را از Dictionary پیدا و اجرا کرد.

---

# 📚 دستورات داخلی

## 1. `echo`

برای نمایش متن استفاده می‌شود.

```bash
echo hello
```

خروجی:

```text
hello
```

چند آرگومان:

```bash
echo hello world
```

خروجی:

```text
hello world
```

پیاده‌سازی:

```python
def echo(self, *args):
    return " ".join(args) + "\n"
```

---

# 2. `pwd`

مسیر فعلی را نمایش می‌دهد.

```bash
pwd
```

مثلاً:

```text
/home/user/shell
```

پیاده‌سازی از `os.getcwd()` استفاده می‌کند.

---

# 3. `cd`

دایرکتوری فعلی را تغییر می‌دهد.

```bash
cd /tmp
```

سپس:

```bash
pwd
```

خروجی:

```text
/tmp
```

همچنین:

```bash
cd ~
```

کاربر را به Home Directory منتقل می‌کند.

---

# 4. `type`

مشخص می‌کند یک دستور Built-in است یا External Command.

مثال:

```bash
type echo
```

خروجی:

```text
echo is a shell builtin
```

برای دستور خارجی:

```bash
type ls
```

مثلاً:

```text
ls is /usr/bin/ls
```

و اگر وجود نداشته باشد:

```bash
type abc
```

خروجی:

```text
abc: not found
```

متد `type` ابتدا Built-inها را بررسی و سپس `PATH` را جستجو می‌کند.

---

# 5. `exit`

Shell را می‌بندد.

```bash
exit
```

قبل از خروج، در صورت وجود `HISTFILE`، History ذخیره می‌شود.

---

# 6. `declare`

برای ایجاد Shell Variable استفاده می‌شود.

مثلاً:

```bash
declare name=Ali
```

سپس:

```bash
echo $name
```

خروجی:

```text
Ali
```

برای مشاهده متغیر:

```bash
declare -p name
```

خروجی:

```text
declare -- name="Ali"
```

نام متغیر باید یک Identifier معتبر باشد.

---

# 7. `history`

نمایش History:

```bash
history
```

مثلاً:

```text
1 echo hello
2 pwd
3 cd /tmp
```

نمایش تعداد مشخصی از دستورات:

```bash
history 3
```

خواندن History از فایل:

```bash
history -r history.txt
```

نوشتن History:

```bash
history -w history.txt
```

Append کردن History:

```bash
history -a history.txt
```

History در `history_data` نگهداری می‌شود.

---

# 8. `complete`

برای تعریف Completion سفارشی استفاده می‌شود.

مثلاً:

```bash
complete -C /path/to/completer mycommand
```

مشاهده Completion:

```bash
complete -p mycommand
```

حذف Completion:

```bash
complete -r mycommand
```

اطلاعات Completion در:

```python
self.completions
```

ذخیره می‌شود.

---

# 🌐 اجرای External Commands

Shell فقط Built-inها را اجرا نمی‌کند.

مثلاً:

```bash
ls
```

یا:

```bash
cat file.txt
```

یا:

```bash
grep hello file.txt
```

برای پیدا کردن برنامه، Shell متد:

```python
find_executable()
```

را اجرا می‌کند.

این متد `PATH` سیستم را بررسی می‌کند و executable مناسب را پیدا می‌کند.

---

# 🔎 `find_executable`

وظیفه:

> پیدا کردن مسیر اجرای یک Command در PATH

مثلاً:

```python
shell.find_executable("ls")
```

ممکن است نتیجه‌ای شبیه این داشته باشد:

```text
/usr/bin/ls
```

اگر پیدا نشود:

```text
None
```

---

# ▶️ `run_not_found`

نام آن در نسخه فعلی کمی گمراه‌کننده است، زیرا علاوه بر مدیریت Commandهای پیدا نشده، اجرای External Command را نیز انجام می‌دهد.

مثلاً:

```bash
ls
```

اگر `ls` پیدا شود، با `subprocess.run()` اجرا می‌شود.

اگر پیدا نشود:

```text
ls: command not found
```

در حالت `capture=True`، خروجی و خطا به صورت Tuple برگردانده می‌شوند.

---

# 🧠 Parser

یکی از مهم‌ترین قسمت‌های Shell:

```python
parse_input()
```

است.

وظیفه آن تبدیل:

```text
echo "hello world"
```

به ساختاری مانند:

```python
[
    "echo",
    "hello world"
]
```

است.

Parser موارد زیر را مدیریت می‌کند:

* Space
* Single Quote
* Double Quote
* Escape Character

---

# Single Quote

مثلاً:

```bash
echo 'hello world'
```

به عنوان یک Argument در نظر گرفته می‌شود:

```text
hello world
```

---

# Double Quote

```bash
echo "hello world"
```

نیز یک Argument محسوب می‌شود.

---

# Escape

مثلاً:

```bash
echo hello\ world
```

باعث می‌شود فاصله بخشی از Argument باشد.

Parser با متغیرهای داخلی زیر وضعیت Parsing را مدیریت می‌کند:

```python
in_single_quotes
in_double_quotes
escape_next
```

این منطق در `parse_input` پیاده‌سازی شده است.

---

# 🔤 Variable Expansion

پس از Parse شدن دستور، Shell متغیرها را Expand می‌کند.

مثلاً:

```bash
declare name=Ali
```

سپس:

```bash
echo Hello $name
```

نتیجه:

```text
Hello Ali
```

همچنین:

```bash
echo ${name}
```

نتیجه:

```text
Ali
```

متد:

```python
expand_variables()
```

با Regular Expression متغیرهای `$name` و `${name}` را پیدا می‌کند.

---

# 📤 Redirection

Shell از Redirectionهای زیر پشتیبانی می‌کند:

| Syntax | عملکرد           |
| ------ | ---------------- |
| `>`    | بازنویسی stdout  |
| `1>`   | بازنویسی stdout  |
| `>>`   | Append به stdout |
| `1>>`  | Append به stdout |
| `2>`   | بازنویسی stderr  |
| `2>>`  | Append به stderr |

---

## `>`

```bash
echo hello > output.txt
```

سپس:

```bash
cat output.txt
```

نتیجه:

```text
hello
```

---

## `>>`

```bash
echo world >> output.txt
```

اکنون:

```bash
cat output.txt
```

نتیجه:

```text
hello
world
```

---

## `2>`

مثلاً:

```bash
ls /not-found 2> error.txt
```

پیغام خطا به جای Terminal داخل فایل قرار می‌گیرد.

---

# معماری Redirection

منطق Redirection به چند متد تقسیم شده است:

```text
_handle_redirection()
        │
        ▼
redirect()
        │
        ├── _run_for_redirection()
        │
        ├── _redirect_stdout()
        │
        └── _redirect_stderr()
```

این تقسیم‌بندی باعث شده متد اصلی `redirect()` مسئولیت‌های کوچک‌تری داشته باشد.

---

# 🔀 Pipeline

Shell از Pipe پشتیبانی می‌کند:

```bash
command1 | command2
```

مثلاً:

```bash
echo hello | cat
```

خروجی:

```text
hello
```

یا:

```bash
echo apple | grep apple
```

---

## Pipeline چندمرحله‌ای

مثلاً:

```bash
cat file.txt | grep apple | wc -l
```

ساختار:

```text
cat
 │
 ▼
grep
 │
 ▼
wc
```

هر Process خروجی خود را به ورودی Process بعدی می‌دهد.

---

# معماری Pipeline

برای تمیزتر شدن کد، Pipeline به چند بخش تقسیم شده است:

```text
run_pipeline()
      │
      ▼
_split_pipeline()
      │
      ├── _run_first_pipeline_command()
      │
      ├── _run_middle_pipeline_command()
      │
      └── _run_last_pipeline_command()
```

متد `run_pipeline` وظیفه هماهنگ کردن این مراحل را دارد و جزئیات اجرای ابتدا، وسط و انتهای Pipeline در متدهای جداگانه قرار گرفته‌اند.

---

# ⚙️ Background Jobs

با اضافه کردن `&` به انتهای دستور، Process در Background اجرا می‌شود.

مثلاً:

```bash
sleep 10 &
```

خروجی:

```text
[1] 12345
```

عدد اول Job ID و عدد دوم Process ID است.

---

# `jobs`

برای مشاهده Jobهای در حال اجرا:

```bash
jobs
```

مثلاً:

```text
[1]+  running                 sleep 10 &
```

---

# Job Reaping

Shell در ابتدای هر iteration متد:

```python
reap_jobs()
```

را اجرا می‌کند.

این متد بررسی می‌کند آیا Process مربوط به Job تمام شده است یا نه.

اگر تمام شده باشد:

```text
[1]+  Done                    sleep 10
```

نمایش داده می‌شود و Job از `jobs_data` حذف می‌شود.

---

# ساختار Job

هر Job تقریباً چنین اطلاعاتی دارد:

```python
{
    "process": process,
    "pid": process.pid,
    "command": original_command,
    "status": "running"
}
```

این اطلاعات داخل:

```python
jobs_data
```

نگهداری می‌شوند.

---

# ⌨️ Autocomplete

Shell از Python `readline` برای Tab Completion استفاده می‌کند.

در `main`:

```python
readline.set_completer(shell.autocomplete)
```

تابع `autocomplete` هنگام فشردن Tab فراخوانی می‌شود.

---

# Command Completion

مثلاً کاربر بنویسد:

```text
ec
```

و Tab بزند.

Shell می‌تواند:

```text
echo
```

را پیشنهاد دهد.

---

# File Completion

مثلاً:

```text
cat tes
```

با Tab می‌تواند فایل‌هایی که با:

```text
tes
```

شروع می‌شوند را پیدا کند.

---

# Path Completion

اگر ورودی شامل `/` باشد:

```text
cat /tmp/tes
```

Shell وارد منطق:

```python
find_file_by_path()
```

می‌شود.

---

# Custom Completion

Shell همچنین از Completionهای سفارشی پشتیبانی می‌کند.

اطلاعات آن در:

```python
self.completions
```

قرار دارد.

اگر برای Command موردنظر Completion تعریف شده باشد، Shell برنامه Completion را اجرا کرده و خروجی آن را به عنوان گزینه‌های Completion استفاده می‌کند.

---

# 🧾 History

History در:

```python
history_data
```

ذخیره می‌شود.

مثلاً:

```python
[
    "pwd",
    "echo hello",
    "cd /tmp"
]
```

---

# HISTFILE

اگر Environment Variable زیر تعریف شده باشد:

```bash
export HISTFILE=/tmp/my_history
```

Shell هنگام شروع، History را از این فایل می‌خواند.

هنگام خروج نیز History را در آن ذخیره می‌کند.

---

# History Flags

## خواندن فایل

```bash
history -r history.txt
```

## نوشتن

```bash
history -w history.txt
```

## Append

```bash
history -a history.txt
```

## نمایش N دستور آخر

```bash
history 5
```

---

# 🧱 ساختار منطقی کلاس Shell

اگر متدها را بر اساس مسئولیت دسته‌بندی کنیم:

```text
Shell
│
├── Main Execution
│   ├── run
│   ├── execute_line
│   └── _execute_command
│
├── Parsing
│   └── parse_input
│
├── Variables
│   ├── declare
│   └── expand_variables
│
├── Built-in Commands
│   ├── echo
│   ├── pwd
│   ├── cd
│   ├── type
│   └── exit
│
├── External Commands
│   ├── find_executable
│   └── run_not_found
│
├── Redirection
│   ├── _handle_redirection
│   ├── redirect
│   ├── _run_for_redirection
│   ├── _redirect_stdout
│   └── _redirect_stderr
│
├── Pipeline
│   ├── run_pipeline
│   ├── _split_pipeline
│   ├── _run_first_pipeline_command
│   ├── _run_middle_pipeline_command
│   └── _run_last_pipeline_command
│
├── Jobs
│   ├── run_background
│   ├── reap_jobs
│   ├── jobs
│   ├── _job_marker
│   ├── _print_running_job
│   └── print_done_job
│
├── History
│   ├── _load_history
│   ├── history
│   ├── _print_full_history
│   ├── _read_history_file
│   ├── _write_history_file
│   ├── _append_history_file
│   └── _print_recent_history
│
└── Autocomplete
    ├── find_matches
    ├── _find_argument_matches
    ├── _find_command_matches
    ├── autocomplete
    ├── _run_custom_completion
    ├── display_matches
    ├── find_entry_by_prefix
    └── find_file_by_path
```

این ساختار یکی از نتایج اصلی Refactoring پروژه است: متدهای بزرگ‌تر به Helper Methodهای کوچک‌تر تقسیم شده‌اند. برای نمونه، History دیگر تمام عملیات فایل و نمایش را در یک متد انجام نمی‌دهد.

---

# 🧪 نمونه‌های کاربردی

## مثال 1 — Echo

```bash
$ echo Hello
Hello
```

---

## مثال 2 — Directory

```bash
$ pwd
/home/user/shell

$ cd /tmp

$ pwd
/tmp
```

---

## مثال 3 — Variable

```bash
$ declare username=Ali

$ echo Hello $username
Hello Ali
```

---

## مثال 4 — Redirect

```bash
$ echo Hello > hello.txt

$ cat hello.txt
Hello
```

---

## مثال 5 — Append

```bash
$ echo One > file.txt

$ echo Two >> file.txt

$ cat file.txt
One
Two
```

---

## مثال 6 — Pipeline

```bash
$ echo hello | cat
hello
```

---

## مثال 7 — Background

```bash
$ sleep 5 &
[1] 12345

$ jobs
[1]+  running                 sleep 5 &
```

---

## مثال 8 — History

```bash
$ echo one
one

$ echo two
two

$ history
1 echo one
2 echo two
3 history
```

---

# 🧠 اصول Refactoring استفاده‌شده

هدف Refactoring این پروژه تغییر رفتار Shell نیست.

هدف اصلی:

> حفظ رفتار موجود و کاهش پیچیدگی کد.

مهم‌ترین تغییرات ساختاری عبارت‌اند از:

### 1. تقسیم متدهای بزرگ

به جای یک متد بسیار بزرگ، عملیات به Helper Methodهای کوچک‌تر تقسیم شده است.

مثلاً:

```python
redirect()
```

از متدهای:

```python
_run_for_redirection()
_redirect_stdout()
_redirect_stderr()
```

استفاده می‌کند.

---

### 2. جداسازی مسئولیت‌ها

مثلاً History به بخش‌های زیر تقسیم شده:

```text
_print_full_history()
_read_history_file()
_write_history_file()
_append_history_file()
_print_recent_history()
```

---

### 3. Pipeline به مراحل مختلف تقسیم شده

به جای قرار دادن تمام منطق Pipeline در یک متد:

```text
first
middle
last
```

جدا شده‌اند.

---

### 4. استفاده از Command Registry

به جای:

```python
if command == "echo":
    ...
elif command == "pwd":
    ...
elif command == "cd":
    ...
```

از Dictionary استفاده شده:

```python
self.commands = {
    "echo": self.echo,
    "pwd": self.pwd,
    "cd": self.cd,
}
```

---

# 📐 معماری کلی پروژه

```text
                    ┌──────────────┐
                    │     User     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │     Shell    │
                    └──────┬───────┘
                           │
                    execute_line()
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
          ▼                ▼                 ▼
       Parser          Variables         Detection
          │                │                 │
          └────────────────┼─────────────────┘
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
          ▼                ▼                 ▼
      Built-in         Pipeline          Background
          │                │                 │
          ▼                ▼                 ▼
      Commands        subprocess          Jobs
          │
          ├───────────────┐
          ▼               ▼
     Redirection      External Commands
          │               │
          ▼               ▼
        Files          PATH / Process
```

---

# 🔧 فایل‌های اصلی

ساختار ساده پروژه:

```text
project/
│
├── main.py
│
├── app/
│   ├── __init__.py
│   └── shell.py
│
├── README.md
│
└── your_program.sh
```

---

# 🧩 نقش `main.py`

`main.py` وظیفه‌ی اصلی اجرای Shell را بر عهده دارد.

وظایف آن شامل:

1. ساخت Object از `Shell`
2. تنظیم `readline`
3. اتصال autocomplete
4. اتصال نمایش Completion
5. شروع حلقه Shell

نمونه:

```python
shell = Shell()

readline.set_completer(shell.autocomplete)
readline.parse_and_bind("tab: complete")
```

به این ترتیب `main.py` بیشتر نقش **Entry Point** برنامه را دارد و منطق اصلی Shell داخل کلاس `Shell` قرار گرفته است.

---

# 🔄 ارتباط main.py و Shell

```text
main.py
   │
   │ creates
   ▼
Shell()
   │
   ├── autocomplete
   ├── display_matches
   ├── run
   └── execute_line
           │
           ├── parse
           ├── expand
           ├── pipeline
           ├── background
           ├── redirect
           └── command
```

---

# ⚠️ نکات مهم

این پروژه یک Shell آموزشی است و هدف آن پیاده‌سازی کامل Bash نیست.

بنابراین برخی رفتارهای پیشرفته Bash ممکن است پشتیبانی نشوند.

از جمله قابلیت‌های پیچیده‌ای مانند:

* Advanced Job Control
* `&&`
* `||`
* Subshell
* Command Substitution
* Wildcard Expansion
* Function Definition
* Advanced Signal Handling
* Full POSIX Parsing
* پیچیدگی‌های کامل Quoting

در محدوده پروژه قرار ندارند مگر اینکه به صورت جداگانه پیاده‌سازی شوند.

---

# 🧪 پیشنهاد برای تست پروژه

برای تست قابلیت‌های اصلی، این دستورات را اجرا کنید:

```bash
echo hello

pwd

cd /tmp

pwd

declare name=Ali

echo Hello $name

echo "hello world"

echo hello > test.txt

echo world >> test.txt

cat test.txt

echo hello | cat

sleep 5 &

jobs

history
```

---

# 📊 خلاصه قابلیت‌ها

| قابلیت             | متد اصلی                   |
| ------------------ | -------------------------- |
| اجرای Shell        | `run()`                    |
| اجرای خط           | `execute_line()`           |
| اجرای Built-in     | `_execute_command()`       |
| Parsing            | `parse_input()`            |
| Variable Expansion | `expand_variables()`       |
| `echo`             | `echo()`                   |
| `pwd`              | `pwd()`                    |
| `cd`               | `cd()`                     |
| `type`             | `type()`                   |
| `exit`             | `exit()`                   |
| `declare`          | `declare()`                |
| History            | `history()`                |
| Background         | `run_background()`         |
| Jobs               | `jobs()`                   |
| Reaping            | `reap_jobs()`              |
| Redirection        | `redirect()`               |
| Pipeline           | `run_pipeline()`           |
| External Command   | `run_not_found()`          |
| Executable Search  | `find_executable()`        |
| Autocomplete       | `autocomplete()`           |
| Custom Completion  | `_run_custom_completion()` |

---

# 🎓 اهداف آموزشی پروژه

این پروژه علاوه بر ساخت یک Shell ساده، مفاهیم مهم زیر را تمرین می‌کند:

### Python

* Class
* Object
* Method
* Dictionary
* List
* Exception Handling
* Regular Expression
* File Handling
* Type Hinting

### سیستم‌عامل

* Process
* PID
* `PATH`
* stdin
* stdout
* stderr
* Pipe
* File Descriptor
* Background Process

### Software Engineering

* Refactoring
* Separation of Responsibilities
* Helper Methods
* کاهش پیچیدگی
* Command Dispatch
* Modular Design
* خوانایی کد
* نگهداری آسان‌تر

---

# 🚀 مسیر توسعه آینده

در مراحل بعدی می‌توان معماری پروژه را یک مرحله دیگر نیز توسعه داد.

برای مثال می‌توان مسئولیت‌های فعلی `Shell` را به کلاس‌های مستقل تقسیم کرد:

```text
Shell
│
├── Parser
├── CommandRegistry
├── BuiltinCommand
├── ExternalCommand
├── HistoryManager
├── JobManager
├── PipelineExecutor
├── RedirectionManager
└── CompletionManager
```

در این حالت کلاس `Shell` بیشتر نقش هماهنگ‌کننده را خواهد داشت.

این معماری برای مرحله بعدی Refactoring پروژه، مخصوصاً برای تمرین مفاهیم **Inheritance، Composition و Polymorphism** مناسب است.

---

# 🏁 جمع‌بندی

این پروژه یک Shell آموزشی است که طیف قابل توجهی از قابلیت‌های اصلی Shell را با Python پیاده‌سازی می‌کند.

معماری فعلی تلاش می‌کند منطق را به بخش‌های کوچک‌تر تقسیم کند و در عین حفظ رفتار برنامه، خوانایی و قابلیت نگهداری کد را افزایش دهد.

مهم‌ترین بخش‌های پروژه عبارت‌اند از:

```text
Input
  ↓
Parser
  ↓
Variable Expansion
  ↓
Command Detection
  ↓
┌──────────┬───────────┬─────────────┬──────────────┐
│ Built-in │ External  │ Pipeline    │ Background   │
│ Command  │ Command   │             │ Job          │
└──────────┴───────────┴─────────────┴──────────────┘
  ↓
Redirection / Process Management
  ↓
Output
```

هدف نهایی پروژه فقط اجرای چند دستور نیست؛ بلکه ساخت یک نمونه عملی برای یادگیری **Parsing، Process Management، I/O، Refactoring و طراحی نرم‌افزار** است.


## نصب و اجرای پروژه

### پیش‌نیازها

برای اجرای این پروژه به موارد زیر نیاز دارید:

* Python 3.10 یا بالاتر
* Git
* یک محیط Linux / macOS / WSL
* در صورت اجرای تست‌های CodeCrafters، حساب CodeCrafters و CLI مربوط به آن

نسخه‌ی Python را بررسی کنید:

```bash
python3 --version
```

خروجی باید چیزی مشابه زیر باشد:

```text
Python 3.11.9
```

---

## دریافت پروژه

اگر پروژه را از Git دریافت می‌کنید:

```bash
git clone <repository-url>
cd <project-directory>
```

سپس ساختار پروژه را بررسی کنید:

```bash
tree
```

ساختار کلی پروژه باید مشابه این باشد:

```text
.
├── app/
│   ├── __init__.py
│   ├── shell.py
│   └── ...
├── main.py
├── your_program.sh
├── README.md
└── ...
```

---

## اجرای Shell

### اجرای مستقیم با Python

برای اجرای Shell:

```bash
python3 main.py
```

پس از اجرا باید prompt زیر را مشاهده کنید:

```text
$
```

اکنون می‌توانید دستورات Shell را وارد کنید:

```text
$ echo hello
hello
```

برای خروج:

```text
$ exit
```

---

## اجرای برنامه با `your_program.sh`

در پروژه‌های CodeCrafters معمولاً برنامه از طریق فایل زیر اجرا می‌شود:

```text
your_program.sh
```

ابتدا مطمئن شوید فایل executable است:

```bash
chmod +x your_program.sh
```

سپس:

```bash
./your_program.sh
```

باید prompt زیر نمایش داده شود:

```text
$
```

مثلاً:

```text
$ echo hello
hello
$ pwd
/home/user/shell
$ exit
```

---

# تست دستی قابلیت‌ها

قبل از اجرای تست‌های رسمی، بهتر است قابلیت‌های اصلی Shell را به صورت دستی بررسی کنید.

## 1. دستور `echo`

```text
$ echo hello
hello
```

چند آرگومان:

```text
$ echo hello world
hello world
```

با quote:

```text
$ echo "hello world"
hello world
```

---

## 2. دستور `pwd`

```text
$ pwd
/home/user/shell
```

---

## 3. دستور `cd`

ورود به یک directory:

```text
$ cd /tmp
$ pwd
/tmp
```

استفاده از `~`:

```text
$ cd ~
$ pwd
/home/user
```

---

## 4. دستور `type`

برای بررسی Built-in:

```text
$ type echo
echo is a shell builtin
```

برای یک executable:

```text
$ type ls
ls is /usr/bin/ls
```

برای دستور ناشناخته:

```text
$ type something
something: not found
```

---

## 5. اجرای دستورات خارجی

مثلاً:

```text
$ ls
```

یا:

```text
$ cat file.txt
```

یا:

```text
$ printf "hello\n"
hello
```

---

# تست Variable Expansion

تعریف متغیر:

```text
$ declare NAME=Ali
```

استفاده از متغیر:

```text
$ echo $NAME
Ali
```

استفاده با `${...}`:

```text
$ echo ${NAME}
Ali
```

متغیر تعریف‌نشده:

```text
$ echo $UNKNOWN

```

---

# تست Redirection

### خروجی با `>`

```text
$ echo hello > output.txt
```

بررسی فایل:

```text
$ cat output.txt
hello
```

### Append با `>>`

```text
$ echo world >> output.txt
```

نتیجه:

```text
$ cat output.txt
hello
world
```

### Redirect کردن stderr

```text
$ some-invalid-command 2> error.txt
```

سپس:

```text
$ cat error.txt
```

---

# تست Pipeline

یک pipeline ساده:

```text
$ echo hello | wc -c
6
```

چند مرحله‌ای:

```text
$ echo hello world | tr " " "\n" | wc -l
2
```

---

# تست Background Jobs

اجرای یک دستور در background:

```text
$ sleep 5 &
```

نمایش Jobها:

```text
$ jobs
```

پس از پایان Job، Shell باید بتواند وضعیت آن را تشخیص دهد.

---

# تست History

چند دستور اجرا کنید:

```text
$ echo apple
apple
$ echo banana
banana
$ echo orange
orange
```

سپس:

```text
$ history
```

باید دستورات قبلی نمایش داده شوند.

همچنین می‌توان با کلید `↑` بین دستورات قبلی حرکت کرد.

---

# تست Tab Completion

برای تست completion ابتدا بخشی از یک دستور را وارد کنید:

```text
$ ec<TAB>
```

در صورت وجود completion مناسب، Shell باید بتواند آن را کامل کند.

برای executableها نیز:

```text
$ pyt<TAB>
```

و برای مسیر فایل‌ها:

```text
$ cat /us<TAB>
```

completion باید بر اساس فایل‌ها و directoryهای موجود عمل کند.

---

# اجرای تست‌های پروژه

اگر پروژه دارای تست‌های Python باشد، ابتدا بررسی کنید آیا فایل‌های تست وجود دارند:

```bash
find . -maxdepth 2 -type f | sort
```

در صورت وجود `pytest` و فایل‌های تست، می‌توانید آن‌ها را با:

```bash
python3 -m pytest
```

اجرا کنید.

برای نمایش جزئیات بیشتر:

```bash
python3 -m pytest -v
```

---

# تست با CodeCrafters

این پروژه برای پیاده‌سازی Shell در محیط CodeCrafters طراحی شده است.

برای اجرای تست‌های CodeCrafters، برنامه باید از طریق:

```bash
./your_program.sh
```

قابل اجرا باشد.

ابتدا:

```bash
chmod +x your_program.sh
```

سپس تست‌های مرحله‌ی فعلی CodeCrafters را اجرا کنید.

در محیط CodeCrafters معمولاً خروجی تست چیزی شبیه این است:

```text
[compile] Compilation successful.
[tester::#XXXX] Running tests for Stage #XXXX
[your-program] $ echo hello
[your-program] hello
[tester::#XXXX] ✓ Command executed successfully
```

اگر تست موفق باشد، در خروجی علامت:

```text
✓
```

مشاهده می‌شود.

---

# بررسی خطاهای رایج

## `Permission denied`

اگر هنگام اجرای:

```bash
./your_program.sh
```

خطای زیر را دیدید:

```text
Permission denied
```

اجازه‌ی اجرا بدهید:

```bash
chmod +x your_program.sh
```

سپس دوباره:

```bash
./your_program.sh
```

---

## `python3: command not found`

نسخه‌ی Python را بررسی کنید:

```bash
python3 --version
```

اگر Python نصب نیست، باید آن را برای سیستم‌عامل خود نصب کنید.

---

## برنامه اجرا نمی‌شود

ابتدا مستقیماً با Python اجرا کنید:

```bash
python3 main.py
```

اگر این روش کار کرد ولی:

```bash
./your_program.sh
```

کار نکرد، محتویات `your_program.sh` را بررسی کنید.

یک wrapper معمولی می‌تواند چیزی شبیه این باشد:

```bash
#!/bin/sh
exec python3 main.py
```

و سپس:

```bash
chmod +x your_program.sh
```

---

# تست سریع Smoke Test

برای یک بررسی سریع بعد از هر تغییر در کد، این سناریو را اجرا کنید:

```text
$ echo hello
hello

$ pwd
/home/user/shell

$ type echo
echo is a shell builtin

$ declare NAME=Ali

$ echo $NAME
Ali

$ echo hello > test.txt

$ cat test.txt
hello

$ echo world >> test.txt

$ cat test.txt
hello
world

$ echo hello | wc -c
6

$ sleep 2 &

$ jobs

$ history

$ exit
```

اگر این سناریو بدون خطای غیرمنتظره اجرا شود، بخش بزرگی از قابلیت‌های اصلی Shell به صورت دستی بررسی شده است.

> توجه: خروجی دقیق بعضی دستورات مانند `pwd`، `jobs` و `history` به محیط اجرا و وضعیت فعلی Shell بستگی دارد؛ بنابراین در تست دستی نباید صرفاً خروجی ثابت مثال بالا را ملاک قرار داد.
