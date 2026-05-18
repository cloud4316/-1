import sys
import os
import subprocess
import tempfile
import time
from .utils import is_valid_text, fix_corrupted_text

MAX_OUTPUT_SIZE = 10_000


FORBIDDEN_IMPORTS = {"os", "sys", "subprocess", "socket", "shutil",
                     "ctypes", "multiprocessing", "threading", "importlib"}

def check_code_safety(code):
    """Возвращает (is_safe, reason)."""
    import ast as _ast
    try:
        tree = _ast.parse(code)
    except SyntaxError:
        return True, ""  # синтакс-ошибки поймает выполнение
    for node in _ast.walk(tree):
        if isinstance(node, (_ast.Import, _ast.ImportFrom)):
            names = [a.name.split(".")[0] for a in node.names] if isinstance(node, _ast.Import) else [node.module.split(".")[0] if node.module else ""]
            for name in names:
                if name in FORBIDDEN_IMPORTS:
                    return False, f"Запрещённый модуль: {name}"
    return True, ""

def run_python_code(code, input_data=None):
    safe, reason = check_code_safety(code)
    if not safe:
        return {'status': 'error', 'output': f'Запрещено: {reason}', 'error': reason}
    """
    Run Python code and return the result
    """
    if not is_valid_text(code):
        code = fix_corrupted_text(code)
        
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w', encoding='utf-8') as f:
        f.write(code)
        temp_file = f.name
    
    try:
        env = {**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}
        process = subprocess.Popen(
            [sys.executable, temp_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            env=env,
        )

        stdout, stderr = process.communicate(input=input_data, timeout=5)
        
        if process.returncode != 0:
            return {
                'status': 'error',
                'output': stderr,
                'error': stderr
            }
        
        return {
            'status': 'success',
            'output': stdout
        }
    except subprocess.TimeoutExpired:
        process.kill()
        return {
            'status': 'error',
            'output': 'Execution timed out',
            'error': 'Execution timed out after 10 seconds'
        }
    except Exception as e:
        return {
            'status': 'error',
            'output': str(e),
            'error': str(e)
        }
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def run_java_code(code, input_data=None):
    """
    Run Java code and return the result
    """
    if not is_valid_text(code):
        code = fix_corrupted_text(code)
        
    # Extract class name from code
    class_name = "Main"  # Default class name
    for line in code.split('\n'):
        if "public class" in line:
            parts = line.split("public class")[1].split("{")[0].strip().split()
            if parts:
                class_name = parts[0]
                break
    
    with tempfile.TemporaryDirectory() as temp_dir:
        java_file = os.path.join(temp_dir, f"{class_name}.java")
        
        with open(java_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # Compile Java code
        # Проверяем наличие javac
        import shutil
        if not shutil.which('javac'):
            return {'status': 'error', 'output': '', 'error': 'Java (javac) не установлена на этом компьютере.'}
        compile_process = subprocess.run(
            ['javac', '-encoding', 'UTF-8', java_file],
            capture_output=True,
            text=True,
            encoding='utf-8',
        )

        if compile_process.returncode != 0:
            return {
                'status': 'error',
                'output': compile_process.stderr,
                'error': f"Compilation error: {compile_process.stderr}"
            }

        # Run Java code
        try:
            process = subprocess.Popen(
                ['java', '-Dfile.encoding=UTF-8', '-Dstdout.encoding=UTF-8', '-cp', temp_dir, class_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
            )
            
            stdout, stderr = process.communicate(input=input_data, timeout=5)
            
            if process.returncode != 0:
                return {
                    'status': 'error',
                    'output': stderr,
                    'error': stderr
                }
            
            return {
                'status': 'success',
                'output': stdout
            }
        except subprocess.TimeoutExpired:
            process.kill()
            return {
                'status': 'error',
                'output': 'Execution timed out',
                'error': 'Execution timed out after 10 seconds'
            }
        except Exception as e:
            return {
                'status': 'error',
                'output': str(e),
                'error': str(e)
            }

def run_cpp_code(code, input_data=None):
    """
    Run C++ code and return the result
    """
    if not is_valid_text(code):
        code = fix_corrupted_text(code)
        
    with tempfile.TemporaryDirectory() as temp_dir:
        cpp_file = os.path.join(temp_dir, "main.cpp")
        exe_file = os.path.join(temp_dir, "main.exe")
        
        with open(cpp_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # Compile C++ code
        compile_process = subprocess.run(
            ['g++', cpp_file, '-o', exe_file, '-finput-charset=UTF-8', '-fexec-charset=UTF-8'],
            capture_output=True,
            text=True,
            encoding='utf-8',
        )

        if compile_process.returncode != 0:
            return {
                'status': 'error',
                'output': compile_process.stderr,
                'error': f"Compilation error: {compile_process.stderr}"
            }

        # Run C++ code
        try:
            env_cpp = {**os.environ, 'PYTHONIOENCODING': 'utf-8'}
            process = subprocess.Popen(
                [exe_file],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                env=env_cpp,
            )
            
            stdout, stderr = process.communicate(input=input_data, timeout=5)
            
            if process.returncode != 0:
                return {
                    'status': 'error',
                    'output': stderr,
                    'error': stderr
                }
            
            return {
                'status': 'success',
                'output': stdout
            }
        except subprocess.TimeoutExpired:
            process.kill()
            return {
                'status': 'error',
                'output': 'Execution timed out',
                'error': 'Execution timed out after 10 seconds'
            }
        except Exception as e:
            return {
                'status': 'error',
                'output': str(e),
                'error': str(e)
            }

def run_javascript_code(code, input_data=None):
    """
    Run JavaScript code using Node.js and return the result
    """
    if not is_valid_text(code):
        code = fix_corrupted_text(code)
        
    with tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='w', encoding='utf-8') as f:
        f.write(code)
        temp_file = f.name
    
    try:
        process = subprocess.Popen(
            ['node', temp_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
        )
        
        stdout, stderr = process.communicate(input=input_data, timeout=5)
        
        if process.returncode != 0:
            return {
                'status': 'error',
                'output': stderr,
                'error': stderr
            }
        
        return {
            'status': 'success',
            'output': stdout
        }
    except subprocess.TimeoutExpired:
        process.kill()
        return {
            'status': 'error',
            'output': 'Execution timed out',
            'error': 'Execution timed out after 10 seconds'
        }
    except Exception as e:
        return {
            'status': 'error',
            'output': str(e),
            'error': str(e)
        }
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)