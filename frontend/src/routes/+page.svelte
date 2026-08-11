<svelte:head>
	<title>Universidad Sabatina del Norte</title>
</svelte:head>

<div class="page-shell">
	<header class="site-header">
		<div class="brand">
			<div class="brand-icon">USN</div>
			<div>
				<p class="brand-label">Universidad Sabatina</p>
				<p class="brand-subtitle">del Norte</p>
			</div>
		</div>

		<a class="btn btn-outline" href="/login" aria-label="Iniciar sesión">Iniciar sesión</a>
	</header>

	<main>
		<section class="hero">
			<div class="hero-copy">
				<p class="eyebrow">Educación superior · modalidad sabatina</p>
				<h1>Tu profesión, tu tiempo, tu sábado.</h1>
				<p class="hero-text">
					Estudia una carrera universitaria sin renunciar a tu trabajo o a tu familia.
					Clases presenciales solo los sábados, diseñadas para adultos que buscan crecer
					con un ritmo real y práctico.
				</p>

				<div class="hero-actions">
					<a class="btn btn-primary" href="#historia">Nuestra historia</a>
					<a class="btn btn-secondary" href="#ubicacion">Cómo llegar</a>
				</div>

				<div class="stats-grid">
					<div>
						<strong>25+</strong>
						<p>Años de trayectoria</p>
					</div>
					<div>
						<strong>8,500+</strong>
						<p>Egresados</p>
					</div>
					<div>
						<strong>20</strong>
						<p>Carreras</p>
					</div>
				</div>
			</div>

			<div class="hero-card">
				<div class="hero-card-label">Inscríbete</div>
				<h2>Tu futuro profesional comienza el sábado.</h2>
				<p>
					En Universidad Sabatina del Norte combinamos experiencia laboral, estudio serio y clases
				
en horarios compatibles con tu vida diaria.
				</p>
				<div class="hero-card-footer">
					<span>Clases presenciales</span>
					<span>7:00 AM - 5:00 PM</span>
				</div>
			</div>
		</section>

		<section id="historia" class="story-section">
			<div class="section-header">
				<p class="eyebrow">Nuestra historia</p>
				<h2>El proyecto educativo que respeta tu tiempo</h2>
			</div>
			<p class="story-copy">
				Desde sus inicios, Universidad Sabatina del Norte nació para acompañar a las
				personas que no pueden estudiar de lunes a viernes. Aquí cada sábado es una oportunidad
				para avanzar, conectar con docentes activos y construir una carrera sin interrumpir
				nuestra vida profesional.
			</p>

			<div class="story-grid">
				<div class="story-card">
					<h3>Aprendizaje flexible</h3>
					<p>
						Nuestro modelo sabatino permite que adultos y profesionales estudien de forma
					compatible con sus obligaciones laborales y familiares.
					</p>
				</div>
				<div class="story-card">
					<h3>Perfil práctico</h3>
					<p>
						Diseñamos programas que impulsan habilidades aplicables desde el primer día,
					con materias y proyectos orientados al mundo real.
					</p>
				</div>
				<div class="story-card">
					<h3>Comunidad adulta</h3>
					<p>
						Estás entre personas con objetivos claros y experiencia previa, en un ambiente
					de respeto, colaboración y crecimiento compartido.
					</p>
				</div>
			</div>
		</section>

		<section id="ubicacion" class="location-section">
			<div class="section-header">
				<p class="eyebrow">Cómo llegar</p>
				<h2>Encuéntranos en el norte de la ciudad</h2>
			</div>
			<div class="map-card">
				<iframe
					src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3393.1691964648776!2d-106.437568823786!3d31.738582374114863!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x86e75bfc9c9b87c1%3A0xa4c938a4e37dab5e!2sMotel%20Mi%20Ranchito!5e0!3m2!1ses!2smx!4v1786425389255!5m2!1ses!2smx"
					loading="lazy"
					referrerpolicy="strict-origin-when-cross-origin"
					allowfullscreen
				></iframe>
			</div>
		</section>
	</main>

	<footer class="site-footer">
		<div>© 2026 Universidad Sabatina del Norte</div>
		<div>contacto@USN.edu | +52 (656) 766 3221</div>
	</footer>
</div>

