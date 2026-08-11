<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import Modal from '$lib/Modal.svelte';
  import ResponsiveTable from '$lib/ResponsiveTable.svelte';

  let email = $state('director@USN.com');
  let nombre = $state('');
  let apellido = $state('');
  let userId = $state(null);

  let showListModal = $state(false);
  let listTitle = $state('');
  let listData = $state([]);
  let listColumns = $state([]);

  let showAspiranteModal = $state(false);
  let aspiranteForm = $state({
    idUsuario: '',
    searchCorreo: '',
    nombre: '',
    apellido: '',
    correo: '',
    contraseña: '',
    numFicha: '',
    periodo: '2026-A',
    carreraSolicita: '',
    puntosExamen: ''
  });
  let actionMsg = $state('');
  let careerOptions = $state([]);

  async function openAspiranteModal(){
    actionMsg = '';
    showAspiranteModal = true;
    try{
      const res = await fetch('http://localhost:8000/directores/mi-carrera', { headers: authHeaders() });
      if(res.ok){
        const c = await res.json();
        careerOptions = [c];
        aspiranteForm.carreraSolicita = c.nombreCarrera || aspiranteForm.carreraSolicita;
      }
    }catch(e){ console.error('error fetching carrera',e); }
  }

  function decodeJwtPayload(token) {
    try {
      const payload = token.split('.')[1];
      const padded = payload.padEnd(payload.length + (4 - (payload.length % 4)) % 4, '=');
      const json = atob(padded.replace(/-/g, '+').replace(/_/g, '/'));
      return JSON.parse(json);
    } catch (e) {
      return null;
    }
  }

  onMount(() => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        goto('/login');
        return;
      }
      const payload = decodeJwtPayload(token);
      if (!payload || payload.tipo !== 'director') {
        alert('Acceso restringido: necesita iniciar sesión como director');
        goto('/login');
        return;
      }
      email = payload.correo || payload.email || '';
      nombre = payload.nombre || '';
      apellido = payload.apellido || '';
      userId = payload.idUsuario || null;
      aspiranteForm.carreraSolicita = payload.nombreCarrera || '';
    } catch (err) {
      console.error(err);
      goto('/login');
    }
  });

  function authHeaders() {
    const t = localStorage.getItem('token');
    return t ? { Authorization: `Bearer ${t}`, 'Content-Type': 'application/json' } : { 'Content-Type': 'application/json' };
  }

  async function fetchList(path, title) {
    actionMsg = '';
    listTitle = title;
    listData = [];
    showListModal = true;
    try {
      const res = await fetch(`http://localhost:8000${path}`, { headers: authHeaders() });
      if (!res.ok) {
        const b = await res.json().catch(()=>({}));
        actionMsg = b.detail || 'Error al recuperar datos';
        return;
      }
      listData = await res.json();
      if (listData && listData.length) {
        if (path.includes('/materias')) {
          listColumns = [
            { key: 'idMateria', label: 'ID' },
            { key: 'nombreMateria', label: 'Nombre' },
            { key: 'objetivo', label: 'Objetivo' },
            { key: 'unidades', label: 'Unidades' }
          ];
        } else if (path.includes('/alumnos')) {
          listColumns = [
            { key: 'idAlumno', label: 'ID' },
            { key: 'idUsuario', label: 'Matrícula' },
            { key: 'idGrupo', label: 'Grupo' },
            { key: 'promedioPrep', label: 'Promedio' }
          ];
        } else if (path.includes('/docentes')) {
          listColumns = [
            { key: 'idDocente', label: 'ID' },
            { key: 'idUsuario', label: 'Matrícula' },
            { key: 'idCarrera', label: 'Carrera' },
            { key: 'nivelEstudios', label: 'Nivel' },
            { key: 'turno', label: 'Turno' }
          ];
        } else if (path.includes('/grupos')) {
          listColumns = [
            { key: 'idGrupo', label: 'ID' },
            { key: 'nombreGrupo', label: 'Nombre' },
            { key: 'periodo', label: 'Periodo' },
            { key: 'numAlumnos', label: 'Alumnos' }
          ];
        } else {
          listColumns = Object.keys(listData[0]).map(k => ({ key: k, label: k }));
        }
      }
    } catch (e) {
      console.error(e);
      actionMsg = 'Error de red';
    }
  }

  async function submitAspirante() {
    actionMsg = '';
    try {
      // if idUsuario present, create aspirante for existing user
      if (aspiranteForm.idUsuario) {
        if (!aspiranteForm.numFicha || !aspiranteForm.carreraSolicita) { actionMsg='Completa los campos obligatorios'; return; }
        const payload = {
          idUsuario: Number(aspiranteForm.idUsuario),
          numFicha: Number(aspiranteForm.numFicha),
          periodo: aspiranteForm.periodo,
          carreraSolicita: aspiranteForm.carreraSolicita,
          puntosExamen: Number(aspiranteForm.puntosExamen || 0)
        };
        const res = await fetch('http://localhost:8000/directores/crear-aspirante', {
          method: 'POST',
          headers: authHeaders(),
          body: JSON.stringify(payload)
        });
        if (!res.ok) { const b = await res.json().catch(()=>({})); actionMsg = b.detail || 'Error al crear aspirante'; return; }
        actionMsg = 'Aspirante creado correctamente (usuario existente)';
      } else {
        // create new usuario + aspirante
        if (!aspiranteForm.nombre || !aspiranteForm.apellido || !aspiranteForm.correo || !aspiranteForm.contraseña || !aspiranteForm.numFicha || !aspiranteForm.carreraSolicita) {
          actionMsg = 'Completa los datos de usuario y aspirante para crear nuevo aspirante';
          return;
        }
        const payload = {
          nombre: aspiranteForm.nombre,
          apellido: aspiranteForm.apellido,
          correo: aspiranteForm.correo,
          contraseña: aspiranteForm.contraseña,
          numFicha: Number(aspiranteForm.numFicha),
          periodo: aspiranteForm.periodo,
          carreraSolicita: aspiranteForm.carreraSolicita,
          puntosExamen: Number(aspiranteForm.puntosExamen || 0)
        };
        const res = await fetch('http://localhost:8000/directores/registrar-aspirante', {
          method: 'POST',
          headers: authHeaders(),
          body: JSON.stringify(payload)
        });
        if (!res.ok) { const b = await res.json().catch(()=>({})); actionMsg = b.detail || 'Error al crear usuario y aspirante'; return; }
        actionMsg = 'Usuario y aspirante creados correctamente';
      }
      setTimeout(() => { showAspiranteModal = false; actionMsg = ''; }, 1000);
    } catch (e) {
      console.error(e);
      actionMsg = 'Error de red';
    }
  }
