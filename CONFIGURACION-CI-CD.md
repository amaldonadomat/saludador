# Configuración CI/CD para alpyro-saludador

Este documento explica cómo está configurado el sistema de CI/CD del proyecto y qué pasos debes seguir para completar la configuración.

## Resumen del Sistema

El proyecto implementa un sistema de CI/CD completo con tres workflows de GitHub Actions:

1. **PR Validation** - Valida pull requests antes de mergear
2. **Release** - Publica automáticamente releases estables en TestPyPI
3. **Pre-Release** - Permite publicar versiones de desarrollo manualmente

## Versionado Automático con setuptools-scm

El proyecto usa `setuptools-scm` para gestionar versiones automáticamente basándose en tags de Git:

- **En un tag exacto** (ej. `v0.1.0`): versión `0.1.0`
- **Commits después del tag**: versión `.post` (ej. `0.1.0.post0`, `0.1.0.post1`)
- **En rama sin merge**: versión `.dev` con distancia y hash

### Configuración en pyproject.toml

```toml
[tool.setuptools_scm]
write_to = "src/alpyro_saludador/_version.py"
version_scheme = "post-release"
local_scheme = "no-local-version"
```

## Workflows

### 1. PR Validation (`.github/workflows/pr-validation.yml`)

**Trigger**: Pull request a `main`

**Validaciones**:
- ✅ Título del PR debe contener `[patch]`, `[minor]` o `[major]`
- ✅ Lint con `ruff`
- ✅ Tests con `pytest`
- ✅ Cobertura mínima del 80%

**Formato de títulos de PR**:
```
[patch] Fix saludo function bug
[minor] Add German language support
[major] Refactor API - breaking changes
```

### 2. Release (`.github/workflows/release.yml`)

**Trigger**: Push a `main` (después de mergear un PR)

**Proceso**:
1. Extrae el tipo de versión del mensaje de commit (`[patch]`, `[minor]`, `[major]`)
2. Calcula el nuevo tag semver basándose en el último tag
3. Crea y pushea el nuevo tag
4. Construye el paquete (setuptools-scm usa el tag para la versión)
5. Publica en TestPyPI
6. Crea un GitHub Release

**Ejemplo**:
- Último tag: `v0.1.0`
- PR con título: `[minor] Add new language support`
- Resultado:
  - Tag `v0.2.0` creado
  - Paquete `alpyro-saludador==0.2.0` publicado en TestPyPI
  - GitHub Release creado

### 3. Pre-Release (`.github/workflows/pre-release.yml`)

**Trigger**: Manual (`workflow_dispatch` desde GitHub Actions)

**Proceso**:
1. Ejecutas el workflow manualmente desde GitHub
2. setuptools-scm genera automáticamente una versión `.post` basada en:
   - Último tag
   - Número de commits desde el tag
   - Hash del commit actual
3. Construye y publica en TestPyPI

**Ejemplo de versión generada**: `0.2.0.post5` (5 commits después del tag v0.2.0)

## Configuración Requerida

### 1. Crear Token de TestPyPI

