"""
Автоматически тестирует ПР студентов по тест-кейсам.
Запуск: python manage.py run_autotests --work_id=1
"""
import json, os, sys
from django.core.management.base import BaseCommand
from works.models import PracticalWork, Solution
from works.code_runner import run_python_code


class Command(BaseCommand):
    help = "Запускает автотесты для решений студентов"

    def add_arguments(self, parser):
        parser.add_argument("--work_id", type=int, default=None)
        parser.add_argument("--solution_id", type=int, default=None)

    def handle(self, *args, **options):
        tests_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "test_data", "auto_tests.json"
        )
        if not os.path.exists(tests_path):
            self.stdout.write(self.style.ERROR("auto_tests.json не найден"))
            return

        with open(tests_path, encoding="utf-8") as f:
            all_tests = json.load(f)

        work_id = options.get("work_id")
        sol_id  = options.get("solution_id")

        solutions = Solution.objects.filter(status="submitted")
        if work_id:
            solutions = solutions.filter(work_id=work_id)
        if sol_id:
            solutions = solutions.filter(id=sol_id)

        for sol in solutions:
            work_tests = all_tests.get(str(sol.work.order))
            if not work_tests:
                continue

            code_path = sol.code_file.path if sol.code_file else None
            if not code_path or not os.path.exists(code_path):
                continue

            with open(code_path, encoding="utf-8", errors="replace") as f:
                code = f.read()

            passed = 0
            for test in work_tests:
                result = run_python_code(code, input_data=test["input"])
                actual = (result.get("output") or "").strip()
                if test["expected"].strip() in actual:
                    passed += 1

            score = round(passed * 100 / len(work_tests))
            status = "correct" if score >= 70 else "partially_correct" if score >= 40 else "incorrect"
            sol.score = round(passed * sol.work.max_score / len(work_tests))
            sol.status = status
            sol.save()
            self.stdout.write(f"  {sol.student.last_name}: {passed}/{len(work_tests)} -> {status}")

        self.stdout.write(self.style.SUCCESS("Автотесты завершены"))
