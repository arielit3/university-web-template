<script>
	import { goto } from '$app/navigation';

	let userId = '';
	let password = '';
	const domain = '@USN.com';

	const email = $derived(() => userId.trim() ? `${userId.trim()}${domain}` : '');
	const canSubmit = $derived(() => userId.trim().length > 0 && password.trim().length > 0);

	function handleSubmit(event) {
		event.preventDefault();
		if (!canSubmit) return;
		goto('/director');
	}
</script>

<svelte:head>
	<title>Iniciar sesión | Universidad Sabatina</title>
</svelte:head>

<div class="page-shell login-shell">
	<header class="site-header">
		<div class="brand">
			<div class="brand-icon">USN</div>
			<div>
				<p class="brand-label">Universidad Sabatina</p>
				<p class="brand-subtitle">del Norte</p>
			</div>
		</div>

		<a class="btn btn-outline" href="/">Regresar</a>
	</header>

	<main>
		<section class="login-panel">
			<div class="login-card">
				<div class="login-header">
					<p class="eyebrow">Datos de acceso</p>
					<h1>Inicia sesión con tu cuenta</h1>
				</div>

				<form on:submit={handleSubmit}>
					<div class="field">
						<label for="userId">Matrícula o número de aspirante</label>
						<div class="input-suffix">
							<input
								id="userId"
								type="text"
								bind:value={userId}
								placeholder="US0000"
								autocomplete="username"
							/>
							<span>{domain}</span>
						</div>
						<p class="hint">
							Se enviará <strong>{email || 'US0000' + domain}</strong> al backend.
						</p>
					</div>

					<div class="field">
						<label for="password">Contraseña</label>
						<input
							id="password"
							type="password"
							bind:value={password}
							placeholder="Ingresa tu contraseña"
							autocomplete="current-password"
						/>
					</div>

					<button class="btn btn-primary" type="submit" disabled={!canSubmit}>
						Iniciar sesión
					</button>
				</form>
			</div>
		</section>
	</main>
</div>

<style>
	:global(body) {
		margin: 0;
		font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
		background: #f3f6fb;
		color: #0f172a;
	}

	:global(*) {
		box-sizing: border-box;
	}

	.page-shell {
		max-width: 980px;
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
		padding: 0.9rem 1.6rem;
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
		padding: 0.1rem 0 2rem;
	}

	.login-panel {
		width: 100%;
		max-width: 560px;
	}

	.login-card {
		padding: 2.5rem;
		border-radius: 32px;
		background: white;
		box-shadow: 0 30px 70px rgba(15, 23, 42, 0.08);
	}

	.login-header {
		margin-bottom: 2rem;
	}

	.login-header h1 {
		margin: 0.5rem 0 0;
		font-size: clamp(2rem, 3vw, 2.5rem);
	}

	.field {
		margin-bottom: 1.5rem;
	}

	.field label {
		display: block;
		margin-bottom: 0.75rem;
		font-weight: 700;
		color: #334155;
	}

	.input-suffix {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 0.75rem;
	}

	.input-suffix input {
		width: 100%;
		padding: 0.95rem 1rem;
		border-radius: 18px;
		border: 1px solid #cbd5e1;
		font-size: 1rem;
	}

	.input-suffix span {
		display: grid;
		place-items: center;
		padding: 0 1rem;
		border-radius: 18px;
		background: #eef2ff;
		color: #1e3a8a;
		font-size: 0.95rem;
		font-weight: 700;
	}

	.field input[type="password"] {
		width: 100%;
		padding: 0.95rem 1rem;
		border-radius: 18px;
		border: 1px solid #cbd5e1;
		font-size: 1rem;
	}

	.hint {
		margin: 0.75rem 0 0;
		color: #475569;
		font-size: 0.95rem;
	}

	button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	@media (max-width: 720px) {
		.page-shell {
			padding: 1rem;
		}

		.login-card {
			padding: 1.75rem;
		}

		.input-suffix {
			grid-template-columns: 1fr;
		}
	}
</style>
