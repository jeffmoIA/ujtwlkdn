# test_mikrotik_repository.py
"""
Script para probar el repositorio MikroTik
"""
import sys
import os

# Agregar src al path
sys.path.insert(0, "src")

def test_repositorio_mikrotik():
    """Prueba las funcionalidades del repositorio MikroTik."""
    try:
        from infrastructure.repositories.mikrotik_repository import MikroTikRepository
        from domain.models.mikrotik import MikroTik
        
        print("🧪 Probando repositorio MikroTik...")
        
        # Crear instancia del repositorio
        repo = MikroTikRepository()
        print("✅ Repositorio creado correctamente")
        
        # Probar crear un MikroTik de ejemplo
        mikrotik_ejemplo = MikroTik(
            nombre="MTK-TEST-001",
            ip_mikrotik="192.168.100.1",
            modelo="RB750Gr3",
            version_routeros="6.49.10",
            usuario_acceso="admin",
            contrasena_acceso="password123",  # En producción esto debe estar encriptado
            ubicacion="Oficina de Pruebas",
            estado="activo",
            cliente_id="CLI-001",
            cliente_nombre="Cliente de Prueba"
        )
        
        print("📋 MikroTik de ejemplo creado")
        
        # Probar métodos de validación
        print("\n🔍 Probando validaciones...")
        existe_nombre = repo.existe_nombre("MTK-TEST-001")
        existe_ip = repo.existe_ip("192.168.100.1")
        
        print(f"  • ¿Existe nombre 'MTK-TEST-001'?: {existe_nombre}")
        print(f"  • ¿Existe IP '192.168.100.1'?: {existe_ip}")
        
        # Si no existen, crear el MikroTik
        if not existe_nombre and not existe_ip:
            mikrotik_creado = repo.create(mikrotik_ejemplo)
            print(f"✅ MikroTik creado en BD: {mikrotik_creado}")
            
            # Probar búsquedas
            print("\n🔍 Probando búsquedas...")
            por_nombre = repo.get_by_nombre("MTK-TEST-001")
            por_ip = repo.get_by_ip("192.168.100.1")
            activos = repo.get_activos()
            
            print(f"  • Búsqueda por nombre: {por_nombre.nombre if por_nombre else 'No encontrado'}")
            print(f"  • Búsqueda por IP: {por_ip.ip_mikrotik if por_ip else 'No encontrado'}")
            print(f"  • MikroTiks activos: {len(activos)}")
            
            # Probar estadísticas
            print("\n📊 Probando estadísticas...")
            stats_estado = repo.count_by_estado()
            stats_disponibilidad = repo.get_disponibilidad_stats()
            
            print(f"  • Por estado: {stats_estado}")
            print(f"  • Disponibilidad: {stats_disponibilidad}")
            
        else:
            print("⚠️ MikroTik ya existe, usando datos existentes")
        
        # Probar listado completo
        todos_mikrotiks = repo.get_all()
        print(f"\n📋 Total de MikroTiks en BD: {len(todos_mikrotiks)}")
        
        for mtk in todos_mikrotiks:
            print(f"  • {mtk.nombre} ({mtk.ip_mikrotik}) - {mtk.estado}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al probar repositorio: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Prueba del Repositorio MikroTik")
    print("=" * 50)
    
    success = test_repositorio_mikrotik()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ ¡Repositorio funcionando correctamente!")
        print("🎉 Puedes continuar con el Paso 3")
    else:
        print("❌ Hay problemas con el repositorio")
        
    print("\n📋 Próximo paso: Crear servicio MikroTik")