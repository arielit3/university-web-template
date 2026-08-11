<script>
  const { columns = [], rows = [] } = $props();
</script>

<table class="rt-table">
  <thead>
    <tr>
      {#if columns.length}
        <th>#</th>
        {#each columns as col}
          <th>{col.label || col}</th>
        {/each}
      {:else}
        <th>#</th>
        <th>Data</th>
      {/if}
    </tr>
  </thead>
  <tbody>
    {#each rows as row, i}
      <tr>
        <td>{i+1}</td>
        {#if columns.length}
            {#each columns as col}
              <td data-label={col.label ?? (col.key ?? col)}>{row[col.key ?? col]}</td>
            {/each}
        {:else}
          <td>{JSON.stringify(row)}</td>
        {/if}
      </tr>
    {/each}
  </tbody>
</table>

<style>
.rt-table {
  width: 100%;
  border-collapse: collapse;
}
.rt-table th, .rt-table td {
  text-align: left;
  padding: 8px 10px;
  border-bottom: 1px solid rgba(15,23,42,0.06);
  vertical-align: top;
}
.rt-table thead th {
  font-weight: 700;
  background: rgba(15,23,42,0.02);
}

@media (max-width: 680px) {
  .rt-table, .rt-table thead, .rt-table tbody, .rt-table th, .rt-table td, .rt-table tr {
    display: block;
  }
  .rt-table thead { display: none; }
  .rt-table tr { margin-bottom: 12px; border-radius: 8px; background: white; box-shadow: 0 6px 18px rgba(2,6,23,0.04); padding: 10px; }
  .rt-table td { display: flex; justify-content: space-between; padding: 8px 10px; border: none; }
  .rt-table td:before { content: attr(data-label); font-weight:700; margin-right:8px; }
}
</style>
