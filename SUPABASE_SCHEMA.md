# Estructura de Base de Datos Supabase para Recetario Épico

## Tabla: `user_config`

Esta tabla almacena la configuración personalizada de cada usuario, incluyendo unidades de medida, conversiones y preferencias.

### Esquema SQL

```sql
-- Crear tabla user_config
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

-- Índice para mejorar rendimiento
CREATE INDEX idx_user_config_user_id ON user_config(user_id);

-- Política RLS (Row Level Security) para que cada usuario solo vea su configuración
ALTER TABLE user_config ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own config"
  ON user_config FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own config"
  ON user_config FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own config"
  ON user_config FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own config"
  ON user_config FOR DELETE
  USING (auth.uid() = user_id);
```

## Campos de la tabla

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `user_id` | UUID | ID del usuario (clave primaria, referencia a auth.users) |
| `custom_units` | JSONB | Objeto JSON con unidades personalizadas. Ejemplo: `{"taza": "Taza", "pizca": "Pizca"}` |
| `custom_conversions` | JSONB | Objeto JSON con conversiones personalizadas. Ejemplo: `{"kilogramo-gramo": 1000, "gramo-kilogramo": 0.001}` |
| `service_percentage` | NUMERIC(5,2) | Porcentaje de gastos de servicio (0-100) |
| `profit_percentage` | NUMERIC(5,2) | Porcentaje de ganancia deseado (0-100) |
| `language` | VARCHAR(10) | Código de idioma preferido (es, en, fr, etc.) |
| `created_at` | TIMESTAMP | Fecha de creación del registro |
| `updated_at` | TIMESTAMP | Fecha de última actualización |

## Ejemplo de datos

```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "custom_units": {
    "taza": "Taza",
    "cucharada": "Cucharada",
    "pizca": "Pizca"
  },
  "custom_conversions": {
    "kilogramo-gramo": 1000,
    "gramo-kilogramo": 0.001,
    "litro-mililitro": 1000,
    "mililitro-litro": 0.001,
    "taza-mililitro": 240,
    "mililitro-taza": 0.004166
  },
  "service_percentage": 15.00,
  "profit_percentage": 30.00,
  "language": "es",
  "created_at": "2026-02-05T03:00:00Z",
  "updated_at": "2026-02-05T03:15:00Z"
}
```

## Notas importantes

1. **JSONB vs JSON**: Se usa JSONB para mejor rendimiento en consultas y actualizaciones.
2. **Row Level Security (RLS)**: Asegura que cada usuario solo pueda acceder a su propia configuración.
3. **ON DELETE CASCADE**: Si se elimina un usuario, su configuración también se elimina automáticamente.
4. **Sincronización bidireccional**: La app sincroniza automáticamente:
   - Al iniciar sesión
   - Al modificar unidades o conversiones
   - Al hacer clic en "Sincronizar manualmente"

## Integración con tablas existentes

Asegúrate de que también existan estas tablas (ya deberían estar creadas):

- `ingredients` - Para almacenar ingredientes del usuario
- `recipes` - Para almacenar recetas del usuario

Ambas deben tener políticas RLS similares para proteger los datos de cada usuario.
