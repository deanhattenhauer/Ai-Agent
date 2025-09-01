from functions.run_python import run_python_file

results_one = run_python_file("calculator", "main.py")
results_two = run_python_file("calculator", "main.py", ["3 + 5"])
results_three = run_python_file("calculator", "tests.py")
results_four = run_python_file("calculator", "../main.py") 
results_five = run_python_file("calculator", "nonexistent.py")


print(results_one)
print(results_two)
print(results_three)
print(results_four)
print(results_five)