<style>
	:global(body) {
		margin: 0;
		font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
		background: #f7f9ff;
		color: #0f172a;
		line-height: 1.6;
	}

	:global(*) {
		box-sizing: border-box;
	}

	.page-shell {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 1.5rem 2rem;
	}

	.site-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1.5rem 0;
	}

	.brand {
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	.brand-icon {
		width: 52px;
		height: 52px;
		display: grid;
		place-items: center;
		border-radius: 16px;
		background: linear-gradient(135deg, #1d4ed8, #60a5fa);
		color: white;
		font-weight: 800;
		font-size: 0.95rem;
	}

	.brand-label {
		margin: 0;
		font-size: 1rem;
		font-weight: 800;
	}

	.brand-subtitle {
		margin: 0;
		font-size: 0.85rem;
		color: #475569;
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
		display: grid;
		gap: 3.5rem;
	}

	.hero {
		display: grid;
		grid-template-columns: minmax(0, 1.2fr) minmax(320px, 1fr);
		gap: 2rem;
		align-items: center;
		padding: 3rem 0 4rem;
	}

	.hero-copy {
		max-width: 620px;
	}

	.eyebrow {
		margin: 0 0 1rem;
		font-size: 0.85rem;
		font-weight: 700;
		letter-spacing: 0.18em;
		text-transform: uppercase;
		color: #2563eb;
	}

	h1 {
		margin: 0;
		font-size: clamp(2.5rem, 4vw, 4.5rem);
		line-height: 1.02;
	}

	.hero-text {
		margin: 1.5rem 0 2rem;
		color: #334155;
		font-size: 1.05rem;
		max-width: 42rem;
	}

	.hero-actions {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
	}

	.stats-grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 1rem;
		margin-top: 2rem;
	}

	.stats-grid div {
		padding: 1.25rem;
		border-radius: 24px;
		background: white;
		box-shadow: 0 15px 35px rgba(15, 23, 42, 0.06);
	}

	.stats-grid strong {
		display: block;
		font-size: 1.75rem;
		color: #0f172a;
	}

	.stats-grid p {
		margin: 0.5rem 0 0;
		color: #64748b;
	}

	.hero-card {
		padding: 2rem;
		border-radius: 32px;
		background: linear-gradient(180deg, rgba(59, 130, 246, 0.12), white 55%);
		box-shadow: 0 30px 70px rgba(15, 23, 42, 0.08);
	}

	.hero-card-label {
		display: inline-flex;
		padding: 0.5rem 0.95rem;
		border-radius: 999px;
		background: rgba(37, 99, 235, 0.12);
		color: #1e40af;
		font-weight: 700;
		font-size: 0.8rem;
		margin-bottom: 1.25rem;
	}

	.hero-card h2 {
		margin: 0;
		font-size: 2rem;
		line-height: 1.2;
	}

	.hero-card p {
		margin: 1rem 0 0;
		color: #475569;
	}

	.hero-card-footer {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
		margin-top: 2rem;
		font-size: 0.95rem;
		color: #1e293b;
	}

	.section-header {
		margin-bottom: 1.75rem;
	}

	.section-header h2 {
		margin: 0.5rem 0 0;
		font-size: clamp(2rem, 3vw, 2.75rem);
	}

	.story-section,
	.location-section {
		padding: 3rem 0;
	}

	.story-copy {
		max-width: 760px;
		color: #475569;
		font-size: 1rem;
		margin-bottom: 2rem;
	}

	.story-grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 1rem;
	}

	.story-card {
		background: white;
		padding: 1.8rem;
		border-radius: 24px;
		box-shadow: 0 20px 55px rgba(15, 23, 42, 0.06);
	}

	.story-card h3 {
		margin: 0 0 0.75rem;
		font-size: 1.15rem;
	}

	.story-card p {
		margin: 0;
		color: #475569;
	}

	.map-card {
		background: white;
		border-radius: 28px;
		overflow: hidden;
		box-shadow: 0 25px 70px rgba(15, 23, 42, 0.08);
		min-height: 480px;
	}

	.map-card iframe {
		width: 100%;
		height: 100%;
		min-height: 440px;
		border: 0;
	}

	.site-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		flex-wrap: wrap;
		gap: 1rem;
		padding: 1.5rem 0;
		margin-top: 2rem;
		border-top: 1px solid rgba(148, 163, 184, 0.16);
		font-size: 0.95rem;
		color: #475569;
	}

	@media (max-width: 900px) {
		.hero {
			grid-template-columns: 1fr;
		}

		.stats-grid {
			grid-template-columns: 1fr 1fr;
		}
	}

	@media (max-width: 720px) {
		.page-shell {
			padding: 0 1rem 1.5rem;
		}

		.site-header {
			flex-direction: column;
			align-items: stretch;
			gap: 1rem;
		}

		.hero-card-footer {
			flex-direction: column;
			align-items: flex-start;
		}

		.stats-grid {
			grid-template-columns: 1fr;
		}

		.story-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
