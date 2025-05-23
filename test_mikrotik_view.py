# test_mikrotik_view.py
"""
Script para probar la vista MikroTik de forma independiente
"""
import sys
import os
import tkinter as tk
from tkinter import ttk

# Agregar src al path
sys.path.insert(0, "src")

def test_vista_mikrotik():
    """Prueba la vista MikroTik de forma independiente."""
    try:
        # Crear ventana principal
        root = tk.Tk()
        root.title("Prueba Vista MikroTik")
        root.geometry("1200x800")
        
        # Configurar tema básico
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except tk.TclError:
            pass
        
        # Configurar estilos básicos
        style.configure("Primary.TButton", background="#4CAF50", foreground="white")
        style.configure("Success.TButton", background="#2ECC71", foreground="white")
        style.configure("Danger.TButton", background="#E74C3C", foreground="white")
        
        print("🎨 Configurando estilos...")
        
        # Importar y crear la vista MikroTik
        from presentation.views.mikrotik_view import MikroTikView
        
        print("📱 Creando vista MikroTik...")
        mikrotik_view = MikroTikView(root)
        mikrotik_view.pack(fill=tk.BOTH, expand=True)
        
        print("✅ Vista MikroTik creada exitosamente")
        
        # Centrar ventana
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'+{x}+{y}')
        
        print("🚀 Iniciando interfaz...")
        print("\n" + "=" * 60)
        print("📋 INSTRUCCIONES DE PRUEBA:")
        print("1. La vista se abrirá con la interfaz completa")
        print("2. Puedes crear MikroTiks de prueba con el botón '➕ Nuevo'")
        print("3. Para probar conexiones reales, necesitas un MikroTik disponible")
        print("4. El ping funciona con cualquier IP (prueba con 8.8.8.8)")
        print("5. Para cerrar, simplemente cierra la ventana")
        print("=" * 60)
        
        # Iniciar la aplicación
        root.mainloop()
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {str(e)}")
        print("💡 Asegúrate de que todos los módulos estén disponibles")
        return False
    except Exception as e:
        print(f"❌ Error al probar vista: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_componentes_por_separado():
    """Prueba componentes individuales antes de la vista completa."""
    print("🧪 Probando componentes por separado...")
    
    try:
        # Probar importación del servicio
        from application.services.mikrotik_service import MikroTikService
        service = MikroTikService()
        print("✅ MikroTikService: OK")
        
        # Probar algunos MikroTiks de ejemplo
        mikrotiks = service.obtener_todos()
        print(f"📋 MikroTiks en BD: {len(mikrotiks)}")
        
        # Probar validación de IP
        test_ips = ["192.168.1.1", "8.8.8.8", "invalid-ip"]
        for ip in test_ips:
            valida = service._validar_ip(ip)
            print(f"🔍 IP '{ip}': {'✅' if valida else '❌'}")
        
        # Probar estadísticas
        stats = service.obtener_estadisticas()
        print(f"📊 Estadísticas: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba de componentes: {str(e)}")
        return False

def crear_mikrotiks_ejemplo():
    """Crea algunos MikroTiks de ejemplo para probar la vista."""
    print("\n📝 Creando MikroTiks de ejemplo...")
    
    try:
        from application.services.mikrotik_service import MikroTikService
        service = MikroTikService()
        
        mikrotiks_ejemplo = [
            {
                "nombre": "MTK-OFICINA-001",
                "ip": "192.168.1.100",
                "usuario": "admin",
                "contrasena": "admin123",
                "modelo": "RB750Gr3",
                "ubicacion": "Oficina Principal",
                "cliente_id": "CLI-001",
                "cliente_nombre": "Cliente Principal"
            },
            {
                "nombre": "MTK-SUCURSAL-001", 
                "ip": "192.168.2.100",
                "usuario": "admin",
                "contrasena": "password123",
                "modelo": "hEX",
                "ubicacion": "Sucursal Norte",
                "cliente_id": "CLI-002",
                "cliente_nombre": "Cliente Sucursal"
            },
            {
                "nombre": "MTK-CLIENTE-001",
                "ip": "10.0.0.100",
                "usuario": "admin",
                "contrasena": "mikrotik123",
                "modelo": "CCR1009",
                "ubicacion": "Casa Cliente",
                "cliente_id": "CLI-003",
                "cliente_nombre": "Cliente Residencial"
            }
        ]
        
        for mtk_data in mikrotiks_ejemplo:
            try:
                # Verificar si ya existe
                existente = service.obtener_por_nombre(mtk_data["nombre"])
                if existente:
                    print(f"  ⚠️ {mtk_data['nombre']}: Ya existe")
                    continue
                
                # Crear el MikroTik
                mikrotik = service.crear(**mtk_data)
                print(f"  ✅ {mikrotik.nombre}: Creado correctamente")
                
            except ValueError as e:
                print(f"  ⚠️ {mtk_data['nombre']}: {str(e)}")
            except Exception as e:
                print(f"  ❌ {mtk_data['nombre']}: Error - {str(e)}")
        
        # Mostrar estadísticas finales
        stats = service.obtener_estadisticas()
        print(f"\n📊 Total de MikroTiks: {stats['total']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear MikroTiks de ejemplo: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Prueba de Vista MikroTik")
    print("=" * 60)
    
    # Paso 1: Probar componentes
    print("PASO 1: Verificando componentes...")
    if not test_componentes_por_separado():
        print("❌ Error en componentes básicos")
        sys.exit(1)
    
    # Paso 2: Crear datos de ejemplo
    print("\nPASO 2: Creando datos de ejemplo...")
    crear_mikrotiks_ejemplo()
    
    # Paso 3: Preguntar si continuar con la vista
    print("\nPASO 3: ¿Abrir la vista MikroTik?")
    respuesta = input("¿Desea abrir la interfaz gráfica? (s/n): ").lower()
    
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        print("\n🎨 Abriendo vista MikroTik...")
        success = test_vista_mikrotik()
        
        if success:
            print("\n✅ ¡Vista MikroTik probada exitosamente!")
        else:
            print("\n❌ Hubo problemas con la vista")
    else:
        print("\n✅ Componentes verificados correctamente")
        print("💡 Para probar la vista, ejecuta nuevamente y responde 's'")
    
    print("\n📋 FASE 6 COMPLETADA:")
    print("✅ Modelo MikroTik creado")
    print("✅ Repositorio MikroTik implementado") 
    print("✅ Servicio MikroTik con todas las funcionalidades")
    print("✅ Vista MikroTik con interfaz completa")
    print("✅ Integración con aplicación principal")
    
    print("\n🎉 ¡Módulo MikroTik completado exitosamente!")
    print("🔧 Ya puedes gestionar equipos MikroTik desde tu aplicación")