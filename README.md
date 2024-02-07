# Перед запуском
Прежде чем запускать проект, нужно указать подключение к базе данных в settings.py
Используется Postgres
Необходимо указать Name, User, Password, Host, Port


# Таблицы в проекте:

- ApiUser (Пользователь) - встроенная модель django плюс поле role
- Section (Секция) - поля: title, teacher
- UserSection (Пользователь-секция) - поля: student, section, date


# Роли:
- ApiUser.Role.MODERATOR - Модератор (создает секции)
- ApiUser.Role.STUDENT - Студент (состоит в секции)
- ApiUser.Role.TEACHER - Преподаватель (заведует секцией)

Можно выбрать одну из трех ролей при регистрации, но изменить её в дальнейшем невозможно.
Невозможно зарегистрировать пользователя не указав поле role


# API Методы:
- [CREATE_SECTION](#CREATE_SECTION)
- [GET_ALL_SECTIONS](#GET_ALL_SECTIONS)
- [DELETE_SECTION](#DELETE_SECTION)
- [JOIN_SECTION](#JOIN_SECTION)
- [LEAVE_SECTION](#LEAVE_SECTION)
- [GET_MY_SECTIONS](#GET_MY_SECTIONS)
- [BECOME_TEACHER](#BECOME_TEACHER)
- [LEAVE_TEACHER_POSITION](#LEAVE_TEACHER_POSITION)
- [GET_SECTION_STUDENTS](#GET_SECTION_STUDENTS)
- [GET_STUDENT_SECTIONS](#GET_STUDENT_SECTIONS)

## CREATE_SECTION:
- __Назначение__: Создать секцию
- __HTTP METHOD__: POST
- __endpoint__: api/sections/create
- __Доступность__: Authed
- __Роль__: TEACHER, MODERATOR
- __В body обязательно__: title - название секции
- __Особенность__: невозможно создать две секции с одинаковым названием


## GET_ALL_SECTIONS:
- __Назначение__: Получить все секции
- __HTTP METHOD__: GET
- __endpoint__: api/sections/get
- __Доступность__: Authed
- __Роль__: All
- __В body обязательно__: -
- __Особенность__: -


## DELETE_SECTION:
- __Назначение__: Удалить секцию
- __HTTP METHOD__: DELETE
- __endpoint__: api/sections/delete
- __Доступность__: Authed
- __Роль__: MODERATOR
- __В body обязательно__: title - название секции
- __Особенность__: невозможно удалить несуществующую секцию


## JOIN_SECTION:
- __Назначение__: Записаться в секцию
- __HTTP METHOD__: POST
- __endpoint__: api/student/join
- __Доступность__: Authed
- __Роль__: STUDENT
- __В body обязательно__: title - название секции
- __Особенность__: невозможно присоедениться к секции X, если студент уже состоит в секции X.


## LEAVE_SECTION:
- __Назначение__: Покинуть секцию
- __HTTP METHOD__: DELETE
- __endpoint__: api/student/leave
- __Доступность__: Authed
- __Роль__: STUDENT
- __В body обязательно__: title - название секции
- __Особенность__: невозможно покинуть секцию, в которой студент не состоит.


## GET_MY_SECTIONS:
- __Назначение__: Посмотреть список секций, в которые я записан
- __HTTP METHOD__: GET
- __endpoint__: api/student/getMySections
- __Доступность__: Authed
- __Роль__: STUDENT
- __В body обязательно__: -
- __Особенность__: -


## BECOME_TEACHER:
- __Назначение__: Стать учителем.
- __HTTP METHOD__: PATCH
- __endpoint__: api/teacher/leadSection
- __Доступность__: Authed
- __Роль__: TEACHER
- __В body обязательно__: title - название секции
- __Особенность__: Невозможно стать учителем несуществующей секции. Невозможно стать учителем в секции, в которой уже есть учитель.


## LEAVE_TEACHER_POSITION:
- __Назначение__: Перестать быть учителем в секции
- __HTTP METHOD__: PATCH
- __endpoint__: api/teacher/leaveSection
- __Доступность__: Authed
- __Роль__: TEACHER
- __В body обязательно__: title - название секции
- __Особенность__: Невозможно перестать быть учителем секции, в которой
ты не являешься учителем. Невозможно перестать быть учителем
несуществующей секции.


## GET_SECTION_STUDENTS:
- __Назначение__: Получить студентов, записанных в данную секцию
- __HTTP METHOD__: GET
- __endpoint__: api/sections/section/getStudents
- __Доступность__: Authed
- __Роль__: All
- __В body обязательно__: title - название секции
- __Особенность__: -


## GET_STUDENT_SECTIONS:
- __Назначение__: Получить секции, в которые записан студент
- __HTTP METHOD__: GET
- __endpoint__: api/student/getSections
- __Доступность__: Authed
- __Роль__: All
- __В body обязательно__: -
- __Особенность__: -
