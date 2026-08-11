<script>
	let email = 'director@USN.com';
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
					<p class="subtext">
						Esta vista es la interfaz inicial del director. En la etapa siguiente
						se conectaran los botones a la logica y los datos reales.
					</p>
				</div>

				<div class="summary-row">
					<div>
						<p class="summary-label">Cuenta</p>
						<p>{email}</p>
					</div>
					<div>
						<p class="summary-label">Rol</p>
						<p>Director de carrera</p>
					</div>
				</div>

				<div class="action-grid">
					<button type="button" class="btn btn-secondary">Listar alumnos</button>
					<button type="button" class="btn btn-secondary">Listar aspirantes</button>
					<button type="button" class="btn btn-secondary">Listar docentes</button>
					<button type="button" class="btn btn-primary">Registrar aspirantes</button>
				</div>
			</div>
		</section>
	</main>
</div>

<style>
	:global(body) {
		margin: 0;
		font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
		background: #eef2ff;
		color: #0f172a;
	}

	:global(*) {
		box-sizing: border-box;
	}

	.page-shell {
		max-width: 1040px;
		margin: 0 auto;
		padding: 0.1rem 1.5rem 0;
	}

	.site-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem 0;
	}

	.brand {
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	.brand-icon {
		width: 50px;
		height: 50px;
		display: grid;
		place-items: center;
		border-radius: 16px;
		background: linear-gradient(135deg, #1d4ed8, #60a5fa);
		color: white;
		font-weight: 800;
		font-size: 0.95rem;
	}

	.btn {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: 0.95rem 1.6rem;
		border-radius: 999px;
		font-weight: 700;
		text-decoration: none;
		transition: transform 0.2s ease, box-shadow 0.2s ease;
		border: none;
		cursor: pointer;
	}

	.btn:hover {
		transform: translateY(-1px);
	}

	.btn-primary {
		background: #2563eb;
		color: white;
		box-shadow: 0 18px 40px rgba(37, 99, 235, 0.12);
	}

	.btn-secondary,
	.btn-outline {
		background: rgba(37, 99, 235, 0.06);
		color: #1e293b;
		border: 1px solid rgba(37, 99, 235, 0.18);
	}

	main {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: calc(100vh - 90px);
		padding: 0;
	}

	.dashboard-card {
		width: min(100%, 960px);
		padding: 2.5rem;
		border-radius: 32px;
		background: white;
		box-shadow: 0 30px 70px rgba(15, 23, 42, 0.08);
	}

	.dashboard-header {
		margin-bottom: 2rem;
	}

	.dashboard-header h1 {
		margin: 0.5rem 0 0;
		font-size: clamp(2rem, 3vw, 2.75rem);
	}

	.subtext {
		max-width: 680px;
		margin: 0.75rem 0 0;
		color: #475569;
		font-size: 1rem;
		line-height: 1.7;
	}

	.summary-row {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 1rem;
		margin-bottom: 2rem;
	}

	.summary-label {
		margin: 0 0 0.35rem;
		font-size: 0.9rem;
		font-weight: 700;
		color: #475569;
	}

	.summary-row p:last-child {
		margin: 0;
		font-size: 1rem;
		color: #0f172a;
	}

	.action-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 1rem;
	}

	.action-grid button {
		width: 100%;
		padding: 1rem 1.2rem;
		font-size: 1rem;
		text-align: center;
	}

	@media (max-width: 720px) {
		.action-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
