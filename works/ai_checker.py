"""
Умная проверка кода студентов.
Использует ast-анализ + запуск против тест-кейсов.
Не требует внешнего API.
"""
import ast as _ast
import os
import json


def analyze_code_quality(code: str) -> dict:
    """Анализирует качество Python кода через AST."""
    issues = []
    suggestions = []
    score = 100

    try:
        tree = _ast.parse(code)
    except SyntaxError as e:
        return {
            "score": 0,
            "issues": [f"Синтаксическая ошибка: {e}"],
            "suggestions": ["Исправьте синтаксические ошибки перед отправкой"],
            "passed": False,
        }

    # Проверка 1: Есть ли функции (хороший стиль)
    functions = [n for n in _ast.walk(tree) if isinstance(n, _ast.FunctionDef)]
    if not functions and len(code) > 200:
        issues.append("Код не разбит на функции")
        suggestions.append("Разбейте код на функции для лучшей читаемости")
        score -= 10

    # Проверка 2: Есть ли комментарии
    if "#" not in code and len(code) > 100:
        issues.append("Нет комментариев в коде")
        suggestions.append("Добавьте комментарии для пояснения логики")
        score -= 5

    # Проверка 3: Имена переменных (не одиночные буквы, кроме i, j, k, n, x, y)
    ok_single = {"i", "j", "k", "n", "x", "y", "a", "b", "c", "s"}
    for node in _ast.walk(tree):
        if isinstance(node, _ast.Name) and isinstance(node.ctx, _ast.Store):
            if len(node.id) == 1 and node.id not in ok_single:
                issues.append(f"Однобуквенное имя переменной: '{node.id}'")
                score -= 3
                break

    # Проверка 4: Глобальные переменные
    globals_count = sum(1 for n in _ast.walk(tree) if isinstance(n, _ast.Global))
    if globals_count > 0:
        issues.append(f"Используются глобальные переменные ({globals_count} раз)")
        suggestions.append("Избегайте global — передавайте данные через параметры")
        score -= 5

    # Проверка 5: Вложенность
    max_depth = _get_max_depth(tree)
    if max_depth > 5:
        issues.append(f"Глубокая вложенность кода: {max_depth} уровней")
        suggestions.append("Уменьшите вложенность — разбейте на функции")
        score -= 10

    score = max(0, score)
    return {
        "score": score,
        "issues": issues,
        "suggestions": suggestions,
        "passed": score >= 60,
        "functions_count": len(functions),
        "lines_count": len(code.splitlines()),
        "max_depth": max_depth,
    }


def _get_max_depth(tree, depth=0):
    """Определяет максимальную глубину вложенности AST."""
    max_d = depth
    for child in _ast.iter_child_nodes(tree):
        if isinstance(child, (_ast.If, _ast.For, _ast.While, _ast.With, _ast.Try,
                               _ast.FunctionDef, _ast.ClassDef)):
            max_d = max(max_d, _get_max_depth(child, depth + 1))
    return max_d


def check_solution_with_tests(code: str, work_order: int) -> dict:
    """Проверяет код против тест-кейсов из auto_tests.json."""
    from works.code_runner import run_python_code

    tests_path = os.path.join(
        os.path.dirname(__file__), "test_data", "auto_tests.json"
    )
    if not os.path.exists(tests_path):
        return {"score": None, "status": "no_tests", "passed": 0, "total": 0}

    with open(tests_path, encoding="utf-8") as f:
        all_tests = json.load(f)

    work_tests = all_tests.get(str(work_order), [])
    if not work_tests:
        return {"score": None, "status": "no_tests", "passed": 0, "total": 0}

    passed = 0
    results = []
    for test in work_tests:
        result = run_python_code(code, input_data=test["input"])
        actual = (result.get("output") or "").strip()
        expected = test["expected"].strip()
        ok = expected in actual or actual == expected
        if ok:
            passed += 1
        results.append({
            "input": test["input"],
            "expected": expected,
            "actual": actual[:200],
            "passed": ok,
        })

    total = len(work_tests)
    score = round(passed * 100 / total) if total else 0
    return {
        "score": score,
        "status": "correct" if score >= 70 else "partially_correct" if score >= 40 else "incorrect",
        "passed": passed,
        "total": total,
        "results": results,
    }


class AICodeChecker:
    """Запускает автопроверку решения и сохраняет результат в CodeCheck."""

    def check_solution(self, solution_id: int, code_check_id: int) -> None:
        from django.utils import timezone
        from works.models import Solution, CodeCheck

        try:
            solution = Solution.objects.get(id=solution_id)
            code_check = CodeCheck.objects.get(id=code_check_id)
        except Exception:
            return

        try:
            # Читаем код из файла
            file_path = solution.code_file.path
            with open(file_path, encoding='utf-8', errors='replace') as f:
                code = f.read()

            # AST-анализ качества
            quality = analyze_code_quality(code)

            # Прогон против тест-кейсов
            tests = check_solution_with_tests(code, solution.work.order)

            # Итоговая оценка: 60% тесты + 40% качество (если тесты есть)
            if tests["status"] != "no_tests":
                final_score = round(tests["score"] * 0.6 + quality["score"] * 0.4)
                verdict = tests["status"]
            else:
                final_score = quality["score"]
                verdict = "correct" if quality["passed"] else "incorrect"

            feedback_lines = []
            if tests["status"] != "no_tests":
                feedback_lines.append(
                    f"Тесты: {tests['passed']}/{tests['total']} пройдено ({tests['score']}%)"
                )
            if quality["issues"]:
                feedback_lines.append("Замечания по коду: " + "; ".join(quality["issues"]))

            code_check.status = 'completed'
            code_check.score = final_score
            code_check.feedback = "\n".join(feedback_lines) or "Проверка завершена."
            code_check.suggestions = quality["suggestions"]
            code_check.errors = quality["issues"]
            code_check.warnings = []
            code_check.completed_at = timezone.now()
            code_check.save()

            # Обновляем статус самого решения
            solution.status = verdict
            solution.score = final_score
            if tests["status"] != "no_tests":
                solution.test_results = {"tests": tests.get("results", []), "passed": tests["passed"], "total": tests["total"]}
            solution.save()

        except Exception as e:
            try:
                code_check.status = 'failed'
                code_check.feedback = f"Ошибка проверки: {e}"
                code_check.completed_at = timezone.now()
                code_check.save()
            except Exception:
                pass
