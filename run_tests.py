import unittest
import sys
import time

# Colores para la terminal
class Colors:
    # Colores ANSI
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    
    @staticmethod
    def enable_windows():
        """Habilita colores en Windows 10+"""
        try:
            import os
            os.system('color')
        except:
            pass

Colors.enable_windows()

class ColoredTextTestResult(unittest.TextTestResult):
    """Test result personalizado con colores"""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.test_times = {}
        self.start_time = None
        self.test_descriptions = descriptions
        self.test_verbosity = verbosity
        
    def startTest(self, test):
        super().startTest(test)
        self.start_time = time.time()
        
    def addSuccess(self, test):
        super().addSuccess(test)
        elapsed = time.time() - self.start_time
        self.test_times[test] = elapsed
        if self.test_verbosity >= 1:
            self.stream.write(f"{Colors.GREEN}✓ PASS{Colors.RESET} ")
            self.stream.write(f"{test} ")
            self.stream.write(f"{Colors.CYAN}({elapsed:.3f}s){Colors.RESET}\n")
            self.stream.flush()
    
    def addError(self, test, err):
        super().addError(test, err)
        elapsed = time.time() - self.start_time
        self.test_times[test] = elapsed
        if self.test_verbosity >= 1:
            self.stream.write(f"{Colors.RED}✗ ERROR{Colors.RESET} ")
            self.stream.write(f"{test} ")
            self.stream.write(f"{Colors.CYAN}({elapsed:.3f}s){Colors.RESET}\n")
            self.stream.flush()
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        elapsed = time.time() - self.start_time
        self.test_times[test] = elapsed
        if self.test_verbosity >= 1:
            self.stream.write(f"{Colors.RED}✗ FAIL{Colors.RESET} ")
            self.stream.write(f"{test} ")
            self.stream.write(f"{Colors.CYAN}({elapsed:.3f}s){Colors.RESET}\n")
            self.stream.flush()
    
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        if self.test_verbosity >= 1:
            self.stream.write(f"{Colors.YELLOW}⊘ SKIP{Colors.RESET} ")
            self.stream.write(f"{test} - {reason}\n")
            self.stream.flush()

class ColoredTextTestRunner(unittest.TextTestRunner):
    """Test runner con salida colorida y mejorada"""
    resultclass = ColoredTextTestResult
    
    def run(self, test):
        """Ejecuta los tests con formato mejorado"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}   EJECUTANDO PRUEBAS UNITARIAS - GESTOR DE NOTAS DAVIVIENDA{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")
        
        start_time = time.time()
        result = super().run(test)
        elapsed_time = time.time() - start_time
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}   RESUMEN DE PRUEBAS{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")
        
        total_tests = result.testsRun
        successes = total_tests - len(result.failures) - len(result.errors) - len(result.skipped)
        
        print(f"{Colors.BOLD}Total de pruebas:{Colors.RESET}  {total_tests}")
        print(f"{Colors.GREEN}✓ Exitosas:{Colors.RESET}        {successes}")
        
        if result.failures:
            print(f"{Colors.RED}✗ Fallidas:{Colors.RESET}         {len(result.failures)}")
        
        if result.errors:
            print(f"{Colors.RED}✗ Errores:{Colors.RESET}          {len(result.errors)}")
        
        if result.skipped:
            print(f"{Colors.YELLOW}⊘ Omitidas:{Colors.RESET}         {len(result.skipped)}")
        
        print(f"\n{Colors.BOLD}Tiempo total:{Colors.RESET}      {elapsed_time:.3f}s")
        
        if total_tests > 0:
            success_rate = (successes / total_tests) * 100
            if success_rate == 100:
                color = Colors.GREEN
                status = "TODAS LAS PRUEBAS PASARON"
            elif success_rate >= 80:
                color = Colors.YELLOW
                status = "MAYORIA DE PRUEBAS PASARON"
            else:
                color = Colors.RED
                status = "MULTIPLES FALLAS DETECTADAS"
            
            print(f"\n{color}{Colors.BOLD}Tasa de exito: {success_rate:.1f}%{Colors.RESET}")
            print(f"{color}{Colors.BOLD}{status}{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")
        
        if result.failures:
            print(f"{Colors.RED}{Colors.BOLD}DETALLES DE FALLAS:{Colors.RESET}\n")
            for test, traceback in result.failures:
                print(f"{Colors.RED}✗ {test}{Colors.RESET}")
                print(f"{traceback}\n")
        
        if result.errors:
            print(f"{Colors.RED}{Colors.BOLD}DETALLES DE ERRORES:{Colors.RESET}\n")
            for test, traceback in result.errors:
                print(f"{Colors.RED}✗ {test}{Colors.RESET}")
                print(f"{traceback}\n")
        
        return result

def run_all_tests():
    """Ejecuta todas las pruebas unitarias"""
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    runner = ColoredTextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_all_tests())