</script>

<svelte:head>
  <title>Panel del director | Universidad Sabatina</title>
</svelte:head>

<div class="page-shell dashboard-shell">
  <header class="site-header">
    <div class="brand">
      <div class="brand-icon">USN</div>
      <div>
        <p class="brand-label">Universidad Sabatina</p>
        <p class="brand-subtitle">Panel director</p>
      </div>
    </div>

    <a class="btn btn-outline" href="/login">Cerrar sesión</a>
  </header>

  <main>
    <section class="dashboard-panel">
      <div class="dashboard-card">
        <div class="dashboard-header">
          <p class="eyebrow">Bienvenido</p>
          <h1>Director de carrera</h1>
          <p class="subtext">Interfaz del director: listar recursos y registrar aspirantes.</p>
        </div>

        <div class="summary-row">
          <div>
            <p class="summary-label">Cuenta</p>
            <p>{nombre} {apellido} &lt;{email}&gt;</p>
          </div>
          <div>
            <p class="summary-label">Rol</p>
            <p>Director de carrera</p>
          </div>
        </div>

        <div class="action-grid">
          <button type="button" class="btn btn-secondary" onclick={() => fetchList('/directores/alumnos','Alumnos de mi carrera')}>Listar alumnos</button>
          <button type="button" class="btn btn-secondary" onclick={() => fetchList('/directores/docentes','Docentes de mi carrera')}>Listar docentes</button>
          <button type="button" class="btn btn-secondary" onclick={() => fetchList('/directores/materias','Materias de mi carrera')}>Listar materias</button>
          <button type="button" class="btn btn-primary" onclick={openAspiranteModal}>Registrar aspirantes</button>
        </div>

        {#if showListModal}
          <Modal open={showListModal} title={listTitle} on:close={() => showListModal = false}>
            {#if actionMsg}
              <p style="color:tomato">{actionMsg}</p>
            {:else if listData.length === 0}
              <p>No hay elementos.</p>
            {:else}
              <ResponsiveTable columns={listColumns} rows={listData} />
            {/if}
          </Modal>
        {/if}

        {#if showAspiranteModal}
          <Modal open={showAspiranteModal} title="Registrar aspirante" on:close={() => { showAspiranteModal=false; actionMsg=''; }}>
            <form onsubmit={e => { e.preventDefault(); submitAspirante(); }}>
              <div style="display:grid;gap:0.6rem">
                <label for="asp-search">Buscar usuario por correo (si ya existe)</label>
                <div style="display:flex;gap:0.5rem">
                  <input id="asp-search" placeholder="correo@ejemplo.com" bind:value={aspiranteForm.searchCorreo} />
                  <button type="button" class="btn btn-secondary" onclick={async () => {
                    actionMsg='';
                    try{
                      const res = await fetch(`http://localhost:8000/directores/buscar-usuario?correo=${encodeURIComponent(aspiranteForm.searchCorreo)}`, { headers: authHeaders() });
                      if(!res.ok){ const b=await res.json().catch(()=>({})); actionMsg=b.detail||'No encontrado'; return; }
                      const u = await res.json();
                      aspiranteForm.idUsuario = u.idUsuario;
                      actionMsg = `Usuario encontrado: ${u.nombre} ${u.apellido} (id ${u.idUsuario})`;
                    }catch(e){ console.error(e); actionMsg='Error búsqueda'; }
                  }}>Buscar</button>
                </div>
                <small>Si no existe, completa los campos de usuario para crearlo automáticamente.</small>

                <label for="asp-nombre">Nombre</label>
                <input id="asp-nombre" bind:value={aspiranteForm.nombre} placeholder="Nombre" />
                <label for="asp-apellido">Apellido</label>
                <input id="asp-apellido" bind:value={aspiranteForm.apellido} placeholder="Apellido" />
                <label for="asp-correo">Correo</label>
                <input id="asp-correo" bind:value={aspiranteForm.correo} placeholder="correo@USN.com" />
                <label for="asp-password">Contraseña</label>
                <input id="asp-password" bind:value={aspiranteForm.contraseña} type="password" />

                <label for="asp-idUsuario">Matrícula (idUsuario) — si buscaste, se llenará</label>
                <input id="asp-idUsuario" bind:value={aspiranteForm.idUsuario} type="number" />

                <label for="asp-numFicha">Núm. ficha</label>
                <input id="asp-numFicha" bind:value={aspiranteForm.numFicha} type="number" required />
                <label for="asp-periodo">Periodo</label>
                <input id="asp-periodo" bind:value={aspiranteForm.periodo} type="text" />
                <label for="asp-carrera">Carrera solicita</label>
                <input id="asp-carrera" bind:value={aspiranteForm.carreraSolicita} type="text" required />
                <label for="asp-puntos">Puntos examen</label>
                <input id="asp-puntos" bind:value={aspiranteForm.puntosExamen} type="number" min="0" max="100" />

                <div style="display:flex;gap:0.5rem;margin-top:0.6rem">
                  <button class="btn btn-primary" type="submit">Registrar</button>
                  <button type="button" class="btn btn-outline" onclick={() => { showAspiranteModal=false; actionMsg=''; }}>Cancelar</button>
                </div>
                {#if actionMsg}
                  <p style="color:tomato">{actionMsg}</p>
                {/if}
              </div>
            </form>
          </Modal>
        {/if}

      </div>
    </section>
  </main>
</div>

<style>
  :global(body) { margin: 0; font-family: Inter, system-ui, -apple-system, 'Segoe UI', sans-serif; background: #eef2ff; color: #0f172a; }
  :global(*) { box-sizing: border-box; }
  .page-shell { max-width: 1040px; margin: 0 auto; padding: 0.1rem 1.5rem 0; }
  .site-header { display:flex; justify-content:space-between; align-items:center; padding:0.75rem 0; }
  .brand { display:flex; gap:1rem; align-items:center; }
  .brand-icon { width:50px; height:50px; display:grid; place-items:center; border-radius:12px; background:linear-gradient(135deg,#1d4ed8,#60a5fa); color:white; font-weight:800 }
  .btn { display:inline-flex; align-items:center; justify-content:center; padding:0.95rem 1.6rem; border-radius:999px; font-weight:700; border:none; cursor:pointer }
  .btn-primary { background:#2563eb; color:#fff }
  .btn-secondary, .btn-outline { background: rgba(37,99,235,0.06); color:#1e293b; border:1px solid rgba(37,99,235,0.18) }
  .dashboard-card { width:min(100%,960px); padding:2.5rem; border-radius:32px; background:white; box-shadow:0 30px 70px rgba(15,23,42,0.08) }
  .action-grid { display:grid; grid-template-columns: repeat(2,1fr); gap:1rem }
  .summary-row { display:grid; grid-template-columns: repeat(2,1fr); gap:1rem; margin-bottom:1rem }
  @media (max-width:720px) { .action-grid { grid-template-columns:1fr } }
</style>
