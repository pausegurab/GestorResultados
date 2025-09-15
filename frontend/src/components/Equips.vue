<script setup>
import { ref, onMounted, computed } from 'vue'
import EquipService from '../services/EquipsServices.js'
import CountryService from '../services/CountryServices.js'

const equips = ref([])
const paisos = ref([])
const showModal = ref(false)
const form = ref({
  nom: '',
  sigles: '',
  foto: '',
  pais_id: null
})
const menuOpen = ref(null)

const fetchEquips = async () => {
  equips.value = await EquipService.getAll()
}
const fetchPaisos = async () => {
  paisos.value = await CountryService.getAll()
}

onMounted(() => {
  fetchEquips()
  fetchPaisos()
})

function obrirModal() {
  form.value = { nom: '', sigles: '', foto: '', pais_id: null }
  showModal.value = true
}

function tancarModal() {
  showModal.value = false
}

async function crearEquip() {
  const nom = form.value.nom
  const sigles = form.value.sigles.trim()
  const foto = form.value.foto
  const pais_id = parseInt(form.value.pais_id)

  if (!nom || !sigles || !foto || isNaN(pais_id)) {
        alert('Cal omplir tots els camps!')
        return
  }


  try {
    await EquipService.create({
      nom,
      sigles,
      foto,
      pais_id
    })
    await fetchEquips()
    showModal.value = false
  } catch (e) {
    alert('Error creant l equip')
    console.error(e)
  }
}

function toggleMenu(id) {
  menuOpen.value = menuOpen.value === id ? null : id
}

async function esborrarEquip(id) {
  const e = equips.value.find(x => x.id === id)
  if (!e) return
  const confirmat = confirm(`Segur que vols esborrar l equip ${e.nom}?`)
  if (!confirmat) return

  try {
    await EquipService.delete(id)
    await fetchEquips()
  } catch (e) {
    alert('Error esborrant l equip')
    console.error(e)
  }
}

const equipsOrdenats = computed(() =>
  [...equips.value].sort((a, b) => a.nom.localeCompare(b.nom))
)
</script>

<template>
  <div class="main-container">
    <header class="header">
      <h2>Equips</h2>
      <button class="crear-btn" @click="obrirModal">Crear equip</button>
    </header>
    <table class="table align-middle">
      <thead>
        <tr>
          <th>Foto</th>
          <th>Nom</th>
          <th>Sigles</th>
          <th>País</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="e in equipsOrdenats" :key="e.id">
          <td>
            <img v-if="e.foto" :src="e.foto" alt="Foto equip" style="max-width:80px; max-height:80px; border-radius:12px;">
          </td>
          <td>{{ e.nom }}</td>
          <td>{{ e.sigles }}</td>
          <td>
            <img
              v-if="paisos.find(p => p.id === e.pais_id)?.url_imatge"
              :src="paisos.find(p => p.id === e.pais_id).url_imatge"
              :alt="paisos.find(p => p.id === e.pais_id)?.nom"
              style="max-width:40px; max-height:40px; border-radius:8px; background:#fff;"
            />
          </td>
          <td>
            <button class="menu-btn" @click="toggleMenu(e.id)">&#8942;</button>
            <div v-if="menuOpen === e.id" class="menu-dropdown">
              <div @click="esborrarEquip(e.id)">Esborrar equip</div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="showModal" class="modal-overlay" @click.self="tancarModal">
      <div class="modal">
        <h3>Nou equip</h3>
        <form @submit.prevent="crearEquip">
          <label>
            Nom:
            <input v-model="form.nom" required />
          </label>
          <label>
            Sigles:
            <input v-model="form.sigles" required />
          </label>
          <label>
             País:
            <select v-model="form.pais_id" required>
              <option disabled value="">Selecciona un país</option>
              <option v-for="pais in paisos" :key="pais.id" :value="pais.id">
                {{ pais.nom }}
              </option>
            </select>
          </label>
          <div v-if="form.pais_id">
            <img
              v-if="paisos.find(p => p.id === form.pais_id)?.url_imatge"
              :src="paisos.find(p => p.id === form.pais_id).url_imatge"
              alt="Imatge país"
              style="max-width: 40px; max-height: 40px; margin-top: 0.5rem;"
            />
          </div>
          <label>
            Imatge (URL):
            <input v-model="form.foto" type="text" placeholder="https://..." />
          </label>
          <div class="modal-actions">
            <button type="button" @click="tancarModal">Cancel·la</button>
            <button type="submit">Crea</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main-container {
  padding-left: 2rem;
  padding-right: 2rem;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
}
.table {
  width: 100%;
  margin-top: 2rem;
  border-collapse: collapse;
  background: #fff;
}
.table th, .table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}
.table th {
  background: #111;
  color: #fff;
}
.table tr:last-child td {
  border-bottom: none;
}

.competicio-nom {
  color: #fff;
  font-size: 2rem;
  font-weight: bold;
  text-align: center;
  word-break: break-word;
  width: 100%;
}
.crear-btn {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1.2rem;
}
.crear-btn:hover {
  background-color: #1565c0;
}
.menu-btn {
  background: none;
  border: none;
  color: #000000 !important;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0 0.5rem;
}
.menu-dropdown {
  position: absolute;
  right: 0;
  margin-top: 0.5rem;
  background: #222;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.25);
  z-index: 10;
  min-width: 180px;
  overflow: hidden;
}
.menu-dropdown div {
  color: #fff;
  padding: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.menu-dropdown div:hover {
  background: #333;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal {
  background: #222;
  padding: 2rem;
  border-radius: 8px;
  width: 300px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}
.modal h3 {
  margin-top: 0;
  color: #fff;
}
.modal label {
  display: block;
  margin-bottom: 0.5rem;
  color: #ddd;
}
.modal input, .modal select {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: none;
  border-radius: 4px;
}
.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.modal-actions button {
  flex: 1 1 0;
  padding: 0.75rem 0;
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  font-weight: bold;
  color: #fff;
  transition: background 0.2s;
}
.modal-actions button[type="button"] {
  background-color: #e53935;
}
.modal-actions button[type="button"]:hover {
  background-color: #b71c1c;
}
.modal-actions button[type="submit"] {
  background-color: #1976d2;
}
.modal-actions button[type="submit"]:hover {
  background-color: #1565c0;
}
</style>