1. Ve a [TestPyPI](https://test.pypi.org/)
2. Crea una cuenta si no tienes
3. Ve a Account Settings → API tokens
4. Crea un nuevo token:
   - **Token name**: `github-actions-alpyro-saludador`
   - **Scope**: "Entire account" (para el primer upload) o específico del proyecto
5. Copia el token (empieza con `pypi-...`)

### 2. Configurar GitHub Secret

1. Ve a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Configura:
   - **Name**: `TESTPYPI_API_TOKEN`
   - **Secret**: Pega el token de TestPyPI
5. Click "Add secret"

### 3. Verificar que el repositorio tenga permisos de escritura

1. Ve a Settings → Actions → General
2. En "Workflow permissions":
   - Selecciona "Read and write permissions"
   - Marca "Allow GitHub Actions to create and approve pull requests"
3. Click "Save"

## Flujo de Trabajo Completo

### Para un Release Estable

1. **Crear rama de feature**:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   # Hacer cambios...
   git add .
   git commit -m "Implementar nueva funcionalidad"
   git push origin feature/nueva-funcionalidad
   ```

2. **Crear Pull Request**:
   - Título debe incluir `[patch]`, `[minor]` o `[major]`
   - Ejemplo: `[minor] Add German language support`
   - El workflow de validación se ejecutará automáticamente

3. **Code Review y Merge**:
   - Una vez aprobado, mergea el PR a `main`
   - El workflow de release se ejecutará automáticamente:
     - Crea tag `v0.2.0`
     - Publica en TestPyPI
     - Crea GitHub Release

4. **Verificar publicación**:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple alpyro-saludador==0.2.0
   ```

### Para un Pre-Release (Testing)

1. **Hacer commits sin mergear**:
   ```bash
   git checkout -b experiment/test-feature
   # Hacer cambios...
   git add .
   git commit -m "Experimental feature"
   git push origin experiment/test-feature
   ```

2. **Ejecutar Pre-Release workflow**:
   - Ve a Actions → Pre-Release (Manual)
   - Click "Run workflow"
   - Selecciona tu rama
   - Añade descripción opcional
   - Click "Run workflow"

3. **El workflow genera versión automáticamente**:
   - Ejemplo: `0.2.0.post3` (si estás 3 commits después del tag v0.2.0)
   - Publica en TestPyPI

4. **Probar la pre-release**:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple alpyro-saludador==0.2.0.post3
   ```

## Versionado Semántico

Usa las siguientes guías para elegir el tipo de versión:

### `[patch]` - Incrementa Z (x.y.Z)
- Correcciones de bugs
- Pequeños ajustes
- No cambia la API pública
- Ejemplo: `0.1.0` → `0.1.1`

### `[minor]` - Incrementa Y (x.Y.0)
- Nuevas funcionalidades
- Cambios compatibles hacia atrás
- Deprecaciones
- Ejemplo: `0.1.5` → `0.2.0`

### `[major]` - Incrementa X (X.0.0)
- Cambios incompatibles con versiones anteriores
- Refactorización de API
- Eliminación de funcionalidades deprecadas
- Ejemplo: `0.9.0` → `1.0.0`

## Testing Local

Antes de crear un PR, puedes probar el build localmente:

```bash
# Activar entorno virtual
source venv/bin/activate

# Construir el paquete
python -m build

# Ver la versión que se generará
python -c "from setuptools_scm import get_version; print(get_version())"

# Instalar localmente para probar
pip install -e .
```

## Verificar Estado de Workflows

1. Ve a la pestaña "Actions" en GitHub
2. Verás todos los workflows ejecutados
3. Click en cualquiera para ver los logs detallados
4. Los workflows fallidos aparecerán en rojo

## Solución de Problemas

### El workflow de release no se ejecuta
- Verifica que el commit message contenga `[patch]`, `[minor]` o `[major]`
- Verifica que sea un push a `main` (no un PR abierto)

### Error "403 Forbidden" al publicar en TestPyPI
- Verifica que el secret `TESTPYPI_API_TOKEN` esté configurado
- Verifica que el token de TestPyPI sea válido
- Si es el primer upload, el token debe tener scope "Entire account"

### Versión incorrecta generada
- Verifica que tengas al menos un tag en el repositorio: `git tag`
- Verifica que setuptools-scm esté instalado: `pip install setuptools-scm`
- Prueba localmente: `python -c "from setuptools_scm import get_version; print(get_version())"`

### Tests fallan en CI pero pasan localmente
- Verifica que todas las dependencias estén en `pyproject.toml`
- Verifica que no estés usando paths absolutos
- Revisa los logs del workflow para más detalles

## Próximos Pasos

1. ✅ Configurar el token de TestPyPI en GitHub Secrets
2. ✅ Crear un PR de prueba con formato `[patch] Test CI/CD setup`
3. ✅ Verificar que todos los workflows pasen
4. ✅ Mergear y verificar que se cree el release automáticamente
5. ✅ Probar instalar el paquete desde TestPyPI

## Referencias

- [TestPyPI](https://test.pypi.org/)
- [setuptools-scm Documentation](https://setuptools-scm.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Semantic Versioning](https://semver.org/)
