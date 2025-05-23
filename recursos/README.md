# Directorio de Recursos

Este directorio contiene todos los recursos necesarios para la aplicación de gestión de red.

## Estructura de Directorios

### 📄 `/documentos`
Documentos generados por la aplicación:
- `upgrades/` - Documentos de upgrades de servicio
- `downgrades/` - Documentos de downgrades de servicio
- `instalaciones/` - Documentos de nuevas instalaciones
- `imagenes/` - Imágenes extraídas o utilizadas en documentos

### 📋 `/plantillas`
Plantillas para generar documentos:
- `word/` - Plantillas de Microsoft Word
- `correo/` - Plantillas de correos electrónicos

### 🖼️ `/imagenes`
Imágenes de la aplicación:
- Logos de la empresa
- Iconos de la interfaz
- Imágenes de referencia

### 📤 `/exports`
Exports de configuración de equipos:
- Configuraciones de Mikrotik
- Configuraciones de switches
- Otros exports de equipos de red

### 💾 `/backup`
Respaldos automáticos:
- Respaldos de la base de datos
- Respaldos de configuraciones importantes

### 📝 `/logs`
Archivos de registro de la aplicación:
- Logs de errores
- Logs de actividad del usuario
- Logs del sistema

### 🔄 `/temp`
Archivos temporales:
- Archivos temporales durante la exportación
- Imágenes temporales del portapapeles
- Cachés temporales

## Uso

Todos estos directorios son creados automáticamente por la aplicación cuando es necesario.
No elimine estos directorios a menos que esté seguro de lo que está haciendo.

## Mantenimiento

- Los archivos temporales pueden ser eliminados periódicamente
- Los logs antiguos se rotan automáticamente
- Los backups se pueden programar según sus necesidades
