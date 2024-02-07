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
- [CREATE_USER](#CREATE_USER)
- [DELETE_USER](#DELETE_USER)
- [GET_TOKEN](#GET_TOKEN)
- [GET_ALL_USERS](#GET_ALL_USERS)
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

## CREATE_USER:
- Назначение: Создать пользователя
- HTTP METHOD: POST
- endpoint: api/auth/users/
- в body обязательно: username, password


## DELETE_USER:
- Назначение: Удалить пользователя
- HTTP METHOD: DELETE
- endpoint: api/auth/users/me


## GET_TOKEN:
- Назначение: Получить аутентификационный токен
- HTTP METHOD: POST
- endpoint: api/auth/token/login/
- в body обязательно: username, password
- ответ: auth_token


## GET_ALL_USERS:
- Назначение: Получить всех пользователей
- HTTP METHOD: GET
- endpoint: api/getUsers
- Доступность: All
- В body обязательно: -
- Особенность: -


## CREATE_SECTION:
- Назначение: Создать секцию
- HTTP METHOD: POST
- endpoint: api/sections/create
- Доступность: Authed
- Роль: TEACHER, MODERATOR
- В body обязательно: title - название секции
- Особенность: невозможно создать две секции с одинаковым названием


## GET_ALL_SECTIONS:
- Назначение: Получить все секции
- HTTP METHOD: GET
- endpoint: api/sections/get
- Доступность: Authed
- Роль: All
- В body обязательно: -
- Особенность: -


## DELETE_SECTION:
- Назначение: Удалить секцию
- HTTP METHOD: DELETE
- endpoint: api/sections/delete
- Доступность: Authed
- Роль: MODERATOR
- В body обязательно: title - название секции
- Особенность: невозможно удалить несуществующую секцию


## JOIN_SECTION:
- Назначение: Записаться в секцию
- HTTP METHOD: POST
- endpoint: api/student/join
- Доступность: Authed
- Роль: STUDENT
- В body обязательно: title - название секции
- Особенность: невозможно присоедениться к секции X, если студент уже состоит в секции X.


## LEAVE_SECTION:
- Назначение: Покинуть секцию
- HTTP METHOD: DELETE
- endpoint: api/student/leave
- Доступность: Authed
- Роль: STUDENT
- В body обязательно: title - название секции
- Особенность: невозможно покинуть секцию, в которой студент не состоит.


## GET_MY_SECTIONS:
- Назначение: Посмотреть список секций, в которые я записан
- HTTP METHOD: GET
- endpoint: api/student/getMySections
- Доступность: Authed
- Роль: STUDENT
- В body обязательно: -
- Особенность: -


## BECOME_TEACHER:
- Назначение: Стать учителем.
- HTTP METHOD: PATCH
- endpoint: api/teacher/leadSection
- Доступность: Authed
- Роль: TEACHER
- В body обязательно: title - название секции
- Особенность: Невозможно стать учителем несуществующей секции. Невозможно стать учителем в секции, в которой уже есть учитель.


## LEAVE_TEACHER_POSITION:
- Назначение: Перестать быть учителем в секции
- HTTP METHOD: PATCH
- endpoint: api/teacher/leaveSection
- Доступность: Authed
- Роль: TEACHER
- В body обязательно: title - название секции
- Особенность: Невозможно перестать быть учителем секции, в которой
ты не являешься учителем. Невозможно перестать быть учителем
несуществующей секции.


## GET_SECTION_STUDENTS:
- Назначение: Получить студентов, записанных в данную секцию
- HTTP METHOD: GET
- endpoint: api/sections/section/getStudents
- Доступность: Authed
- Роль: All
- В body обязательно: title - название секции
- Особенность: -


## GET_STUDENT_SECTIONS:
- Получить секции, в которые записан студент
- HTTP METHOD: GET
- endpoint: api/student/getSections
- Доступность: Authed
- Роль: All
- В body обязательно: -
- Особенность: -
