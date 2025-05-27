import argparse 
import os 
import xml.etree.ElementTree as ET 
import matplotlib.pyplot as plt 


def parse_xml(file_path): 
    tree = ET.parse(file_path) 
    root = tree.getroot() 

    x_dano = root.find("xdata").findall("x") 
    y_dano = root.find("ydata").findall("y") 
    x_zn = [float(x.text) for x in x_dano] 
    y_zn = [float(y.text) for y in y_dano] 

    return x_zn, y_zn


def main(): 
    parser = argparse.ArgumentParser(description="График функции из XML-файла") 
    parser.add_argument("filepath", type=str, help="Путь к XML-файлу") 
    parser.add_argument("--linewidth", type=float, default=1.0,help="Толщина линии графика (по умолчанию: 1.0)")

    args = parser.parse_args() 
    file_path = args.filepath 

    if not os.path.isfile(file_path): 
        print("Файл не найден") 
        return 

    x, y = parse_xml(file_path) 

    plt.plot(x, y, label="f(x)", color='blue', linewidth=1.0) 
    plt.title("График функции f(x)") 
    plt.xlabel("x") 
    plt.ylabel("f(x)") 
    plt.legend() 
    plt.grid(True)
    plt.tight_layout() 
    plt.show() 
    plt.plot(x, y, label="f(x)", color='blue', linewidth=args.linewidth) 
    plt.title("График функции f(x)") 
    plt.xlabel("x") 
    plt.ylabel("f(x)") 
    plt.legend() 
    plt.grid(True)
    plt.tight_layout() 
    plt.show() 


if __name__ == "__main__": 
    main()