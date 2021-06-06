package com.company;

import org.python.core.PyInteger;
import org.python.core.PyObject;
import org.python.core.PySystemState;
import org.python.util.InteractiveConsole;
import org.python.util.PythonInterpreter;

import java.util.Properties;

public class Main {

	public static void main(String[] args) {
		int[] psi = {0,0,0,0,0,0,0,0};
		// функция выхода
		int[] ksi = {0,0,0,0,0,0,0,0};
		// the java stack traces within the jython runtime aren't useful for users
		 PythonInterpreter interp = new InteractiveConsole();
        interp.exec("import sys");
        interp.exec("print sys");
        interp.set("a", new PyInteger(42));
        interp.exec("print a");
        interp.exec("x = 2+2");
        PyObject x = interp.get("x");
        System.out.println("x: " + x);
	}
}
