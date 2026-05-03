# RHCSA 10 - Automation Scripts

Este repositorio contiene un conjunto de scripts y configuraciones automatizadas utilizadas para practicar y resolver escenarios típicos del examen **RHCSA (Red Hat Certified System Administrator)**.

El código está organizado en dos directorios principales, correspondientes a los dos nodos (servidores) que comúnmente se configuran durante las prácticas del examen:

---

## 📁 `nodo1/`
Contiene los scripts orientados a la configuración inicial del sistema, redes, servicios compartidos y paquetería en el primer servidor.

**Escenarios cubiertos:**
- **Configuración de Red:** Scripts para levantar y configurar las interfaces de red estáticas/dinámicas (ej. `add-enp0s3.sh`, `add-enp0s8.sh`).
- **Repositorios y Paquetería:** Configuración de repositorios locales (`BaseOS` y `AppStream`).
- **Flatpak:** Automatización de la instalación de Flatpak, adición del repositorio de *Flathub* e instalación de aplicaciones para usuarios específicos (ej. `vscodium`).
- **NFS y Autofs:** Scripts para exportar carpetas compartidas por red y configurar el montaje automático bajo demanda en los clientes.

---

## 📁 `nodo2/`
Se enfoca en tareas avanzadas de almacenamiento local, creación de particiones, gestión de LVM (Logical Volume Manager) y sistemas de archivos. *Incluye protecciones mediante discos virtuales (`loop devices`) para probar escenarios de discos de forma segura sin romper el servidor.*

**Escenarios cubiertos:**
- **`create-swap-file/`**: Utiliza automatización de `fdisk` para crear una tabla GPT y una partición de Linux Swap de 800 MiB, formateándola y configurándola de manera persistente en `/etc/fstab`.
- **`lv-adjust/`**: Crea un entorno de pruebas LVM (Volume Group y Logical Volume) simulado. Demuestra cómo montar particiones con formato `XFS` y la manera correcta de redimensionar el disco con `lvresize` y expandir el sistema de ficheros en caliente con `xfs_growfs`.
- **`create-lv/`**: Muestra la inicialización de discos físicos (`pvcreate`), creación de VGs especificando el tamaño de los Physical Extents (`vgcreate -s 16M`), la creación de LVs específicos (`lvcreate`), formateo en `ext3` y montaje automatizado.

---

## Modo de Uso General
Cada directorio dentro de los nodos suele contener un script de creación (`*_create.py` o `.sh`) y un script de destrucción o limpieza (`*_destroy.py`).

1. Para probar un escenario, ingresa a su directorio y ejecuta el script principal.
2. Los scripts basados en Python imprimirán en pantalla cada comando real de `bash` antes de ejecutarlo para que puedas estudiar qué está haciendo por detrás.
3. Al terminar tu práctica, ejecuta el script `*_destroy.py` para deshacer los cambios, borrar las configuraciones de `/etc/fstab` y dejar el servidor limpio.
