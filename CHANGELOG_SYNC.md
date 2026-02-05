# Resumen de Cambios: Sincronización de Unidades y Conversiones

## ✅ Implementación Completada

Se ha implementado la sincronización completa de **unidades de medida** y **conversiones** tanto en exportación JSON como en sincronización con la nube (Supabase).

---

## 📦 Exportación JSON (Ya existente - Mejorado)

La función `exportBulkData()` ya incluía las unidades y conversiones en el archivo JSON exportado:

```javascript
{
  "recetas": [...],
  "ingredientes": [...],
  "unidades": {...},           // ✅ Unidades personalizadas
  "conversiones": {...},       // ✅ Conversiones personalizadas
  "configuracion": {
    "servicePercentage": 15,
    "profitPercentage": 30,
    "language": "es"
  },
  "exportDate": "2026-02-05T03:00:00.000Z",
  "version": "1.0"
}
```

---

## ☁️ Sincronización con la Nube (NUEVO)

### Cambios implementados:

### 1. **Función `uploadLocalData()`** - Actualizada
- Ahora sube también las unidades y conversiones a Supabase
- Se almacena en la tabla `user_config`
- Incluye: `custom_units`, `custom_conversions`, `service_percentage`, `profit_percentage`, `language`

### 2. **Función `syncDataWithSupabase()`** - Mejorada
- Sincroniza bidireccionalmente:
  - Ingredientes ✅
  - Recetas ✅
  - **Unidades personalizadas** ✅ (NUEVO)
  - **Conversiones personalizadas** ✅ (NUEVO)
  - Porcentajes de servicio y ganancia ✅ (NUEVO)
  - Idioma preferido ✅ (NUEVO)

### 3. **Nueva función `syncConfigToCloud()`**
- Función auxiliar que sincroniza solo la configuración
- Se llama automáticamente cuando el usuario:
  - Añade una unidad personalizada
  - Elimina una unidad personalizada
  - Restaura unidades por defecto
  - Añade una conversión
  - Elimina una conversión
  - Restaura conversiones por defecto

### 4. **Funciones actualizadas con auto-sincronización:**
- `addCustomUnit()` → Sincroniza después de añadir
- `deleteCustomUnit()` → Sincroniza después de eliminar
- `resetUnits()` → Sincroniza después de restaurar
- `addConversion()` → Sincroniza después de añadir
- `deleteConversion()` → Sincroniza después de eliminar
- `resetConversions()` → Sincroniza después de restaurar

---

## 🗄️ Estructura de Base de Datos

Se requiere crear la tabla `user_config` en Supabase con el siguiente esquema:

```sql
CREATE TABLE user_config (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  custom_units JSONB DEFAULT '{}'::jsonb,
  custom_conversions JSONB DEFAULT '{}'::jsonb,
  service_percentage NUMERIC(5,2) DEFAULT 0,
  profit_percentage NUMERIC(5,2) DEFAULT 0,
  language VARCHAR(10) DEFAULT 'es',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

Ver archivo `SUPABASE_SCHEMA.md` para el esquema completo con políticas RLS.

---

## 🔄 Flujo de Sincronización

### Cuando el usuario está **autenticado**:

1. **Al iniciar sesión**: Se descargan automáticamente las unidades y conversiones desde la nube
2. **Al modificar unidades/conversiones**: Se sincronizan automáticamente con la nube
3. **Al sincronizar manualmente**: Se actualizan todos los datos (ingredientes, recetas, unidades, conversiones)

### Cuando el usuario está **sin autenticar**:

- Los datos se guardan solo en `localStorage`
- No se sincroniza con la nube (función `syncConfigToCloud()` retorna sin hacer nada)

---

## 📝 Archivos Modificados

1. **`index.html`**:
   - Función `uploadLocalData()` - Añadido upload de configuración
   - Función `syncDataWithSupabase()` - Añadida sincronización de configuración
   - Nueva función `syncConfigToCloud()` - Sincronización auxiliar
   - Funciones de unidades y conversiones - Añadidas llamadas a `syncConfigToCloud()`

2. **`SUPABASE_SCHEMA.md`** (NUEVO):
   - Documentación completa del esquema de base de datos
   - Políticas RLS
   - Ejemplos de datos

---

## ✨ Beneficios

- ✅ **Sincronización automática**: No requiere acción manual del usuario
- ✅ **Backup en la nube**: Las unidades personalizadas están seguras
- ✅ **Multi-dispositivo**: Accede a tus unidades desde cualquier dispositivo
- ✅ **Exportación completa**: El JSON incluye toda la configuración
- ✅ **Importación completa**: Restaura todo desde un archivo JSON

---

## 🚀 Próximos Pasos

Para que funcione completamente:

1. **Crear la tabla `user_config` en Supabase** usando el SQL del archivo `SUPABASE_SCHEMA.md`
2. **Configurar las políticas RLS** para proteger los datos de cada usuario
3. **Probar la sincronización**:
   - Crear unidades personalizadas
   - Verificar que se suben a Supabase
   - Iniciar sesión desde otro dispositivo
   - Verificar que se descargan correctamente
