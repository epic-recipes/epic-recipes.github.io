-- =====================================================
-- Script de Migración para Recetario Épico
-- Tabla: user_config
-- Descripción: Almacena configuración personalizada del usuario
-- =====================================================

-- 1. Crear la tabla user_config
CREATE TABLE IF NOT EXISTS user_config (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  custom_units JSONB DEFAULT '{}'::jsonb NOT NULL,
  custom_conversions JSONB DEFAULT '{}'::jsonb NOT NULL,
  service_percentage NUMERIC(5,2) DEFAULT 0 CHECK (service_percentage >= 0 AND service_percentage <= 100),
  profit_percentage NUMERIC(5,2) DEFAULT 0 CHECK (profit_percentage >= 0 AND profit_percentage <= 100),
  language VARCHAR(10) DEFAULT 'es' NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- 2. Crear índice para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_user_config_user_id ON user_config(user_id);
CREATE INDEX IF NOT EXISTS idx_user_config_updated_at ON user_config(updated_at);

-- 3. Habilitar Row Level Security (RLS)
ALTER TABLE user_config ENABLE ROW LEVEL SECURITY;

-- 4. Eliminar políticas existentes si existen (para evitar duplicados)
DROP POLICY IF EXISTS "Users can view their own config" ON user_config;
DROP POLICY IF EXISTS "Users can insert their own config" ON user_config;
DROP POLICY IF EXISTS "Users can update their own config" ON user_config;
DROP POLICY IF EXISTS "Users can delete their own config" ON user_config;

-- 5. Crear políticas RLS
CREATE POLICY "Users can view their own config"
  ON user_config FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own config"
  ON user_config FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own config"
  ON user_config FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own config"
  ON user_config FOR DELETE
  USING (auth.uid() = user_id);

-- 6. Crear función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 7. Crear trigger para actualizar updated_at
DROP TRIGGER IF EXISTS update_user_config_updated_at ON user_config;
CREATE TRIGGER update_user_config_updated_at
  BEFORE UPDATE ON user_config
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- 8. Comentarios para documentación
COMMENT ON TABLE user_config IS 'Configuración personalizada del usuario incluyendo unidades, conversiones y preferencias';
COMMENT ON COLUMN user_config.user_id IS 'ID del usuario (referencia a auth.users)';
COMMENT ON COLUMN user_config.custom_units IS 'Unidades de medida personalizadas en formato JSON';
COMMENT ON COLUMN user_config.custom_conversions IS 'Conversiones entre unidades en formato JSON';
COMMENT ON COLUMN user_config.service_percentage IS 'Porcentaje de gastos de servicio (0-100)';
COMMENT ON COLUMN user_config.profit_percentage IS 'Porcentaje de ganancia deseado (0-100)';
COMMENT ON COLUMN user_config.language IS 'Código de idioma preferido (es, en, fr, etc.)';
COMMENT ON COLUMN user_config.created_at IS 'Fecha de creación del registro';
COMMENT ON COLUMN user_config.updated_at IS 'Fecha de última actualización (se actualiza automáticamente)';

-- =====================================================
-- Fin del script
-- =====================================================

-- Para verificar que todo se creó correctamente:
-- SELECT * FROM user_config;
