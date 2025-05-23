# test_mikrotik_service.py
"""
Script para probar el servicio MikroTik
"""
import sys
import os

# Agregar src al path
sys.path.insert(0, "src")

def test_servicio_mikrotik():
    """Prueba las funcionalidades del servicio MikroTik."""
    try:
        from application.services.mikrotik_service import MikroTikService
        
        print("🧪 Probando servicio MikroTik...")
        
        # Crear instancia del servicio
        service = MikroTikService()
        print("✅ Servicio creado correctamente")
        
        # Probar validación de IP
        print("\n🔍 Probando validación de IP...")
        ips_prueba = [
            ("192.168.1.1", True),
            ("10.0.0.1", True), 
            ("256.256.256.256", False),
            ("192.168", False),
            ("no-es-ip", False)
        ]
        
        for ip, esperado in ips_prueba:
            resultado = service._validar_ip(ip)
            estado = "✅" if resultado == esperado else "❌"
            print(f"  {estado} IP '{ip}': {resultado} (esperado: {esperado})")
        
        # Probar crear MikroTik
        print("\n📝 Probando crear MikroTik...")
        try:
            mikrotik = service.crear(
                nombre="MTK-SERVICE-TEST",
                ip="192.168.200.1",
                usuario="admin",
                contrasena="test123",
                modelo="RB750Gr3",
                ubicacion="Oficina Test",
                cliente_id="CLI-TEST",
                cliente_nombre="Cliente Test"
            )
            print(f"✅ MikroTik creado: {mikrotik}")
            
        except ValueError as e:
            if "Ya existe" in str(e):
                print("⚠️ MikroTik ya existe, usando el existente")
                mikrotik = service.obtener_por_nombre("MTK-SERVICE-TEST")
            else:
                raise e
        
        # Probar ping
        print("\n🏓 Probando ping...")
        ips_ping = [
            "8.8.8.8",      # Google DNS (debería funcionar)
            "192.168.200.1", # IP del MikroTik test (probablemente no responda)
            "192.168.1.1"   # Gateway común (puede funcionar)
        ]
        
        for ip in ips_ping:
            resultado = service.hacer_ping(ip)
            estado = "✅" if resultado else "❌"
            print(f"  {estado} Ping a {ip}: {'Responde' if resultado else 'No responde'}")
        
        # Probar verificar conectividad
        if mikrotik:
            print(f"\n🔍 Probando verificar conectividad del MikroTik ID {mikrotik.id}...")
            disponible = service.verificar_conectividad(mikrotik.id)
            print(f"  {'✅' if disponible else '❌'} MikroTik disponible: {disponible}")
        
        # Probar obtener estadísticas
        print("\n📊 Probando estadísticas...")
        stats = service.obtener_estadisticas()
        print(f"  📋 Total MikroTiks: {stats['total']}")
        print(f"  📊 Por estado: {stats['por_estado']}")
        print(f"  🔧 Por modelo: {stats['por_modelo']}")
        print(f"  🌐 Disponibilidad: {stats['disponibilidad']}")
        
        # Probar validaciones de negocio
        print("\n🔒 Probando validaciones de negocio...")
        
        # Intentar crear con datos inválidos
        try:
            service.crear("", "192.168.1.1")  # Nombre vacío
            print("❌ ERROR: Debería haber fallado con nombre vacío")
        except ValueError as e:
            print(f"✅ Validación correcta: {str(e)}")
        
        try:
            service.crear("TEST", "ip-invalida")  # IP inválida
            print("❌ ERROR: Debería haber fallado con IP inválida")
        except ValueError as e:
            print(f"✅ Validación correcta: {str(e)}")
        
        # Probar búsquedas
        print("\n🔍 Probando búsquedas...")
        todos = service.obtener_todos()
        print(f"  📋 Total encontrados: {len(todos)}")
        
        if todos:
            primer_mtk = todos[0]
            print(f"  🔍 Búsqueda por ID: {service.obtener_por_id(primer_mtk.id).nombre if service.obtener_por_id(primer_mtk.id) else 'No encontrado'}")
            print(f"  🔍 Búsqueda por nombre: {service.obtener_por_nombre(primer_mtk.nombre).nombre if service.obtener_por_nombre(primer_mtk.nombre) else 'No encontrado'}")
            print(f"  🔍 Búsqueda por IP: {service.obtener_por_ip(primer_mtk.ip_mikrotik).nombre if service.obtener_por_ip(primer_mtk.ip_mikrotik) else 'No encontrado'}")
        
        # Probar conexión API (solo si librouteros está disponible)
        print("\n🔗 Probando conexión API...")
        try:
            import librouteros
            print("✅ librouteros disponible")
            
            if mikrotik and mikrotik.tiene_credenciales():
                print(f"  🔧 Intentando conectar a {mikrotik.ip_mikrotik}...")
                exito, mensaje, conexion = service.conectar_mikrotik(mikrotik.id)
                
                if exito:
                    print(f"  ✅ Conexión exitosa: {mensaje}")
                    
                    # Probar obtener colas
                    print("  🔍 Obteniendo colas...")
                    exito_colas, msg_colas, colas = service.obtener_colas(mikrotik.id)
                    if exito_colas:
                        print(f"    ✅ Colas obtenidas: {len(colas)} encontradas")
                        for cola in colas:
                            print(f"      • {cola.get('name', 'Sin nombre')}: {cola.get('max-limit', 'Sin límite')}")
                    else:
                        print(f"    ⚠️ Error obteniendo colas: {msg_colas}")
                    
                    # Probar export (solo si la conexión funciona)
                    print("  📄 Obteniendo export completo...")
                    exito_export, msg_export, export_data = service.obtener_export_completo(mikrotik.id)
                    if exito_export:
                        lineas = export_data.split('\n')
                        print(f"    ✅ Export obtenido: {len(lineas)} líneas de configuración")
                        print(f"    📋 Primeras líneas:")
                        for i, linea in enumerate(lineas[:3]):
                            print(f"      {i+1}: {linea[:80]}...")
                    else:
                        print(f"    ⚠️ Error obteniendo export: {msg_export}")
                    
                    # Cerrar conexión si existe
                    if conexion:
                        try:
                            conexion.close()
                        except:
                            pass
                        
                else:
                    print(f"  ⚠️ No se pudo conectar: {mensaje}")
            else:
                print("  ⚠️ MikroTik no tiene credenciales configuradas")
                
        except ImportError:
            print("⚠️ librouteros no está instalado")
            print("  💡 Para probar conexiones API, instala: pip install librouteros")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al probar servicio: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_formula_conversion():
    """Prueba la fórmula de conversión Mbps a Kbps."""
    print("\n🧮 Probando fórmula de conversión Mbps → Kbps...")
    
    casos_prueba = [
        (1, 1024),      # 1 Mbps = 1024 Kbps
        (5, 5120),      # 5 Mbps = 5120 Kbps
        (10, 10240),    # 10 Mbps = 10240 Kbps
        (100, 102400),  # 100 Mbps = 102400 Kbps
        (0.5, 512),     # 0.5 Mbps = 512 Kbps
    ]
    
    for mbps, kbps_esperado in casos_prueba:
        kbps_calculado = int(mbps * 1024)
        estado = "✅" if kbps_calculado == kbps_esperado else "❌"
        print(f"  {estado} {mbps} Mbps = {kbps_calculado} Kbps (esperado: {kbps_esperado})")
        
        # Formato para MikroTik
        formato_mikrotik = f"{kbps_calculado}k/{kbps_calculado}k"
        print(f"      Formato MikroTik: {formato_mikrotik}")

if __name__ == "__main__":
    print("🚀 Prueba del Servicio MikroTik")
    print("=" * 60)
    
    # Probar fórmula de conversión
    test_formula_conversion()
    
    # Probar servicio completo
    success = test_servicio_mikrotik()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ¡Servicio funcionando correctamente!")
        print("🎉 Puedes continuar con el Paso 4 (Vista)")
    else:
        print("❌ Hay problemas con el servicio")
        
    print("\n📋 Próximo paso: Crear vista MikroTik")
    print("💡 Recuerda instalar: pip install librouteros")
    print("🔧 Para probar conexiones reales, necesitarás un MikroTik disponible")