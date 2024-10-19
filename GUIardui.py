import tkinter as tk
from tkinter import messagebox
import serial
import serial.tools.list_ports
import time

class ESP32InterfaceApp:
    def __init__(self, window):
        self.window = window
        self.window.title("ESP32 Serial Interface GUI")
        self.arduino = None  # Objeto serial inicialmente desconectado

        # Puerto
        self.port_var = tk.StringVar(value="Seleccionar puerto")
        self.port_menu = tk.OptionMenu(window, self.port_var, *self.get_serial_ports())
        self.port_menu.pack(pady=5)

        # Botón conectar puerto
        self.connect_button = tk.Button(window, text="Conectar", command=self.connect_serial)
        self.connect_button.pack(pady=5)

        # Entrada para el número
        self.num_entry = tk.Entry(window)
        self.num_entry.insert(0, "Ingresa un número")
        self.num_entry.bind("<FocusIn>", self.clear_placeholder)  # Evento para borrar el placeholder
        self.num_entry.pack(pady=5)

        # Resultado
        self.result_label = tk.Label(window, text="Resultado:")
        self.result_label.pack(pady=5)

        # Botón enviar número
        self.send_button = tk.Button(window, text="Enviar", command=self.send_number)
        self.send_button.pack(pady=5)

        # Botón desconectar
        self.disconnect_button = tk.Button(window, text="Desconectar", command=self.disconnect_serial)
        self.disconnect_button.pack(pady=5)

        # Botón salir
        self.exit_button = tk.Button(window, text="Salir", command=window.quit)
        self.exit_button.pack(pady=5)

    def get_serial_ports(self):
        """Obtiene una lista de puertos seriales disponibles."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect_serial(self):
        """Conecta al puerto serial seleccionado."""
        port = self.port_var.get()
        if port == "Seleccionar puerto" or not port:
            messagebox.showerror("Error", "Seleccione un puerto")
            return
        try:
            self.arduino = serial.Serial(port=port, baudrate=115200, timeout=0.1)
            messagebox.showinfo("Conectado", f"Conectado al puerto {port}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al puerto {port}: {str(e)}")

    def clear_placeholder(self, event):
        """Elimina el placeholder cuando el usuario empieza a escribir."""
        if self.num_entry.get() == "Ingresa un número":
            self.num_entry.delete(0, tk.END)

    def send_number(self):
        """Envía un número al ESP32 y muestra el resultado."""
        if not self.arduino or not self.arduino.is_open:
            messagebox.showwarning("Advertencia", "Conéctese al puerto antes de enviar un número.")
            return

        num = self.num_entry.get()
        if not num.isdigit():
            messagebox.showerror("Error", "Ingrese un número válido")
            return

        self.arduino.write(bytes(num, 'utf-8'))  # Enviar número en formato utf-8
        time.sleep(0.05)  # Pequeña pausa para la respuesta
        result = self.arduino.readline().decode('utf-8').strip()  # Leer respuesta
        self.result_label.config(text=f"Resultado: {result}")

    def disconnect_serial(self):
        """Desconecta el puerto serial."""
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            messagebox.showinfo("Desconectado", "Puerto desconectado")
        else:
            messagebox.showwarning("Advertencia", "No hay puerto conectado")

if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("300x350")
    app = ESP32InterfaceApp(window)
    window.mainloop()

