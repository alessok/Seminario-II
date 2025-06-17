# 🔒 INSTRUCCIONES DE SEGURIDAD PARA PROTECCIÓN DE DATOS

## ⚠️ IMPORTANTE: LEE ANTES DE HACER COMMIT PÚBLICO

Este proyecto contiene datos sensibles que NO deben ser subidos a repositorios públicos. Se han implementado las siguientes medidas de protección:

### 📋 **Archivos Protegidos por .gitignore:**

1. **Datos empresariales reales:**
   - `mapeo_pymes.csv` - Contiene DOI y razones sociales de empresas reales
   - `pymes_con_clusters.csv` - Datos de clustering con información empresarial
   - `combined_time_series_data.csv` - Series temporales con datos financieros
   - `ts_mensual_historico.csv` - Históricos financieros por empresa

2. **Documentos académicos:**
   - `S2_AS2_N2_AngeloMontes_AlessandroLedesma.docx`
   - `S2_AS2_N2_AngeloMontes_AlessandroLedesma.pdf`

3. **Datos procesados:**
   - `X_procesado_para_pca.csv`
   - `cluster_characteristics.csv`
   - `kmedoids_summary.csv`
   - `pronostico_prophet_cluster_*.csv`

### ✅ **Archivos Seguros para Commit Público:**

- `app.py` (sanitizado - sin información personal)
- `README.md` (sanitizado - nombres ocultos)
- `requirements.txt`
- `SemiCode.ipynb` (verificar antes del commit)
- `mapeo_pymes_demo.csv` (datos ficticios para demostración)
- `.gitignore`

### 🛡️ **Medidas Implementadas:**

1. **Información personal removida:** Nombres de estudiantes y códigos universitarios ocultos
2. **Datos empresariales protegidos:** Archivos con información real excluidos
3. **Datos de demostración:** Creado `mapeo_pymes_demo.csv` con información ficticia
4. **Documentación sanitizada:** README actualizado sin información sensible

### 📝 **Antes de Hacer Commit:**

1. Verificar que el `.gitignore` esté funcionando:
   ```bash
   git status
   ```

2. Asegurarse de que los archivos sensibles NO aparezcan en la lista

3. Revisar el contenido de `SemiCode.ipynb` para remover cualquier información sensible

4. Considerar si el notebook debe ser incluido o excluido del commit público

### 🚨 **EN CASO DE EMERGENCIA:**

Si accidentalmente subes información sensible:

1. **NO HAGAS PANIC**
2. Contacta inmediatamente al administrador del repositorio
3. Considera hacer el repositorio privado temporalmente
4. Usa `git filter-branch` o `BFG Repo-Cleaner` para limpiar el historial

### 📞 **Contacto de Emergencia:**

Para cualquier duda sobre seguridad de datos, contactar a los desarrolladores del proyecto.

---

**RECUERDA: Es mejor ser precavido que lamentar la exposición de datos sensibles.**
