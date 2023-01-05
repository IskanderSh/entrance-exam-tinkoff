# entrance-exam-tinkoff

Программа для оценки схожести двух python текстов:

## Files
- [Compare.py](#compare)
- [Tester.py](#tester)
- [Input.txt](#input)
- [Scores.txt](#scores)
- [Files, Plagiat1, Plagiat2](#files)

### Compare.py <div id="#compare"></div>
В этом файле реализован код, который сравнивает похожесть двух программ алгоритмом Левенштейна. Он принимает данные из - [Input.txt](#input) и записывает выходные данные
в [Scores.txt](#scores)

### Tester.py <div id="#tester"></div>
Данный файл создан для тестировки программы, он рандомно выбирает какие 50 файлов проверить на антиплагиат и записывает эти данные в [Input.txt](#input). В в [Input.txt](#input)
можно ввести и свои данные

### Input.txt <div id="#input"></div>
Входные данные в виде:
```
files/main.py plagiat1/main.py
files/arima.py plagiat2/arima.py
files/cgd.py files/cgd.py
```

### Scores.txt <div id="#scores"></div>
Выходные данные в виде:
```
0.5148514851485149
0.41037204058624577
1.0
```

### Files, Plagiat1, Plagiat2 <div id="files"></div>
Папки где хранятся python файлы для проверки схожести
