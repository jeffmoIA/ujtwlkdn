# src/application/services/mikrotik_service.py
"""
Servicio para la gestión de equipos MikroTik.
Este servicio maneja toda la lógica de negocio relacionada con MikroTiks.
"""
import subprocess
import platform
import re
from typing import List, Optional, Dict, Any, Tuple
import time

# Importar librería para conectar con MikroTik
try:
    import librouteros
    from librouteros import connect
    LIBROUTEROS_AVAILABLE = True
except ImportError:
    LIBROUTEROS_AVAILABLE = False
    print("⚠️ librouteros no está instalado. Instálalo con: pip install librouteros")

from domain.models.mikrotik import MikroTik
from infrastructure.repositories.mikrotik_repository import MikroTikRepository

class MikroTikService:
    """Servicio para manejar operaciones relacionadas con equipos MikroTik."""
    
    def __init__(self):
        """Constructor del servicio."""
        self.repository = MikroTikRepository()
        
        # Configuraciones por defecto
        self.timeout_ping = 3  # Segundos para timeout de ping
        self.timeout_api = 10  # Segundos para timeout de conexión API
    
    # === OPERACIONES CRUD CON VALIDACIONES ===
    
    def obtener_todos(self) -> List[MikroTik]:
        """
        Obtiene todos los equipos MikroTik.
        
        Returns:
            List[MikroTik]: Lista de todos los MikroTiks
        """
        return self.repository.get_all()
    
    def obtener_por_id(self, mikrotik_id: int) -> Optional[MikroTik]:
        """
        Obtiene un MikroTik por su ID.
        
        Args:
            mikrotik_id: ID del MikroTik a buscar
            
        Returns:
            Optional[MikroTik]: El MikroTik encontrado o None si no existe
        """
        return self.repository.get_by_id(mikrotik_id)
    
    def obtener_por_nombre(self, nombre: str) -> Optional[MikroTik]:
        """
        Obtiene un MikroTik por su nombre.
        
        Args:
            nombre: Nombre del MikroTik a buscar
            
        Returns:
            Optional[MikroTik]: El MikroTik encontrado o None si no existe
        """
        return self.repository.get_by_nombre(nombre)
    
    def obtener_por_ip(self, ip: str) -> Optional[MikroTik]:
        """
        Obtiene un MikroTik por su IP.
        
        Args:
            ip: IP del MikroTik a buscar
            
        Returns:
            Optional[MikroTik]: El MikroTik encontrado o None si no existe
        """
        return self.repository.get_by_ip(ip)
    
    def crear(self, nombre: str, ip: str, usuario: str = "admin", 
              contrasena: str = "", modelo: str = "", version: str = "",
              ubicacion: str = "", cliente_id: str = "", 
              cliente_nombre: str = "", notas: str = "") -> MikroTik:
        """
        Crea un nuevo MikroTik con validaciones de negocio.
        
        Args:
            nombre: Nombre único del MikroTik
            ip: Dirección IP única del MikroTik
            usuario: Usuario para acceso (por defecto "admin")
            contrasena: Contraseña para acceso
            modelo: Modelo del MikroTik
            version: Versión de RouterOS
            ubicacion: Ubicación física
            cliente_id: ID del cliente
            cliente_nombre: Nombre del cliente
            notas: Notas adicionales
            
        Returns:
            MikroTik: El MikroTik creado
            
        Raises:
            ValueError: Si los datos no son válidos o ya existen
        """
        # === VALIDACIONES DE NEGOCIO ===
        
        # Validar campos obligatorios
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del MikroTik es obligatorio")
        
        if not ip or not ip.strip():
            raise ValueError("La IP del MikroTik es obligatoria")
        
        # Validar formato de IP
        if not self._validar_ip(ip):
            raise ValueError(f"La IP '{ip}' no tiene un formato válido")
        
        # Validar unicidad
        if self.repository.existe_nombre(nombre):
            raise ValueError(f"Ya existe un MikroTik con el nombre '{nombre}'")
        
        if self.repository.existe_ip(ip):
            raise ValueError(f"Ya existe un MikroTik con la IP '{ip}'")
        
        # === CREAR EL MIKROTIK ===
        
        # Crear el nuevo MikroTik
        nuevo_mikrotik = MikroTik(
            nombre=nombre.strip(),
            ip_mikrotik=ip.strip(),
            usuario_acceso=usuario.strip() or "admin",
            contrasena_acceso=contrasena,  # En producción, esto debería encriptarse
            modelo=modelo.strip() if modelo else None,
            version_routeros=version.strip() if version else None,
            ubicacion=ubicacion.strip() if ubicacion else None,
            cliente_id=cliente_id.strip() if cliente_id else None,
            cliente_nombre=cliente_nombre.strip() if cliente_nombre else None,
            notas=notas.strip() if notas else None,
            estado="activo",  # Por defecto activo
            disponible=False  # Se determinará con ping
        )
        
        # Guardar en base de datos
        mikrotik_creado = self.repository.create(nuevo_mikrotik)
        
        # ARREGLO: Verificar conectividad sin actualizar inmediatamente
        # Esto evita problemas de sesión de SQLAlchemy
        try:
            # Solo hacer ping, sin actualizar estado inmediatamente
            disponible = self.hacer_ping(mikrotik_creado.ip_mikrotik)
            print(f"🏓 Ping a {mikrotik_creado.ip_mikrotik}: {'✅' if disponible else '❌'}")
            
            # Si quieres actualizar la disponibilidad, hazlo después con una nueva consulta
            # self.verificar_conectividad(mikrotik_creado.id)  # Comentado para evitar el error
            
        except Exception as e:
            print(f"⚠️ Error al verificar conectividad inicial: {str(e)}")
        
        return mikrotik_creado
    
    def actualizar(self, mikrotik_id: int, nombre: str = None, ip: str = None,
                   usuario: str = None, contrasena: str = None, modelo: str = None,
                   version: str = None, ubicacion: str = None, estado: str = None,
                   cliente_id: str = None, cliente_nombre: str = None,
                   notas: str = None) -> Optional[MikroTik]:
        """
        Actualiza un MikroTik existente con validaciones.
        
        Args:
            mikrotik_id: ID del MikroTik a actualizar
            [Resto de parámetros opcionales]
            
        Returns:
            Optional[MikroTik]: El MikroTik actualizado o None si no existe
            
        Raises:
            ValueError: Si los datos no son válidos
        """
        # Obtener el MikroTik existente
        mikrotik = self.repository.get_by_id(mikrotik_id)
        if not mikrotik:
            return None
        
        # === VALIDACIONES ===
        
        # Validar nombre si se proporciona
        if nombre is not None:
            if not nombre.strip():
                raise ValueError("El nombre no puede estar vacío")
            
            if self.repository.existe_nombre(nombre, excluir_id=mikrotik_id):
                raise ValueError(f"Ya existe otro MikroTik con el nombre '{nombre}'")
            
            mikrotik.nombre = nombre.strip()
        
        # Validar IP si se proporciona
        if ip is not None:
            if not ip.strip():
                raise ValueError("La IP no puede estar vacía")
            
            if not self._validar_ip(ip):
                raise ValueError(f"La IP '{ip}' no tiene un formato válido")
            
            if self.repository.existe_ip(ip, excluir_id=mikrotik_id):
                raise ValueError(f"Ya existe otro MikroTik con la IP '{ip}'")
            
            mikrotik.ip_mikrotik = ip.strip()
        
        # Validar estado si se proporciona
        if estado is not None:
            estados_validos = ["activo", "inactivo", "mantenimiento", "error"]
            if estado.lower() not in estados_validos:
                raise ValueError(f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}")
            
            mikrotik.estado = estado.lower()
        
        # Actualizar otros campos opcionales
        if usuario is not None:
            mikrotik.usuario_acceso = usuario.strip() or "admin"
        
        if contrasena is not None:
            mikrotik.contrasena_acceso = contrasena  # En producción, encriptar
        
        if modelo is not None:
            mikrotik.modelo = modelo.strip() if modelo else None
        
        if version is not None:
            mikrotik.version_routeros = version.strip() if version else None
        
        if ubicacion is not None:
            mikrotik.ubicacion = ubicacion.strip() if ubicacion else None
        
        if cliente_id is not None:
            mikrotik.cliente_id = cliente_id.strip() if cliente_id else None
        
        if cliente_nombre is not None:
            mikrotik.cliente_nombre = cliente_nombre.strip() if cliente_nombre else None
        
        if notas is not None:
            mikrotik.notas = notas.strip() if notas else None
        
        # Guardar cambios
        return self.repository.update(mikrotik)
    
    def eliminar(self, mikrotik_id: int) -> bool:
        """
        Elimina un MikroTik.
        
        Args:
            mikrotik_id: ID del MikroTik a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        return self.repository.delete(mikrotik_id)
    
    # === OPERACIONES DE CONECTIVIDAD ===
    
    def hacer_ping(self, ip: str) -> bool:
        """
        Hace ping a una IP para verificar conectividad.
        
        Args:
            ip: Dirección IP a hacer ping
            
        Returns:
            bool: True si responde, False si no responde
        """
        try:
            # Determinar comando según sistema operativo
            if platform.system().lower() == "windows":
                comando = ["ping", "-n", "1", "-w", str(self.timeout_ping * 1000), ip]
            else:  # Linux/Mac
                comando = ["ping", "-c", "1", "-W", str(self.timeout_ping), ip]
            
            # Ejecutar comando
            resultado = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                timeout=self.timeout_ping + 2  # Timeout extra para el proceso
            )
            
            # Verificar resultado
            return resultado.returncode == 0
            
        except subprocess.TimeoutExpired:
            return False
        except Exception as e:
            print(f"Error al hacer ping a {ip}: {str(e)}")
            return False
    
    def verificar_conectividad(self, mikrotik_id: int) -> bool:
        """
        Verifica la conectividad de un MikroTik y actualiza su estado.
        
        Args:
            mikrotik_id: ID del MikroTik a verificar
            
        Returns:
            bool: True si está disponible, False si no
        """
        # Obtener el MikroTik
        mikrotik = self.repository.get_by_id(mikrotik_id)
        if not mikrotik:
            return False
        
        # Hacer ping
        disponible = self.hacer_ping(mikrotik.ip_mikrotik)
        
        # ARREGLO SIMPLE: Actualizar solo lo necesario usando parámetros específicos
        try:
            # Preparar actualizaciones
            updates = {}
            
            # Actualizar estado basado en disponibilidad
            if not disponible and mikrotik.estado == "activo":
                updates["estado"] = "error"
            elif disponible and mikrotik.estado == "error":
                updates["estado"] = "activo"
            
            # Usar el método actualizar si hay cambios de estado
            if updates:
                self.actualizar(mikrotik_id, **updates)
            
            # Para la disponibilidad, hacer una actualización directa más simple
            # Esto evita problemas de sesión de SQLAlchemy
            from infrastructure.database.config import SessionLocal
            with SessionLocal() as db:
                mtk = db.query(MikroTik).filter(MikroTik.id == mikrotik_id).first()
                if mtk:
                    mtk.disponible = disponible
                    db.commit()
            
        except Exception as e:
            print(f"⚠️ Error al actualizar disponibilidad del MikroTik {mikrotik_id}: {str(e)}")
            # Si falla la actualización, al menos retornamos el resultado del ping
            pass
        
        return disponible
    
    def verificar_conectividad_masiva(self) -> Dict[str, Any]:
        """
        Verifica la conectividad de todos los MikroTiks activos.
        
        Returns:
            Dict[str, Any]: Estadísticas de conectividad
        """
        mikrotiks_activos = self.repository.get_by_estado("activo")
        
        resultados = {
            "total_verificados": len(mikrotiks_activos),
            "disponibles": 0,
            "no_disponibles": 0,
            "detalles": []
        }
        
        for mikrotik in mikrotiks_activos:
            disponible = self.hacer_ping(mikrotik.ip_mikrotik)
            
            # ARREGLO: Actualizar de forma segura usando métodos del servicio
            try:
                # Solo actualizar estado si cambió
                if not disponible and mikrotik.estado == "activo":
                    self.actualizar(mikrotik.id, estado="error")
                
                # Actualizar disponibilidad
                mikrotik_fresh = self.repository.get_by_id(mikrotik.id)
                if mikrotik_fresh:
                    mikrotik_fresh.disponible = disponible
                    self.repository.update(mikrotik_fresh)
                
            except Exception as e:
                print(f"⚠️ Error al actualizar MikroTik {mikrotik.id}: {str(e)}")
            
            # Actualizar estadísticas
            if disponible:
                resultados["disponibles"] += 1
            else:
                resultados["no_disponibles"] += 1
            
            resultados["detalles"].append({
                "id": mikrotik.id,
                "nombre": mikrotik.nombre,
                "ip": mikrotik.ip_mikrotik,
                "disponible": disponible
            })
        
        return resultados
    
    # === CONEXIÓN A LA API DE MIKROTIK ===
    
    def conectar_mikrotik(self, mikrotik_id: int) -> Tuple[bool, str, Any]:
        """
        Conecta a un MikroTik mediante la API.
        
        Args:
            mikrotik_id: ID del MikroTik al que conectar
            
        Returns:
            Tuple[bool, str, Any]: (éxito, mensaje, conexión)
        """
        if not LIBROUTEROS_AVAILABLE:
            return False, "librouteros no está instalado", None
        
        # Obtener el MikroTik
        mikrotik = self.repository.get_by_id(mikrotik_id)
        if not mikrotik:
            return False, "MikroTik no encontrado", None
        
        # Verificar que tenga credenciales
        if not mikrotik.tiene_credenciales():
            return False, "MikroTik no tiene credenciales configuradas", None
        
        try:
            # Conectar a la API
            conexion = connect(
                username=mikrotik.usuario_acceso,
                password=mikrotik.contrasena_acceso,
                host=mikrotik.ip_mikrotik,
                timeout=self.timeout_api
            )
            
            return True, "Conexión exitosa", conexion
            
        except Exception as e:
            error_msg = f"Error al conectar: {str(e)}"
            return False, error_msg, None
    
    # === GESTIÓN DE COLAS (UPGRADE/DOWNGRADE) ===
    
    def obtener_colas(self, mikrotik_id: int) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """
        Obtiene las colas simples de un MikroTik.
        
        Args:
            mikrotik_id: ID del MikroTik
            
        Returns:
            Tuple[bool, str, List[Dict]]: (éxito, mensaje, lista de colas)
        """
        # Conectar al MikroTik
        exito, mensaje, conexion = self.conectar_mikrotik(mikrotik_id)
        if not exito:
            return False, mensaje, []
        
        try:
            # Obtener colas simples
            colas = list(conexion.path('/queue/simple').select('.id', 'name', 'target', 'max-limit'))
            
            # Cerrar conexión
            conexion.close()
            
            # Formatear resultados
            colas_formateadas = []
            for cola in colas:
                colas_formateadas.append({
                    'id': cola.get('.id', ''),
                    'name': cola.get('name', ''),
                    'target': cola.get('target', ''),
                    'max-limit': cola.get('max-limit', ''),
                })
            
            return True, "Colas obtenidas exitosamente", colas_formateadas
            
        except Exception as e:
            try:
                conexion.close()
            except:
                pass
            return False, f"Error al obtener colas: {str(e)}", []
    
    def modificar_cola(self, mikrotik_id: int, nombre_cola: str, 
                       mbps_download: float, mbps_upload: float = None) -> Tuple[bool, str]:
        """
        Modifica una cola específica con nuevo ancho de banda.
        
        Args:
            mikrotik_id: ID del MikroTik
            nombre_cola: Nombre de la cola a modificar
            mbps_download: Mbps de descarga (se convertirá a Kbps)
            mbps_upload: Mbps de subida (si no se especifica, usa el mismo que download)
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        # Usar mismo valor para upload si no se especifica
        if mbps_upload is None:
            mbps_upload = mbps_download
        
        # Convertir Mbps a Kbps usando la fórmula: Mbps * 1024
        kbps_download = int(mbps_download * 1024)
        kbps_upload = int(mbps_upload * 1024)
        
        # Formatear límite para MikroTik: "upload/download" en Kbps
        nuevo_limite = f"{kbps_upload}k/{kbps_download}k"
        
        # Conectar al MikroTik
        exito, mensaje, conexion = self.conectar_mikrotik(mikrotik_id)
        if not exito:
            return False, mensaje
        
        try:
            # Buscar la cola por nombre
            colas = list(conexion.path('/queue/simple').select('.id', 'name'))
            
            cola_encontrada = None
            for cola in colas:
                if cola.get('name') == nombre_cola:
                    cola_encontrada = cola
                    break
            
            if not cola_encontrada:
                conexion.close()
                return False, f"No se encontró la cola '{nombre_cola}'"
            
            # Modificar la cola
            conexion.path('/queue/simple').update(
                **{'.id': cola_encontrada['.id'], 'max-limit': nuevo_limite}
            )
            
            # Cerrar conexión
            conexion.close()
            
            return True, f"Cola '{nombre_cola}' actualizada a {mbps_download} Mbps ({nuevo_limite})"
            
        except Exception as e:
            try:
                conexion.close()
            except:
                pass
            return False, f"Error al modificar cola: {str(e)}"
    
    # === EXPORT DE CONFIGURACIÓN ===
    
    def obtener_export_completo(self, mikrotik_id: int) -> Tuple[bool, str, str]:
        """
        Obtiene el export completo de la configuración del MikroTik.
        
        Args:
            mikrotik_id: ID del MikroTik
            
        Returns:
            Tuple[bool, str, str]: (éxito, mensaje, export completo)
        """
        # Conectar al MikroTik
        exito, mensaje, conexion = self.conectar_mikrotik(mikrotik_id)
        if not exito:
            return False, mensaje, ""
        
        try:
            # Ejecutar comando export
            resultado = list(conexion.path('/export'))
            
            # Cerrar conexión
            conexion.close()
            
            # El export viene como una lista de líneas
            export_completo = '\n'.join(resultado) if resultado else "No se pudo obtener el export"
            
            # Guardar el export en el MikroTik para respaldo
            mikrotik = self.repository.get_by_id(mikrotik_id)
            if mikrotik:
                mikrotik.ultimo_export = export_completo
                self.repository.update(mikrotik)
            
            return True, "Export obtenido exitosamente", export_completo
            
        except Exception as e:
            try:
                conexion.close()
            except:
                pass
            return False, f"Error al obtener export: {str(e)}", ""
    
    # === MÉTODOS DE UTILIDAD ===
    
    def _validar_ip(self, ip: str) -> bool:
        """
        Valida si una IP tiene formato válido.
        
        Args:
            ip: IP a validar
            
        Returns:
            bool: True si es válida, False si no
        """
        patron = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        return bool(re.match(patron, ip))
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales de MikroTiks.
        
        Returns:
            Dict[str, Any]: Estadísticas completas
        """
        return {
            "total": len(self.repository.get_all()),
            "por_estado": self.repository.count_by_estado(),
            "por_modelo": self.repository.count_by_modelo(),
            "disponibilidad": self.repository.get_disponibilidad_stats(),
            "con_credenciales": len(self.repository.get_con_credenciales()),
            "sin_credenciales": len(self.repository.get_sin_credenciales())
        }