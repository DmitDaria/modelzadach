import os 
import numpy as np 
import matplotlib.pyplot as plt 
import xml.etree.ElementTree as ET 
from xml.dom import minidom 

A=1.34941
x1 = np.linspace(-10, 10, 1000) 
y1 = -0.0001 * (np.abs(np.sin(x1) * np.sin(A) * np.exp(np.abs(100 - np.sqrt((x1**2 + A**2) / np.pi) ) )) + 1)**0.1

root = ET.Element("data") 
xdata = ET.SubElement(root, "xdata") 
ydata = ET.SubElement(root, "ydata")

for x, y in zip(x1, y1): 
    ET.SubElement(xdata, "x").text = f"{x:.6f}" 
    ET.SubElement(ydata, "y").text = f"{y:.6f}" 

results_dir = "results" 
os.makedirs(results_dir, exist_ok=True)

output_path = os.path.join(results_dir, 
"function_results.xml") 
xml_str = ET.tostring(root, encoding="utf-8") 
pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="")

with open(output_path, "w", encoding="utf-8") as f: 
    f.write(pretty_xml)

plt.plot(x1, y1, label="f(x)", color='blue') 
plt.title("График функции f(x)") 
plt.xlabel("x") 
plt.ylabel("f(x)") 
plt.grid(True) 
plt.legend() 
plt.show()
