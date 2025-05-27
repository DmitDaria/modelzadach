import requests
import numpy as np
from scipy.special import spherical_jn, spherical_yn
import matplotlib.pyplot as plt
import toml
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

class TaskDownloader:
    @staticmethod
    def get_task_params(url: str, variant: int) -> tuple:
        response = requests.get(url)
        response.raise_for_status()
        data = toml.loads(response.text)
        
        for item in data["data"]:
            if item.get("variant") == variant:
                return float(item["D"]), float(item["fmin"]), float(item["fmax"])
        raise ValueError(f"Вариант {variant} не найден")

class RCS:
    def __init__(self, D: float):
        self.r = D / 2

    def calculate(self, frequencies: np.ndarray, n_terms: int = 20) -> np.ndarray:
        rcs = np.zeros_like(frequencies)
        
        for i, f in enumerate(frequencies):
            wavelength = 3e8 / f
            k = 2 * np.pi / wavelength
            kr = k * self.r
            
            sum_term = 0j
            for n in range(1, n_terms + 1):
                jn = spherical_jn(n, kr)
                jn_1 = spherical_jn(n-1, kr)
                yn = spherical_yn(n, kr)
                hn = jn + 1j * yn
                hn_1 = spherical_jn(n-1, kr) + 1j * spherical_yn(n-1, kr)
                
                a_n = jn / hn
                b_n = (kr*jn_1 - n*jn) / (kr*hn_1 - n*hn)
                sum_term += (-1)**n * (n + 0.5) * (b_n - a_n)
            
            rcs[i] = (wavelength**2 / np.pi) * abs(sum_term)**2
        
        return rcs

def save_results(filename: str, freqs: np.ndarray, rcs: np.ndarray):
    root = Element('data')
    
    for tag, values in [
        ('frequencydata', freqs),
        ('lambdadata', 3e8/freqs),
        ('rcsdata', rcs)
    ]:
        elem = SubElement(root, tag)
        for val in values:
            SubElement(elem, tag[:-4]).text = f"{val:.6e}"

    xml_str = minidom.parseString(tostring(root)).toprettyxml()
    with open(filename, 'w') as f:
        f.write(xml_str)

def plot_results(freqs: np.ndarray, rcs: np.ndarray):
    plt.figure(figsize=(10, 6))
    plt.plot(freqs, rcs)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('RCS (m²)')
    plt.title('Radar Cross Section of a Sphere')
    plt.grid(True)
    plt.show()

def main():
    try:
        url = "https://jenyay.net/uploads/Student/Modelling/task_rcs_01.toml"
        variant = 6
        n_points = 200

        D, fmin, fmax = TaskDownloader.get_task_params(url, variant)
        print(f"Параметры: D={D}m, fmin={fmin}Hz, fmax={fmax}Hz")

        freqs = np.logspace(np.log10(fmin), np.log10(fmax), n_points)
        rcs = RCS(D).calculate(freqs)

        save_results(f"rcs_{variant}.xml", freqs, rcs)
        plot_results(freqs, rcs)

    except Exception as e:
        print(f"Ошибка: {e}\nПроверьте URL и параметры варианта")

if __name__ == "__main__":
    main()