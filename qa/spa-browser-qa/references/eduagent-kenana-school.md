# eduAgent / Kenana School Platform (mydemo.kenanaschool.com)

Angular (PrimeNG) school-management platform by CODIATOR. Three portals: manager, teacher, student. Same codebase also served at `ed.arishuniversity.com` (landing = marketing site; the app is the same Angular app with a different institution name "كلية التربية").

## Accounts (demo)

| Portal | Username | Password | Notes |
|---|---|---|---|
| Manager (admin) | `amr` | `#01129529648As` | Full admin: SIS, HR, finance, control, CRM, POS — password CHANGED Aug 2026 (old `EDU@#147852547dgsdjghs` is dead) |
| Teacher | `29602151304094` | `Aa000@#` | Portal: basic data, courses, advising, timetable |
| Student | `1234567` | `Ss000@#` | Portal: courses, results, payments, services |

**DATA CHANGES: only when explicitly requested.** Default posture is read-only (client-facing demo), but the user DOES request data maintenance (e.g. Aug 2026: delete all "مستخدم تجريبي/trial user" teachers). Login via API needs the `X-Tenant-Id: mydemo` header + `email` field (not `username`) — see `api-security-probing` skill for the exact pattern. Mass-delete workflow: delete linked `MyApplicationUser` rows first (they FK-block teacher DELETE with 500), then `TimeTables`/`Lectures` rows, then the teacher.

## Login quirk

- Login URL: `https://mydemo.kenanaschool.com/#/login`
- `document.querySelectorAll('input')` returns ~17 — only 2 visible (username + password). Fill via placeholder selectors: `input[placeholder*="اسم المستخدم"]`, `input[placeholder*="كلمة المرور"]`.
- Submit button text: `تسجيل الدخول`. After click it shows `aria-busy="true"` with a spinner — wait 5-8s, then check `location.href` for `#/admin/dashboard`.
- **Use `wait_until="domcontentloaded"` everywhere** — `networkidle` times out (Angular long-polling).
- Manager login lands on a dashboard that ALSO renders the teacher home card (dr. — the manager is a teacher too).

## Route map (manager, prefix `#/`)

- Dashboard: `admin/dashboard`
- Students hub: `admin/coursesSys/students` (list), `admin/coursesSys/students/studentsMenus` (hub), `admin/coursesSys/StudentAffairs`
- Admission: `admin/coursesSys/students/admissionRequests` (NOTE: 0 applicants in demo → weak page)
- Grades/control: `admin/coursesSys/gradesReport`, `totalGradesReport`, `courseStatisticsReport`, `coursesBooksReport` (rich data)
- Attendance: `admin/coursesSys/StudentAffairs/studentAffairsReports/attendanceReport`
- Users: `admin/coursesSys/systemUser`, `userTypes`
- Library: `admin/library/books`
- Accounting: `admin/accounting/sales` (invoices), `debitVoucher` (rich), `creditVoucher`, `gens` (journal, very rich), `accountsTree`, `products`, `salePackages`, `discountRules`, `pos`, `bulkSales`, `financialReports`
- CRM: `admin/crm` (0 leads in demo → weak)
- News: `admin/social/news/manage`
- Metrics: `admin/metrics`
- Settings/backups: `admin/coursesSys/settings/databaseBackups`, `settings/logEntries`

## Course sub-routes (entity id varies, e.g. 3061)

- Teacher: `admin/teacherPortal/teacherCourses/<id>` → `basicInfo`, `lectures`, `courseContent`, `enrolledStudents`, `MonthlyStudentsEvaluation`, `gradingSetup`, `exams`, `assignments`, `reports`, `questionCategories`, `enrollmentsGroups`, `courseSettings`
- Student: `admin/studentPortal/studentCourses/<id>` → `basicInfo`, `lectures`, `courseContent`, `enrolledStudents`, `assignments`, `exams`, `studentsEvaluation`, `reports`

## Working scripts (written during the capture, reusable)

- `/cursor-noise/scripts/kenana_shots2.py` — teacher+student portal screenshot walker (login + route list + viewport + full-page shots)
- `/cursor-noise/scripts/kenana_student_shots.py` — student portal 21-page capture
- `/cursor-noise/scripts/eduagent_manager_shots.py` — manager 26-page capture (route list in SHOTS array)
- `/cursor-noise/scripts/eduagent_crawl.py` — click-every-menu crawl that records URL + text length + snippet into a JSON map (use to classify strong/weak pages BEFORE shooting)

## Data-density findings (which pages are worth shooting)

STRONG (real data): dashboard, students list, books report (24K chars), journal entries (10K), invoices (5.8K), debit vouchers, accounts tree, POS, products, packages, grades reports, library, teacher content (real lessons ألف/باء/تاء), student home (64% progress), exams (real attempts 2/7).
WEAK/EMPTY (skip or RESERVE): admission requests (0 applicants), CRM (0 leads), payments (no transactions), currencies, cost centers, warehouses, purchases, POS terminals, attendance (0 records), monthly evaluations (empty), question bank (0 questions), news, events, leaderboard.

## Warnings-report topics seen in the real demo

- "مستخدم تجريبي" / "منتج تجريبي" / "حمام لاحم" / "سمان" — demo data that looks like a poultry store, not a school → flag for cleanup
- "كلية التربية" branding on the university-origin deploy → confirm school branding before client demo
- Repeated toast "تم تغيير طريقة ترتيب الطلاب" — noise
- University-flavored modules (CGPA, academic advising wording) — check school fit
