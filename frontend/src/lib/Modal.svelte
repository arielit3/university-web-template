<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
  // runes: use $props() to access incoming props
  let { open = false, title = '' } = $props();
  function close() {
    dispatch('close');
  }
  function onBackdrop(e) {
    if (e.target === e.currentTarget) close();
  }
  function handleBackdropKey(e) {
    // allow Enter or Space to trigger backdrop click, and Escape to close
    if (e.key === 'Enter' || e.key === ' ') {
      // emulate click
      onBackdrop(e);
    } else if (e.key === 'Escape') {
      close();
    }
  }
</script>

{#if open}
  <div class="modal-backdrop" onclick={onBackdrop} onkeydown={handleBackdropKey} role="button" tabindex="0">
    <div class="modal-card">
      <header class="modal-header">
        <h3>{title}</h3>
        <button class="close" onclick={close} aria-label="Cerrar">✕</button>
      </header>
      <div class="modal-body">
        <slot />
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: fixed;
    inset: 0;
    display: grid;
    place-items: center;
    background: rgba(2,6,23,0.5);
    z-index: 60;
    padding: 1.25rem;
  }
  .modal-card {
    width: 100%;
    max-width: 820px;
    background: white;
    border-radius: 12px;
    padding: 1rem;
    box-shadow: 0 20px 60px rgba(2,6,23,0.4);
  }
  .modal-header { display:flex; align-items:center; justify-content:space-between; gap:1rem }
  .modal-body { margin-top:0.75rem }
  .close { background:transparent; border:none; font-size:1.1rem; cursor:pointer }
</style>
