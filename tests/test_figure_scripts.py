import py_compile
import unittest


class FigureScriptTests(unittest.TestCase):
    def test_figure_scripts_compile(self):
        scripts = [
            "figures/generate_fig5_architecture.py",
            "figures/generate_fig8_results.py",
            "figures/generate_fig9_fault_type.py",
            "figures/generate_fig10_noise_effect.py",
        ]
        for script in scripts:
            py_compile.compile(script, doraise=True)


if __name__ == "__main__":
    unittest.main()
