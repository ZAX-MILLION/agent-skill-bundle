# Kenana School demo (mydemo.kenanaschool.com) — screenshot specifics

Angular SPA (hash routing), Arabic UI, teacher portal. Used as the bulk-capture + data-density example for spa-browser-qa Phase 5.

## Login
- URL: `https://mydemo.kenanaschool.com/#/login`
- Form: two `input` boxes (username, password) — fill via `page.locator("input")` nth(0)/nth(1).
- The submit button (`button.login-card__submit`) shows `aria-busy=true` + spinner while authenticating; a plain `.click()` or Enter may not fire it — click via JS `btn.click()` if the form seems stuck, then wait ~5s for the hash-route redirect to `#/admin/dashboard`.
- Login succeeds → URL becomes `#/admin/dashboard`.

## Route map (teacher portal, course id 3061 = اللغة العربية)
```
#/admin/dashboard                                    teacher home (S01)
#/admin/teacherPortal/teacherCourses                 my courses (S02)
#/admin/teacherPortal/teacherStudents                advising students
#/admin/teacherPortal/teacherTimeTable               timetable
#/admin/teacherPortal/teacherBooks                   books
#/admin/teacherPortal/basicData                      basic data
#/admin/teacherPortal/teacherCourses/3061            course dashboard (S03)
#/admin/teacherPortal/teacherCourses/3061/basicInfo
#/admin/teacherPortal/teacherCourses/3061/lectures              attendance (S04b)
#/admin/teacherPortal/teacherCourses/3061/courseContent         content (S04)
#/admin/teacherPortal/teacherCourses/3061/enrolledStudents      students (S05)
#/admin/teacherPortal/teacherCourses/3061/MonthlyStudentsEvaluation  monthly grades (S09)
#/admin/teacherPortal/teacherCourses/3061/gradingSetup          assessment config (S08)
#/admin/teacherPortal/teacherCourses/3061/exams                 exams (S07)
#/admin/teacherPortal/teacherCourses/3061/assignments           assignments (S06)
#/admin/teacherPortal/teacherCourses/3061/reports               reports (S10)
#/admin/teacherPortal/teacherCourses/3061/questionCategories    question bank (S07b)
#/admin/teacherPortal/teacherCourses/3061/enrollmentsGroups
#/admin/teacherPortal/teacherCourses/3061/courseSettings
```
Course cards on the dashboard are `<button class="timetable-course-card">` — clicking navigates to `teacherCourses/<id>`. Discover the id by clicking the first card and reading `location.href`.

## Data status observed (2026-08-02)
- Filled: course content (units/lessons for حروف الأبجدية), 2 assignments (due dates, 10 pts), 1 exam (5 min, 7 questions, closed), 1 lecture, 2 enrolled students (KG1, القسم العربي), 1 question bank (0 questions).
- Empty/zero: dashboard advising students=0, classes today=0, progress=blank; grading setup "لا توجد تقييمات افتراضية"; question bank 0 questions; monthly-evaluations page is just a month picker with no grid; no attendance records; no assignment submissions.
- Arabic empty markers to grep for: `لا توجد`, `لا يوجد`, `لا تتوفر`, `لا توجد بيانات`, `لا توجد مهام`, `لا توجد اختبارات`.

## Working scripts (kept under /cursor-noise/scripts/)
- `kenana_shots2.py` — login + capture all routes (viewport + full_page)
- `kenana_check.py` — per-page text dump + empty-marker detection (data-density check)
- `kenana_deep.py` — deep-check specific pages (table/input counts, full text)
- Output: `/cursor-noise/screenshots/kenana/S*.png`

User requirement for this job: screenshots must show FILLED data, not zeros — deliver the honest current state with a gaps table, then offer enrichment (A: agent fills demo data via UI + re-shoot, B: user fills + re-shoot, C: ship as-is).

## Student portal (second phase — separate account)

The user then switches to the STUDENT portal with a different account — same site, different role view. Flow: they post a numbered screenshot plan (in Arabic, often 15-25 pages with a priority list at the end); map each requirement to a route, capture ALL, deliver the top-priority ones as MEDIA, keep the rest in the folder, report data status per page.

### Login
- User `1234567` / `Ss000@#` → same login form → `#/admin/dashboard` (student = ماسة احمد السيد, KG1).
- ⚠️ The browser-tool manual form fill can silently fail (stale form state after a previous login); the Playwright script login works every time (fresh context). If the manual attempt stays on `#/login` with no error, don't fight it — use the Playwright script for capture.

### Route map (student portal, same course id 3061)
```
#/admin/dashboard                                    student home (P01)
#/admin/studentPortal/studentCourses                 courses list (P02)
#/admin/studentPortal/studentCourses/3061            course dashboard (P03)
#/admin/studentPortal/studentCourses/3061/courseContent   content (P04)
#/admin/studentPortal/studentCourses/3061/assignments      assignments (P05)
#/admin/studentPortal/studentCourses/3061/exams            exams (P06)
#/admin/studentPortal/studentTimeTable               timetable (P07)
#/admin/studentPortal/studentResultsInPortal         results (P08)
#/admin/studentPortal/academicHistory                academic status (P09)
#/admin/studentPortal/studentPayments                payments (P10)
#/studentServices                                    e-services (P11)
#/admin/studentPortal/basicData                      basic data (P12)
#/admin/studentPortal/studentCourses/3061/basicInfo
#/admin/studentPortal/studentCourses/3061/lectures
#/admin/studentPortal/studentCourses/3061/enrolledStudents  classmates
#/admin/studentPortal/studentCourses/3061/studentsEvaluation  grades
#/admin/studentPortal/studentCourses/3061/reports
#/admin/studentPortal/studentExamEvents              exam schedule
#/home/news                                          news
#/admin/studentPortal/studentBooks                   books
```
Entry buttons are `<button>` with text `لوحة المقرر` (not links) — click via `page.locator("button:has-text('لوحة المقرر')").first.click()` then read `page.url` for the course id. Assignment detail: click the assignment card (`div:has-text('تكليف 1')`) — captures the detail/answer view.

### Student data status observed (2026-08-02)
- Filled: home (welcome + 2 courses + 64% progress), results, grades (exam attempt 1/5 recorded), academic status (GPA calc, hours), exams (real exam, 2/7 attempts), content (same lessons as teacher side).
- Empty/zero: payments ("لا توجد مدفوعات"), attendance 0%, upcoming exam none, assignments not submitted.
- Student portal data is generally BETTER than teacher portal — most priority pages are presentable as-is.

### Scripts (student phase)
- `kenana_student_shots.py` — login + all P01-P20 routes + assignment detail click
- `kenana_student_check.py` — per-page empty-marker verification
- Output: `/cursor-noise/screenshots/kenana/student/P*.png`
